from dataclasses import dataclass, asdict, fields
from typing import Any, List, TypedDict

class TransactionSignature(TypedDict):
    type: str
    public_key: str
    signatura: str

class TransactionPayload(TypedDict):
    type: str
    function: str
    type_arguments: List[str]
    arguments: List[Any]

@dataclass
class AptosTransaction:
    hash: str
    sender: str
    sequence_number: int
    max_gas_amount: int
    gas_unit_price: int
    expiration_timestamp_secs: int
    payload: TransactionPayload
    signature: TransactionSignature
    tx_type: str

    @staticmethod
    def from_dict(json_dict: dict):
        valid_fields = {field.name for field in fields(AptosTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        filtered_data["sequence_number"] = int(json_dict['sequence_number'])
        filtered_data["max_gas_amount"] = int(json_dict['max_gas_amount'])
        filtered_data["gas_unit_price"] = int(json_dict['gas_unit_price'])
        filtered_data["expiration_timestamp_secs"] = int(json_dict['expiration_timestamp_secs'])
        filtered_data["tx_type"] = json_dict['type']

        return AptosTransaction(**filtered_data)
    
    def to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict

