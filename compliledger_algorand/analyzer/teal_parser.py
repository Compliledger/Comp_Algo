from __future__ import annotations

from typing import Dict, Any


def parse_teal_file(file_path: str) -> Dict[str, Any]:
    """Very small TEAL signal parser for P0.
    We scan for key opcodes/keywords to power rule checks.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [ln.strip().lower() for ln in f.readlines()]

    def any_contains(substr: str) -> bool:
        return any(substr in ln for ln in lines)

    return {
        "uses_delete": any_contains("delete_application"),
        "uses_update": any_contains("update_application"),
        "uses_global_put": any_contains("app_global_put"),
        "uses_local_put": any_contains("app_local_put"),
        "uses_box_ops": any(any_contains(k) for k in ["box_put", "box_replace", "box_create"]),
        "has_assert": any_contains("assert"),
        "uses_inner_txn": any_contains("inner_txn") or any_contains("itxn"),
        "has_fee_bound_assert": any_contains("txn fee") and any_contains("<=") and any_contains("assert"),
        "has_admin_sender_assert": any_contains("txn sender") and any_contains("global creator_address") and any_contains("==") and any_contains("assert"),
        "has_rekey_zero_assert": any_contains("txn rekey_to") and any_contains("global zero_address") and any_contains("==") and any_contains("assert"),
        "has_close_zero_assert": any_contains("txn close_remainder_to") and any_contains("global zero_address") and any_contains("==") and any_contains("assert"),
        "uses_btoi_args": any_contains("btoi") and any_contains("txna ApplicationArgs".lower()),
    }
