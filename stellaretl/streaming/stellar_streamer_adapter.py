import logging

from blockchainetl.thread_local_proxy import ThreadLocalProxy
from stellaretl.api.horizon_api import HorizonApi
from stellaretl.api.soroban_rpc import SorobanRpc
from stellaretl.jobs.export_events_job import ExportEventsJob
from stellaretl.jobs.export_ledgers_job import ExportLedgersJob
from stellaretl.streaming.stellar_item_id_calculator import StellarItemIdCalculator
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter

class StellarStreamerAdapter:
    def __init__(
            self,
            api_url: str,
            rpc_url: str,
            item_exporter=ConsoleItemExporter(),
            batch_size=1,
            enable_ledgers=True,
            enable_transactions=True,
            enable_events=True,
            max_workers=5,
        ):
        self.api_url = api_url
        self.rpc_url = rpc_url
        self.horizon_api = HorizonApi(api_url)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.enable_ledgers = enable_ledgers
        self.enable_transactions = enable_transactions
        self.enable_events = enable_events
        self.max_workers = max_workers
        self.item_id_calculator = StellarItemIdCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return self.horizon_api.get_latest_ledger().sequence

    def export_all(self, start_ledger, end_ledger):
        # Export blocks and transactions
        ledgers_and_transactions_item_exporter = InMemoryItemExporter(item_types=['ledger', 'transaction'])

        ledgers_and_transactions_job = ExportLedgersJob(
            start_ledger=start_ledger,
            end_ledger=end_ledger,
            batch_size=self.batch_size,
            horizon_api=self.horizon_api,
            max_workers=self.max_workers,
            item_exporter=ledgers_and_transactions_item_exporter,
            export_ledgers=self.enable_ledgers,
            export_transactions=self.enable_transactions,
        )
        ledgers_and_transactions_job.run()

        events = []
        if self.enable_events:
            events_item_exporter = InMemoryItemExporter(item_types=['event'])
            events_job = ExportEventsJob(
                start_ledger=start_ledger,
                end_ledger=end_ledger,
                batch_size=self.batch_size,
                soroban_rpc=ThreadLocalProxy(lambda: SorobanRpc(self.rpc_url)), # type: ignore
                max_workers=self.max_workers,
                item_exporter=events_item_exporter
            )
            
            events_job.run()
            events = events_item_exporter.get_items('event')

        ledgers = ledgers_and_transactions_item_exporter.get_items('ledger')
        transactions = ledgers_and_transactions_item_exporter.get_items('transaction')

        logging.info('Exporting with {type(self.item_exporter).__name__}')

        all_items = ledgers + transactions + events

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
