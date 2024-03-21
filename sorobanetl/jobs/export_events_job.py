from sorobanetl.api.soroban_rpc import SorobanRpc
from sorobanetl.domain.event import SorobanEvent
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range
from blockchainetl.classes.base_item_exporter import BaseItemExporter
from sorobanetl.service.soroban_service import SorobanService

# Exports events
class ExportEventsJob(BaseJob):
    def __init__(
            self,
            start_ledger: int,
            end_ledger: int,
            batch_size: int,
            soroban_rpc: SorobanRpc,
            max_workers: int,
            item_exporter: BaseItemExporter
        ):
        validate_range(start_ledger, end_ledger)
        self.start_ledger = start_ledger
        self.end_ledger = end_ledger
        self.batch_size = batch_size

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.service = SorobanService(soroban_rpc)
        self.ledger_events_cache: dict[int, dict[str, SorobanEvent]] = {}

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_ledger, self.end_ledger + 1),
            self._export_batch,
            total_items=self.end_ledger - self.start_ledger + 1
        )

    def _export_batch(self, ledger_sequence_batch: list[int]):
        for ledger_sequence in ledger_sequence_batch:
            # As we cannot get the events for a specific ledger
            # in the soroban rpc as it is returning several ledgers
            # within the limit imposed in the pagination key,
            # we need to save the events we receive in a cache so
            # if we already have this event in the cache we will not lose it,
            # and thus we optimize event requests
            events = self.service.get_events(ledger_sequence, pagination={'limit': 10000})
            for event in events:
                ledger_sequence_dict = self.ledger_events_cache.setdefault(ledger_sequence, {})
                ledger_sequence_dict[event.id] = event
                
        for ledger_sequence in ledger_sequence_batch:
            self._export_events(list(self.ledger_events_cache[ledger_sequence].values()))
            del self.ledger_events_cache[ledger_sequence] # clear the memory

    def _export_events(self, events: list[SorobanEvent]):
        for event in events:
            self.item_exporter.export_item(event.to_dict())

    def _end(self):
        del self.ledger_events_cache
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
