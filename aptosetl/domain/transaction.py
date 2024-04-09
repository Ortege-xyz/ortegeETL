from dataclasses import dataclass, asdict, fields
from typing import Any, List, Optional

@dataclass
class AptosTransaction:
    hash: str
    block_number: int
    state_change_hash: str
    event_root_hash: str
    version: int
    gas_used: int
    success: bool
    vm_status: str
    accumulator_root_hash: str
    changes: list[Any]
    events: list[Any]
    tx_type: str
    
    #optionals parameters
    state_checkpoint_hash: Optional[str]
    payload: Optional[dict]
    id: Optional[str]
    epoch: Optional[str]
    round: Optional[str]
    previous_block_votes_bitvec: Optional[List[int]]
    proposer: Optional[str]
    failed_proposer_indices: Optional[list[str]]
    timestamp: Optional[int]

    @staticmethod
    def from_dict(json_dict: dict):
        valid_fields = {field.name for field in fields(AptosTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        filtered_data["block_number"] = int(json_dict['block_number'])
        filtered_data["version"] = int(json_dict['version'])
        filtered_data["gas_used"] = int(json_dict['gas_used'])
        filtered_data["tx_type"] = json_dict['type']

        return AptosTransaction(**filtered_data)
    
    def to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict

