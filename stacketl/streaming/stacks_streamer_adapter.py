import logging

from stacketl.api.stack_api import StackApi
from stacketl.jobs.export_blocks_job import ExportBlocksJob
from stacketl.streaming.stacks_item_id_calculator import StackItemIdCalculator
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from typing import Optional

class StacksStreamerAdapter:
    def __init__(
            self,
            api_url: str,
            api_key: Optional[str] = None,
            item_exporter=ConsoleItemExporter(),
            batch_size=1,
            enable_blocks=True,
            enable_transactions=True,
            enable_contracts=True,
            max_workers=5,
        ):
        self.api_url = api_url
        self.stack_api = StackApi(api_url, api_key)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.enable_blocks = enable_blocks
        self.enable_transactions = enable_transactions
        self.enable_contracts = enable_contracts
        self.max_workers = max_workers
        self.item_id_calculator = StackItemIdCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return int(self.stack_api.get_latest_block().number)

    def export_all(self, start_block, end_block):
        all_items = []
        if self.enable_blocks or self.enable_transactions:
            # Export blocks and transactions
            blocks_transactions_contracts_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction', 'contract'])

            blocks_and_transactions_job = ExportBlocksJob(
                start_block=start_block,
                end_block=end_block,
                batch_size=self.batch_size,
                stack_api=self.stack_api,
                max_workers=self.max_workers,
                item_exporter=blocks_transactions_contracts_item_exporter,
                export_blocks=self.enable_blocks,
                export_transactions=self.enable_transactions,
                export_contracts=self.enable_contracts
            )
            blocks_and_transactions_job.run()

            blocks = blocks_transactions_contracts_item_exporter.get_items('block')
            transactions = blocks_transactions_contracts_item_exporter.get_items('transaction')
            contracts = blocks_transactions_contracts_item_exporter.get_items('contract')
            
            logging.info(f"Number of blocks: {len(blocks)}")
            logging.info(f"Number of transactions: {len(transactions)}")
            logging.info(f"Number of contracts: {len(contracts)}")
            
            all_items.extend(blocks)
            all_items.extend(transactions)
            all_items.extend(contracts)

        logging.info('Exporting with ' + type(self.item_exporter).__name__)

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
