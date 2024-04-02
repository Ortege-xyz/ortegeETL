import logging
import json
from ordinalsetl.rpc.ord_rpc import OrdRpc
from ordinalsetl.streaming.ord_json_transformer import OrdJsonTransformer
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


class OrdStreamerAdapter:
    def __init__(
            self,
            ord_rpc: OrdRpc,
            item_exporter=ConsoleItemExporter(),
            batch_size=2,
            max_workers=5):
        self.ord_rpc = ord_rpc
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.transformer = OrdJsonTransformer()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return int(self.ord_rpc.get_block_height())

    def export_all(self, start_block, end_block):
        for x in range(start_block, end_block + 1):
            self._export_block(x)

    def _export_block(self, block):
        logging.info('Exporting block: ' + str(block))

        json_dict = self.ord_rpc.get_inscriptions_by_block(block)
        inscriptions = json_dict.get('inscriptions')
        logging.info(inscriptions)

        for ins_id in inscriptions:
            ins_json = self.ord_rpc.get_inscription_by_id(ins_id)
            formatted = self.transformer.format_inscription(ins_json)
            self.item_exporter.export_item(formatted)

    def close(self):
        self.item_exporter.close()
