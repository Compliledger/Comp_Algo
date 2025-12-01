from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from ..analyzer.checker import ComplianceChecker
from ..core.verdict import build_verdict, ComplianceVerdict
from ..client import CompliLedgerClient

console = Console()


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_text(path: str, content: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


@click.group()
def cli():
    """CompliLedger Algorand SDK CLI (P0)

    Commands:
      - check:    scan PyTeal/TEAL and print violations & score
      - report:   export report (json/html/markdown)
      - list-policies
      - anchor:   anchor a Compliance Verdict JSON on Algorand
      - verify:   verify a verdict against a TXID
    """


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--policy", default="algorand-baseline", help="Policy pack name")
@click.option("--threshold", default=80, type=int, help="Pass score threshold (0-100)")
@click.option("--verdict-out", type=click.Path(), help="Output a Compliance Verdict JSON (only when checking a single file)")
def check(path: str, policy: str, threshold: int, verdict_out: Optional[str]):
    ck = ComplianceChecker(policy_pack=policy, threshold=threshold)
    results = ck.check_path(path)

    total_files = len(results)
    failed = 0

    table = Table(title=f"Compliance Check ({policy})")
    table.add_column("File")
    table.add_column("Score", justify="right")
    table.add_column("Passed", justify="center")
    table.add_column("Critical/High/Med/Low", justify="center")

    for r in results:
        crit = r.counts.get("critical", 0)
        high = r.counts.get("high", 0)
        med = r.counts.get("medium", 0)
        low = r.counts.get("low", 0)
        table.add_row(
            os.path.relpath(r.file_path),
            str(r.score),
            "✅" if r.passed else "❌",
            f"{crit}/{high}/{med}/{low}",
        )
        if not r.passed:
            failed += 1

    console.print(table)

    # Print detailed violations
    for r in results:
        if r.violations:
            console.rule(f"[bold]Details: {os.path.relpath(r.file_path)}")
            for v in r.violations:
                console.print(f"[bold red]{v['severity'].upper()}[/bold red] {v['rule_id']}: {v['message']}")
                if v.get("controls"):
                    console.print(f"  Controls: {', '.join([c['framework']+':'+c['control_id'] for c in v['controls']])}")

    if failed:
        console.print(f"[red]Failed {failed}/{total_files} file(s)[/red]")
        sys.exit(1)
    else:
        console.print("[green]All files passed threshold[/green]")

    # Optional: generate Compliance Verdict JSON for single file run
    if verdict_out:
        if os.path.isdir(path):
            console.print("[red]--verdict-out is only supported when PATH is a single file[/red]")
            sys.exit(1)
        # Find the single result
        r = results[0]
        # Build verdict: use SOC2/CC6.1 by default, fail_on derived from threshold via severity bands
        def band(th: int) -> str:
            if th >= 90:
                return "medium"
            if th >= 80:
                return "high"
            return "critical"
        from ..core.verdict import build_verdict

        verdict = build_verdict(
            contract=os.path.relpath(r.file_path),
            violations=r.violations,
            framework="SOC2",
            control_id="CC6.1",
            fail_on=band(threshold),
        )
        _save_text(verdict_out, json.dumps(verdict.model_dump(), indent=2))
        console.print(f"[green]Verdict written:[/green] {verdict_out}")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--policy", default="algorand-baseline", help="Policy pack")
@click.option("--format", "fmt", default="json", type=click.Choice(["json", "html", "markdown"]))
@click.option("-o", "output", required=True, help="Output file path")
def report(path: str, policy: str, fmt: str, output: str):
    ck = ComplianceChecker(policy_pack=policy)
    results = ck.check_path(path)
    data = []
    for r in results:
        data.append({
            "file": r.file_path,
            "score": r.score,
            "passed": r.passed,
            "violations": r.violations,
        })

    if fmt == "json":
        _save_text(output, json.dumps({"policy": policy, "results": data}, indent=2))
    elif fmt == "markdown":
        lines = [f"# Compliance Report ({policy})", ""]
        for r in results:
            lines.append(f"## {r.file_path}")
            lines.append(f"Score: {r.score}  Passed: {'Yes' if r.passed else 'No'}")
            for v in r.violations:
                lines.append(f"- **{v['severity'].upper()}** {v['rule_id']}: {v['message']}")
            lines.append("")
        _save_text(output, "\n".join(lines))
    else:  # html
        html = ["<html><body>", f"<h1>Compliance Report ({policy})</h1>"]
        for r in results:
            html.append(f"<h2>{r.file_path}</h2>")
            html.append(f"<p>Score: {r.score} &nbsp; Passed: {'Yes' if r.passed else 'No'}</p>")
            if r.violations:
                html.append("<ul>")
                for v in r.violations:
                    html.append(f"<li><b>{v['severity'].upper()}</b> {v['rule_id']}: {v['message']}</li>")
                html.append("</ul>")
        html.append("</body></html>")
        _save_text(output, "".join(html))
    console.print(f"[green]Report written:[/green] {output}")


@cli.command("list-policies")
def list_policies():
    pol_dir = Path(__file__).resolve().parents[1] / "policies"
    packs = []
    for f in pol_dir.glob("*.json"):
        packs.append(f.stem)
    console.print("Available policies:")
    for p in sorted(packs):
        console.print(f"- {p}")


@cli.command()
@click.option("--verdict", "verdict_path", type=click.Path(exists=True), required=True, help="Path to Compliance Verdict JSON")
@click.option("--network", default="testnet", type=click.Choice(["testnet", "mainnet"]))
@click.option("--algod-url", envvar="ALGO_URL", default="https://testnet-api.algonode.cloud")
@click.option("--algod-token", envvar="ALGO_TOKEN", default="")
@click.option("--mnemonic", envvar="ALGO_MNEMONIC", required=True)
def anchor(verdict_path: str, network: str, algod_url: str, algod_token: str, mnemonic: str):
    v = _load_json(verdict_path)
    client = CompliLedgerClient(algod_url=algod_url, algod_token=algod_token, sender_mnemonic=mnemonic, network=network)
    res = client.mint_verdict(v)
    console.print(f"[green]Anchored![/green] TXID: {res.txid}")
    console.print(f"Explorer: {res.explorer_url}")


@cli.command()
@click.option("--verdict", "verdict_path", type=click.Path(exists=True), required=True)
@click.option("--txid", required=True)
@click.option("--network", default="testnet", type=click.Choice(["testnet", "mainnet"]))
@click.option("--algod-url", envvar="ALGO_URL", default="https://testnet-api.algonode.cloud")
@click.option("--algod-token", envvar="ALGO_TOKEN", default="")
def verify(verdict_path: str, txid: str, network: str, algod_url: str, algod_token: str):
    v = _load_json(verdict_path)
    # mnemonic not required to verify
    client = CompliLedgerClient(algod_url=algod_url, algod_token=algod_token, sender_mnemonic=os.getenv("ALGO_MNEMONIC", ""), network=network)
    ok = client.verify_verdict(v, txid)
    console.print("[green]VALID[/green]" if ok else "[red]INVALID[/red]")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    cli()
