import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from stellar_sdk.xdr import SCVal
from typing import Any, Dict, List, Optional

from stellaretl.convert_xdr import convert_xdr

@dataclass
class SorobanEvent:
    event_type: str
    ledger: int
    ledger_closed_at: int
    contract_id: str
    tx_hash: str
    id: str
    paging_token: str
    topic: Optional[List[str]]
    value: Optional[str]
    in_successful_contract_call: bool

    @staticmethod
    def from_dict(json_dict: Dict[str, Any]):
        timestamp_obj = datetime.fromisoformat(json_dict["ledgerClosedAt"].rstrip("Z"))
        json_dict["ledger_closed_at"] = int(timestamp_obj.timestamp())
        json_dict["paging_token"] = json_dict["pagingToken"]
        json_dict["contract_id"] = json_dict["contractId"]
        json_dict["in_successful_contract_call"] = json_dict["inSuccessfulContractCall"]
        json_dict["tx_hash"] = json_dict["txHash"]
        json_dict["event_type"] = json_dict["type"]
        

        del json_dict["ledgerClosedAt"]
        del json_dict["pagingToken"]
        del json_dict["contractId"]
        del json_dict["inSuccessfulContractCall"]
        del json_dict["txHash"]
        del json_dict["type"]

        try:
            if(isinstance(json_dict["value"], str)):
                value = str(convert_xdr(SCVal.from_xdr(json_dict["value"])))
            elif(isinstance(json_dict["value"], dict)):
                value = str(convert_xdr(SCVal.from_xdr(json_dict["value"]["xdr"])))
            else:
                value = None
            json_dict["value"] = value
        except Exception as e:
            logging.warning(f"Error to convert the event value {json_dict.get('value')} id {json_dict['id']}, {e}")
            json_dict["value"] = None

        topic: Optional[List[str]] = []
        try:
            for _topic in json_dict["topic"]:
                topic.append(str(convert_xdr(SCVal.from_xdr(_topic))))
        except Exception as e:
            logging.warning(f"Error to convert the event topic {json_dict.get('topic')} id {json_dict['id']}, {e}")
            topic = None
        finally:
            json_dict["topic"] = topic

        return SorobanEvent(**json_dict)
    
    def to_dict(self):
        event_dict = asdict(self)
        event_dict["type"] = "event"

        return event_dict
