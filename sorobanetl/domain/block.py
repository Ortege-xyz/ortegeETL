from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, List

@dataclass
class SorobanBlock:
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
    header_xdr: str

    transactions: List[Any]
    successful_transaction_count: int
    failed_transaction_count: int
    operation_count: int
    tx_set_operation_count: int

    @staticmethod
    def json_dict_to_block(json_dict: dict):
        timestamp_obj = datetime.fromisoformat(json_dict["closed_at"].rstrip("Z"))
        json_dict["timestamp"] = int(timestamp_obj.timestamp())
        return SorobanBlock(**json_dict)
    
    def block_to_dict(self):
        return asdict(self)
