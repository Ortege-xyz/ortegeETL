from dataclasses import dataclass, asdict
from datetime import datetime
from stellar_sdk.xdr import LedgerHeader
from typing import List, TypedDict

from sorobanetl.domain.transaction import SorobanTransaction

class Ext:
    v: int

class StellarValueExt(Ext):
    lc_value_signature: int

class ExtV1(TypedDict):
    flags: int
    ext: Ext

class ScpValue(TypedDict):
    close_time: int
    tx_set_hash: str
    upgrades: list
    

class LedgerHeaderExt(TypedDict):
    v: int
    v1: ExtV1 

class Header(TypedDict):
    base_fee: int
    base_reserve: int
    ledger_version: int
    scp_value: StellarValueExt
    tx_set_result_hash: str
    bucket_list_hash: str
    ledger_seq: int
    inflation_seq: int
    id_pool: int
    skip_list: List[str]
    ext: LedgerHeaderExt

@dataclass
class SorobanLedger:
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
    header: Header

    transactions: List[SorobanTransaction]
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

        header = LedgerHeader.from_xdr(json_dict["header_xdr"])
        decoded_header: Header = {}
        decoded_header["base_fee"] = header.base_fee.uint32
        decoded_header["base_reserve"] = header.base_reserve.uint32
        decoded_header["bucket_list_hash"] = header.bucket_list_hash.hash.hex()
        decoded_header["id_pool"] = header.id_pool.uint64
        decoded_header["ledger_version"] = header.ledger_version.uint32
        decoded_header["ledger_seq"] = header.ledger_seq.uint32
        decoded_header["tx_set_result_hash"] = header.tx_set_result_hash.hash.hex()
        decoded_header["inflation_seq"] = header.inflation_seq.uint32
        decoded_header["ext"] = {
            "v": header.ext.v,
            "v1": {
                "flags": header.ext.v1.flags.uint32,
                "ext": {
                    "v": header.ext.v1.ext.v
                },
            },
        }
        decoded_header["skip_list"] = [value.hash.hex() for value in header.skip_list]

        json_dict["header"] = decoded_header

        return SorobanLedger(**json_dict)
    
    def ledger_to_dict(self):
        ledger_dict = asdict(self)
        ledger_dict["type"] = "ledger"
        
        del ledger_dict["transactions"]

        return ledger_dict
