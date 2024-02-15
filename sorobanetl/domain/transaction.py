from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, TypedDict

class Preconditions(TypedDict):
    timebounds: Dict[str, str]

@dataclass
class SorobanTransaction:
    paging_token: str
    successful: bool
    hash: str
    ledger: int
    datetime: int
    created_at: str
    source_account: str
    source_account_sequence: str
    fee_account: str
    fee_charged: str
    max_fee: str
    operation_count: int
    envelope_xdr: str
    result_xdr: str
    result_meta_xdr: str
    fee_meta_xdr: str
    memo_type: str
    signatures: List[str]
    valid_after: str
    preconditions: Preconditions

    @staticmethod
    def json_dict_to_transaction(json_dict: dict):
        timestamp_obj = datetime.fromisoformat(json_dict["closed_at"].rstrip("Z"))
        json_dict["timestamp"] = int(timestamp_obj.timestamp())
        return SorobanTransaction(**json_dict)
    
    def transaction_to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict
