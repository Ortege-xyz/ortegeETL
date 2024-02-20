from sorobanetl.api.horizon_api import HorizonApi
from sorobanetl.domain.ledger import SorobanLedger
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range
from blockchainetl.classes.base_item_exporter import BaseItemExporter


# Exports ledgers and transactions
class ExportLedgersJob(BaseJob):
    def __init__(
            self,
            start_ledger: int,
            end_ledger: int,
            batch_size: int,
            horizon_api: HorizonApi,
            max_workers: str,
            item_exporter: BaseItemExporter,
            export_ledgers=True,
            export_transactions=True):
        validate_range(start_ledger, end_ledger)
        self.start_ledger = start_ledger
        self.end_ledger = end_ledger
        self.batch_size = batch_size

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_ledgers = export_ledgers
        self.export_transactions = export_transactions
        if not self.export_ledgers and not self.export_transactions:
            raise ValueError('At least one of export_ledgers or export_transactions must be True')

        self.horizon_api = horizon_api

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_ledger, self.end_ledger + 1),
            self._export_batch,
            total_items=self.end_ledger - self.start_ledger + 1
        )

    def _export_batch(self, ledger_number_batch: list[int]):
        ledgers = self.horizon_api.get_ledger_in_sequence(ledger_number_batch[0], ledger_number_batch[-1], min(200, self.batch_size)) # Let's assume the ledger number is in sequence, bacause of line 40, if no need to change the method

        if self.export_transactions:
            transactions = self.horizon_api.get_ledgers_transactions(ledger_number_batch)
            for ledger, ledger_transactions in zip(ledgers, transactions):
                if ledger and not ledger_transactions:
                    self._export_ledger(ledger)
                elif ledger_transactions:
                    ledger.transactions = ledger_transactions
                    self._export_ledger(ledger)
            return

        for ledger in ledgers:
            self._export_ledger(ledger)

    def _export_ledger(self, ledger: SorobanLedger):
        if self.export_ledgers:
            self.item_exporter.export_item(ledger.ledger_to_dict())
        if self.export_transactions:
            for tx in ledger.transactions:
                self.item_exporter.export_item(tx.transaction_to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
