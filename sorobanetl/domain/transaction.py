from dataclasses import dataclass
from typing import Dict, List, TypedDict

class Preconditions(TypedDict):
    timebounds: Dict[str, str]

@dataclass
class SorobanTransaction:
    paging_token: str
    successful: bool
    hash: str
    ledger: int
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