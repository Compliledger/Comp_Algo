from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Optional

from algosdk.v2client import algod
from algosdk import transaction, mnemonic


@dataclass
class AnchorResult:
    txid: str
    explorer_url: str
    verdict_hash: str
    network: str


def explorer_url_for(txid: str, network: str = "testnet") -> str:
    base = "https://testnet.algoexplorer.io/tx/" if network == "testnet" else "https://algoexplorer.io/tx/"
    return f"{base}{txid}"


class AlgorandClient:
    def __init__(self, algod_url: str, algod_token: str, network: str = "testnet"):
        self.algod = algod.AlgodClient(algod_token, algod_url)
        self.network = network

    def send_note_tx(self, sender_mnemonic: str, note_text: str) -> str:
        sender_sk = mnemonic.to_private_key(sender_mnemonic)
        sender_addr = mnemonic.to_public_key(sender_mnemonic)
        params = self.algod.suggested_params()
        params.flat_fee = True
        params.fee = max(params.min_fee, 1000)
        txn = transaction.PaymentTxn(
            sender=sender_addr,
            sp=params,
            receiver=sender_addr,
            amt=0,
            note=note_text.encode("utf-8"),
        )
        signed = txn.sign(sender_sk)
        txid = self.algod.send_transaction(signed)
        transaction.wait_for_confirmation(self.algod, txid, 4)
        return txid

    def get_note_text(self, txid: str) -> Optional[str]:
        info = self.algod.pending_transaction_info(txid)
        # note is base64 in different nesting levels depending on SDK version
        note_b64 = (
            info.get("txn", {}).get("txn", {}).get("note")
            or info.get("txn", {}).get("note")
            or info.get("note")
        )
        if not note_b64:
            return None
        try:
            raw = base64.b64decode(note_b64)
            return raw.decode("utf-8", errors="ignore")
        except Exception:
            return None
