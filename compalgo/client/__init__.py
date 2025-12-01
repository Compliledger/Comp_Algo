from __future__ import annotations

from typing import Union, Dict, Any

from .algorand import AlgorandClient, AnchorResult, explorer_url_for
from ..core.verdict import ComplianceVerdict, verdict_hash


class CompliLedgerClient:
    def __init__(self, *, algod_url: str, algod_token: str = "", sender_mnemonic: str, network: str = "testnet"):
        self._algo = AlgorandClient(algod_url=algod_url, algod_token=algod_token, network=network)
        self._mnemonic = sender_mnemonic
        self._network = network

    def mint_verdict(self, verdict: Union[ComplianceVerdict, Dict[str, Any]]) -> AnchorResult:
        v = verdict if isinstance(verdict, ComplianceVerdict) else ComplianceVerdict(**verdict)
        h = verdict_hash(v)
        note_text = f"CLG1|sha256:{h}"
        txid = self._algo.send_note_tx(self._mnemonic, note_text)
        return AnchorResult(txid=txid, explorer_url=explorer_url_for(txid, self._network), verdict_hash=h, network=self._network)

    def verify_verdict(self, verdict: Union[ComplianceVerdict, Dict[str, Any]], txid: str) -> bool:
        v = verdict if isinstance(verdict, ComplianceVerdict) else ComplianceVerdict(**verdict)
        h = verdict_hash(v)
        nt = self._algo.get_note_text(txid) or ""
        return nt.strip() == f"CLG1|sha256:{h}"
