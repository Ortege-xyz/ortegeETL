from aptosetl.api.aptos_node import AptosNodeApi
from aptosetl.domain.block import AptosBlock
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range
from blockchainetl.classes.base_item_exporter import BaseItemExporter

# Exports blocks and transactions
class ExportBlocksJob(BaseJob):
    def __init__(
            self,
            start_block: int,
            end_block: int,
            batch_size: int,
            aptos_node_api: AptosNodeApi,
            max_workers: int,
            item_exporter: BaseItemExporter,
            export_blocks=True,
            export_transactions=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block
        self.batch_size = batch_size

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_blocks = export_blocks
        self.export_transactions = export_transactions
        if not self.export_blocks and not self.export_transactions:
            raise ValueError('At least one of export_blocks or export_transactions must be True')

        self.aptos_node_api = aptos_node_api

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch: list[int]):
        blocks = self.aptos_node_api.get_blocks(block_number_batch, self.export_transactions)

        for block in blocks:
            self._export_block(block)

    def _export_block(self, block: AptosBlock):
        if self.export_blocks:
            self.item_exporter.export_item(block.to_dict())
        if self.export_transactions:
            for tx in block.transactions:
                self.item_exporter.export_item(tx.to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
