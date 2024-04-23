import json
from stellar_sdk import StrKey
from stellar_sdk.xdr import (
    Int32,
    Int64,
    Uint32,
    Uint64,
    Uint256,
    Int128Parts,
    Int256Parts,
    UInt128Parts,
    UInt256Parts,
    Hash,
    String32,
    String64,
    String,
    Boolean,
    AccountID,
    PublicKey,
    MuxedAccount,
    SCVal,
    SCBytes,
    SCMap,
    SCVec,
    SCString,
    SCSymbol,
    SCNonceKey,
    SCAddress,
    TimePoint,
    SequenceNumber,
    Thresholds,
)
from enum import Enum
from typing import Any, List, Dict, Optional

def convert_xdr(value: object, value_name: Optional[str] = None):
    """This function convert a class from xdr in python type

    Args:
        value (object): Value to be converted
        value_name (Optional[str], optional): The name of the key if this value is a value of a key in a dictionary. Defaults to None.

    """
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
    if isinstance(value, Int128Parts):
        hi_value = value.hi.int64 
        lo_value = value.lo.uint64
        return (hi_value << 64) | lo_value
    if isinstance(value, UInt128Parts):
        hi_value = value.hi.uint64 
        lo_value = value.lo.uint64
        return (hi_value << 64) | lo_value
    if isinstance(value, Int256Parts):
        hi_hi_value = value.hi_hi.int64
        hi_lo_value = value.hi_lo.uint64
        lo_hi_value = value.lo_hi.uint64
        lo_lo_value = value.lo_lo.uint64
        return (hi_hi_value << 192) | (hi_lo_value << 128) | (lo_hi_value << 64) | lo_lo_value
    if isinstance(value, UInt256Parts):
        hi_hi_value = value.hi_hi.uint64
        hi_lo_value = value.hi_lo.uint64
        lo_hi_value = value.lo_hi.uint64
        lo_lo_value = value.lo_lo.uint64
        return (hi_hi_value << 192) | (hi_lo_value << 128) | (lo_hi_value << 64) | lo_lo_value
    if isinstance(value, Hash):
        return value.hash.hex()
    if isinstance(value, String):
        return value.value.decode("utf-8")
    if isinstance(value, (String32, String64)):
        text: str = getattr(value, type(value).__name__.lower()).decode("utf-8") # the attribute to bytes in these classes is the name of class lower, eg String32.string32
        return text
    if isinstance(value, Boolean):
        return value.value
    if isinstance(value, AccountID):
        return StrKey.encode_ed25519_public_key(value.account_id.ed25519.to_xdr_bytes())
    if isinstance(value, (PublicKey, MuxedAccount)):
        if value.ed25519 is not None:
            return StrKey.encode_ed25519_public_key(value.ed25519.to_xdr_bytes())
        return None
    if isinstance(value, TimePoint):
        return value.time_point.uint64
    if isinstance(value, SequenceNumber):
        return value.sequence_number.int64
    if isinstance(value, Thresholds):
        return value.thresholds.hex()
    if isinstance(value, SCAddress):
        return convert_xdr(value.account_id)
    if isinstance(value, SCBytes):
        return value.sc_bytes.hex()
    if isinstance(value, SCString):
        return value.sc_string.decode("utf-8")
    if isinstance(value, SCSymbol):
        return value.sc_symbol.decode("utf-8")
    if isinstance(value, SCVec):
        vec: List[Any] = []
        for vec_value in value.sc_vec:
            _vec_value = convert_xdr(vec_value)
            if _vec_value is not None:
                vec.append(_vec_value)
        return vec
    if isinstance(value, SCMap):
        sc_map: Dict[str, Any] = {}
        for entry in value.sc_map:
            entry_key = convert_xdr(entry.key)
            entry_value = convert_xdr(entry.val)
            str_entry_key = str(entry_key)
            sc_map[str_entry_key] = entry_value
        return sc_map
    if isinstance(value, SCNonceKey):
        return value.nonce.int64
    if isinstance(value, SCVal):
        value_Dict = value.__dict__
        if value_Dict.get('type') is not None:
            del value_Dict['type']

        for attr_value in value_Dict.values():
            if attr_value is None:
                continue
            sc_value = convert_xdr(attr_value)
            
            if isinstance(sc_value, (dict, list)):
                return json.dumps(sc_value)   

            if sc_value is not None:
                return sc_value
        return None
    if isinstance(value, (List, tuple, set)):
        items = []
        for item in value:
            if item is not None:
                coverted_item = convert_xdr(item)
                if coverted_item is not None:
                    items.append(coverted_item)
        return items
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    if isinstance(value, (int, float, str, bool)):
        return value
    
    value_Dict = value.__dict__

    for key, value in value_Dict.items():
        value_Dict[key] = convert_xdr(value, key)
    return value_Dict