from dataclasses import dataclass, asdict
from datetime import datetime
from stellar_sdk.xdr import LedgerHeader
from typing import Any, Dict, List, Optional

from stellaretl.convert_xdr import convert_xdr
from stellaretl.domain.transaction import StellarTransaction

@dataclass
class StellarLedger:
    id: str
    sequence: int
    hash: str
    prev_hash: str
    timestamp: int
    closed_at: str
    total_coins: str
    fee_pool: str
    base_fee_in_stroops: int
    base_reserve_in_stroops: int
    max_tx_set_size: int
    protocol_version: int
    paging_token: str

    header_xdr: str
    header: Optional[Dict[str, Any]]

    transactions: List[StellarTransaction]
    successful_transaction_count: int
    failed_transaction_count: int
    operation_count: int
    tx_set_operation_count: int

    @staticmethod
    def json_dict_to_ledger(json_dict: dict):
        timestamp_obj = datetime.fromisoformat(json_dict["closed_at"].rstrip("Z"))
        json_dict["timestamp"] = int(timestamp_obj.timestamp())
        json_dict["transactions"] = []

        del json_dict["_links"]

        try:
            header = LedgerHeader.from_xdr(json_dict["header_xdr"])
            decoded_header: Dict[str, Any] = convert_xdr(header) # type: ignore
        except:
            decoded_header = None # type: ignore

        json_dict["header"] = decoded_header

        return StellarLedger(**json_dict)
    
    def ledger_to_dict(self):
        ledger_dict = asdict(self)
        ledger_dict["type"] = "ledger"
        
        del ledger_dict["transactions"]

        return ledger_dict
