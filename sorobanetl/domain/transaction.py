from dataclasses import dataclass, asdict, fields
from datetime import datetime
from stellar_sdk import StrKey
from stellar_sdk.xdr import (
    FeeBumpTransaction,
    TransactionResult,
    TransactionEnvelope,
    Int32,
    Int64,
    Uint32,
    Uint64,
    Uint256,
    Hash,
    String32,
    String64,
    String,
    Boolean,
    AccountID,
    PublicKey,
    MuxedAccount,
)
from enum import Enum
from typing import Any, List, Dict, TypedDict, Optional

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
    envelope: Dict[str, Any]
    result_xdr: str
    result: Dict[str, Any]
    result_meta_xdr: str
    fee_meta_xdr: str
    fee_meta: str
    memo_type: str
    memo: Optional[str]
    memo_bytes: Optional[str]
    signatures: List[str]
    valid_after: Optional[str]
    valid_before: Optional[str]
    preconditions: Optional[Preconditions]

    @staticmethod
    def json_dict_to_transaction(json_dict: dict):
        timestamp_obj = datetime.fromisoformat(json_dict["created_at"].rstrip("Z"))
        json_dict["timestamp"] = int(timestamp_obj.timestamp())

        valid_fields = {field.name for field in fields(SorobanTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        valid_after = filtered_data.get("valid_after")
        filtered_data["valid_after"] = valid_after

        valid_before = filtered_data.get("valid_before")
        filtered_data["valid_before"] = valid_before

        memo = filtered_data.get("memo")
        filtered_data["memo"] = memo

        memo_bytes = filtered_data.get("memo_bytes")
        filtered_data["memo_bytes"] = memo_bytes

        preconditions = filtered_data.get("preconditions")
        filtered_data["preconditions"] = preconditions

        result = TransactionResult.from_xdr(filtered_data.get("result_xdr"))
        filtered_data["result"] = SorobanTransaction.convert_xdr(result)

        envelope = TransactionEnvelope.from_xdr(filtered_data.get('envelope_xdr'))
        filtered_data["envelope"] = SorobanTransaction.convert_xdr(envelope)

        fee_meta = FeeBumpTransaction.from_xdr(filtered_data.get('fee_meta_xdr'))
        filtered_data["fee_meta"] = SorobanTransaction.convert_xdr(fee_meta)

        return SorobanTransaction(**filtered_data)
    
    def transaction_to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict
    
    def convert_xdr(value: object, value_name: str = None):
        if value is None:
            return None
        if isinstance(value, Enum):
            return value.name
        if isinstance(value, (Int32, Int64, Uint32, Uint64)):
            attribute: int = getattr(value, type(value).__name__.lower()) # the attribute to int in these classes is the name of class lower, eg Int32.int32
            return attribute
        if isinstance(value, Uint256):
            if(value_name == "ed25519"):
                return StrKey.encode_ed25519_public_key(value.uint256)
            return int.from_bytes(value.uint256, byteorder="big")
        if isinstance(value, Hash):
            return value.hash.hex()
        if isinstance(value, String):
            return value.value.decode("utf-8")
        if isinstance(value, (String32, String64)):
            text: str = getattr(value, type(value).__name__.lower()).decode("utf-8") # the attribute to bytes in these classes is the name of class lower, eg String32.string32
            return text
        if isinstance(value, AccountID):
            return StrKey.encode_ed25519_public_key(value.account_id.ed25519.to_xdr_bytes())
        if isinstance(value, (PublicKey, MuxedAccount)):
            if value.ed25519 is not None:
                return StrKey.encode_ed25519_public_key(value.ed25519.to_xdr_bytes())
        if isinstance(value, Boolean):
            return value.value
        if isinstance(value, (list, tuple, set)):
            return [SorobanTransaction.convert_xdr(item) for item in value]
        if isinstance(value, (bytes, bytearray)):
            return value.hex()
        if isinstance(value, (int, float, str, bool)):
            return value
        
        value_dict = value.__dict__

        for key, value in value_dict.items():
            value_dict[key] = SorobanTransaction.convert_xdr(value, key)
        return value_dict
