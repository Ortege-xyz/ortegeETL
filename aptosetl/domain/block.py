from dataclasses import dataclass, asdict, fields
from typing import List

from aptosetl.domain.transaction import AptosTransaction

@dataclass
class AptosBlock:
    number: int
    hash: str
    timestamp: int
    first_version: int
    last_version: int

    transactions: List[AptosTransaction]

    @staticmethod
    def from_dict(json_dict: dict):
        valid_fields = {field.name for field in fields(AptosTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        filtered_data["hash"] = int(json_dict['block_hash'])
        filtered_data["number"] = int(json_dict['block_height'])
        filtered_data["timestamp"] = int(json_dict['max_gas_amount'])
        filtered_data["first_version"] = int(json_dict['block_timestamp'])
        filtered_data["last_version"] = int(json_dict['last_version'])
        
        json_dict["transactions"] = []

        return AptosBlock(**json_dict)
    
    def to_dict(self):
        block_dict = asdict(self)
        block_dict["type"] = "block"
        
        del block_dict["transactions"]

        return block_dict
