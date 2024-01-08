import click

from stacketl.jobs.export_blocks_job import ExportBlocksJob
from stacketl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from stacketl.api.stack_api import StackApi
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of blocks to export at a time.')
@click.option('-a', '--api-uri', default='https://api.testnet.hiro.so/', type=str,
              help='The URI of the remote Stack api')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--blocks-output', default=None, type=str,
              help='The output file for blocks. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
def export_blocks_and_transactions(start_block, end_block, batch_size, api_uri,
                                   max_workers, blocks_output, transactions_output):
    """Export blocks and transactions."""
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        stack_api=ThreadLocalProxy(lambda: StackApi(api_uri)),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output, transactions_output),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None)
    job.run()
