import click

from stacketl.jobs.export_contracts_job import ExportContractsJob
from stacketl.jobs.exporters.contracts_item_exporter import contracts_item_exporter
from stacketl.api.stack_api import StackApi
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of blocks to export at a time.')
@click.option('-a', '--api-uri', default='https://api.mainnet.hiro.so/', type=str,
              help='The URI of the remote Stack api')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--contracts-output', default=None, type=str,
              help='The output file for contracts. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
def export_contracts(start_block, end_block, batch_size, api_uri,
                                   max_workers, contracts_output):
    """Export contracts."""
    if contracts_output is None:
        raise ValueError('Either --contracts_output-output option must be provided')

    job = ExportContractsJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        stack_api=ThreadLocalProxy(lambda: StackApi(api_uri)),
        max_workers=max_workers,
        item_exporter=contracts_item_exporter(contracts_output),
    )
    job.run()
