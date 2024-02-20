from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Dict, List, TypedDict, Optional

class Timebounds(TypedDict):
    min_time: Optional[str]
    max_time: Optional[str]

class Ledgerbounds(TypedDict):
    min_ledger: Optional[int]
    max_ledger: Optional[int]

class Preconditions(TypedDict):
    timebounds: Optional[Timebounds]
    ledgerbounds: Optional[Ledgerbounds]
    min_account_sequence: Optional[str]
    min_account_sequence_age: Optional[int]
    min_account_sequence_ledger_gap: Optional[int]
    extra_signers: Optional[List[str]]


@dataclass
class SorobanTransaction:
    id: str
    paging_token: str
    successful: bool
    hash: str
    ledger: int
    timestamp: int
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
    memo: str
    memo_bytes: str
    signatures: List[str]
    valid_after: str
    valid_before: str
    preconditions: Optional[Preconditions]

    @staticmethod
    def json_dict_to_transaction(json_dict: dict):
        timestamp_obj = datetime.fromisoformat(json_dict["created_at"].rstrip("Z"))
        json_dict["timestamp"] = int(timestamp_obj.timestamp())

        valid_fields = {field.name for field in fields(SorobanTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        valid_after = filtered_data.get("valid_after", "")
        filtered_data["valid_after"] = valid_after

        valid_before = filtered_data.get("valid_before", "")
        filtered_data["valid_before"] = valid_before

        memo = filtered_data.get("memo", "")
        filtered_data["memo"] = memo

        memo_bytes = filtered_data.get("memo_bytes", "")
        filtered_data["memo_bytes"] = memo_bytes

        preconditions = filtered_data.get("preconditions")
        filtered_data["preconditions"] = preconditions

        return SorobanTransaction(**filtered_data)
    
    def transaction_to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict
