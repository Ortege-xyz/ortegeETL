import click

from aptosetl.jobs.export_blocks_job import ExportBlocksJob
from aptosetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from aptosetl.api.aptos_node import AptosNodeApi
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-ledger', default=0, type=int, help='Start block number')
@click.option('-e', '--end-ledger', required=True, type=int, help='End block number')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of blocks to export at a time.')
@click.option('-a', '--api-uri', default='https://fullnode.devnet.aptoslabs.com', type=str,
              help='The URI of the Aptos node api')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--blocks-output', default=None, type=str,
              help='The output file for blocks. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
def export_blocks_and_transactions(start_ledger, end_ledger, batch_size, api_uri,
                                   max_workers, blocks_output, transactions_output):
    """Export blocks and transactions."""
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksJob(
        start_block=start_ledger,
        end_block=end_ledger,
        batch_size=batch_size,
        aptos_node_api=AptosNodeApi(api_uri),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output, transactions_output),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None)
    job.run()
