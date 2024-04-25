from stellaretl.api.soroban_rpc import SorobanRpc
from typing import Any, Optional, Union

from stellaretl.domain.event import SorobanEvent

class SorobanService():
    def __init__(self, soroban_rpc: SorobanRpc):
        self.soroban_rpc = soroban_rpc

    def get_latest_ledger(self):
        ledger_result = self.soroban_rpc.getLatestLedger()

        if ledger_result is None: 
            return None

        return ledger_result

    def get_events(
        self,
        start_ledger: int,
        filters: Optional[list[dict[str, Any]]] = None,
        pagination: Optional[dict[str, Union[str, int, None]]] = None
    ) -> list[SorobanEvent]:
        param: dict[str, Any] = {
            'startLedger': start_ledger,
        }
        
        if filters:
            param['filters'] = filters
        if pagination:
            param['pagination'] = pagination

        result = self.soroban_rpc.getEvents(param)

        if result is None:
            return []
        import json
        events = result.get('events', [])

        return [SorobanEvent.from_dict(event) for event in events]

    def get_ledger_entries(self, entries_keys: list[str]) -> list[dict[str, Union[str, int]]]:
        param = {
            'keys': entries_keys,
        }
        result = self.soroban_rpc.getLedgerEntries(param)
        if result is None:
            return []

        entries = result.get('entries', [])
        return entries
