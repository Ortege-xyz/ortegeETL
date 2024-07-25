import decimal
import json
import re
import requests
from typing import Any, Dict, List, Optional, Union

class SorobanRpc:

    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout

    def batch(self, commands: List[List[Union[str, dict]]]):
        rpc_calls = []
        for i, command in enumerate(commands, 1):
            method: str = command.pop(0) # type: ignore
            if len(command) == 0:
                rpc_calls.append({"jsonrpc": "2.0", "method": method, "id": str(i)})
            elif len(command) == 1:
                rpc_calls.append({"jsonrpc": "2.0", "method": method, "params": command[0], "id": str(i)})
            else:
                rpc_calls.append({"jsonrpc": "2.0", "method": method, "params": command, "id": str(i)})
        
        response = requests.post(
            url=self.provider_uri,
            json=rpc_calls,
            timeout=self.timeout
        )
        
        data = response.json()
        
        if isinstance(data, dict):
            return [data.get('result')]
        
        result = []
        for resp_item in response.json():
            if resp_item.get('result') is None:
                raise ValueError('"result" is None in the JSON RPC response {}. Request: {}', resp_item.get('error'), rpc_calls)
            result.append(resp_item.get('result'))
        return result

    def getLedgerEntries(self, param: Dict[str, Any]):
        response = self.batch([['getLedgerEntries', param]])
        return response[0] if len(response) > 0 else None
    
    def getEvents(self, param: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = self.batch([['getEvents', param]])
        return response[0] if len(response) > 0 else None

    def getLatestLedger(self):
        response = self.batch([['getLatestLedger']])
        return response[0] if len(response) > 0 else None

    def getNetwork(self):
        response = self.batch([['getNetwork']])
        return response[0] if len(response) > 0 else None
    
    def getTransaction(self):
        response = self.batch([['getTransaction']])
        return response[0] if len(response) > 0 else None

    def _decode_rpc_response(self, response):
        response_text = response.decode('utf-8')
        return json.loads(response_text, parse_float=decimal.Decimal)
