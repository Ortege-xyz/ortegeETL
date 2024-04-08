import logging

from blockchainetl.thread_local_proxy import ThreadLocalProxy
from aptosetl.api.aptos_node import AptosNodeApi
from aptosetl.jobs.export_blocks_job import ExportBlocksJob
from sorobanetl.streaming.soroban_item_id_calculator import SorobanItemIdCalculator
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter

class AptosStreamerAdapter:
    def __init__(
            self,
            api_url: str,
            item_exporter=ConsoleItemExporter(),
            batch_size=1,
            enable_blocks=True,
            enable_transactions=True,
            max_workers=5,
        ):
        self.api_url = api_url
        self.aptos_node_api = AptosNodeApi(api_url)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.enable_blocks = enable_blocks
        self.enable_transactions = enable_transactions
        self.max_workers = max_workers
        self.item_id_calculator = SorobanItemIdCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return self.aptos_node_api.get_latest_block()

    def export_all(self, start_ledger, end_ledger):
        # Export blocks and transactions
        blocks_and_transactions_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction'])

        blocks_and_transactions_job = ExportBlocksJob(
            start_ledger=start_ledger,
            end_ledger=end_ledger,
            batch_size=self.batch_size,
            horizon_api=self.horizon_api,
            max_workers=self.max_workers,
            item_exporter=blocks_and_transactions_item_exporter,
            export_ledgers=self.enable_ledgers,
            export_transactions=self.enable_transactions,
        )
        blocks_and_transactions_job.run()

        blocks = blocks_and_transactions_item_exporter.get_items('block')
        transactions = blocks_and_transactions_item_exporter.get_items('transaction')

        logging.info(f'Exporting with {type(self.item_exporter).__name__}')

        all_items = blocks + transactions

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
