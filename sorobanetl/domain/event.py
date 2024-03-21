from dataclasses import dataclass, asdict
from datetime import datetime
from stellar_sdk.xdr import SCVal
from typing import Any, Optional

from sorobanetl.convert_xdr import convert_xdr

@dataclass
class SorobanEvent:
    type: str
    ledger: int
    ledger_closed_at: int
    contract_id: str
    tx_hash: str
    id: int
    paging_token: str
    topic: list[Any]
    value: Any
    in_successful_contract_call: bool

    @staticmethod
    def from_dict(json_dict: dict[str, Any]):
        timestamp_obj = datetime.fromisoformat(json_dict["ledgerClosedAt"].rstrip("Z"))
        json_dict["ledger_closed_at"] = int(timestamp_obj.timestamp())
        json_dict["paging_token"] = json_dict["pagingToken"]
        json_dict["contract_id"] = json_dict["contractId"]
        json_dict["in_successful_contract_call"] = json_dict["inSuccessfulContractCall"]
        json_dict["tx_hash"] = json_dict["txHash"]

        del json_dict["ledgerClosedAt"]
        del json_dict["pagingToken"]
        del json_dict["contractId"]
        del json_dict["inSuccessfulContractCall"]
        del json_dict["txHash"]

        try:
            json_dict["value"] = convert_xdr(SCVal.from_xdr(json_dict["value"]["xdr"]))
        except:
            json_dict["value"] = None

        topic = []
        try:
            for _topic in json_dict["topic"]:
                topic.append(convert_xdr(SCVal.from_xdr(_topic)))
        finally:
            json_dict["topic"] = topic

        return SorobanEvent(**json_dict)
    
    def to_dict(self):
        event_dict = asdict(self)
        event_dict["type"] = "event"

        return event_dict
