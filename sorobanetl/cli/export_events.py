import click

from sorobanetl.jobs.export_events_job import ExportEventsJob
from sorobanetl.jobs.exporters.events_item_exporter import events_item_exporter
from sorobanetl.api.soroban_rpc import SorobanRpc
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-ledger', default=0, type=int, help='Start ledger sequence')
@click.option('-e', '--end-ledger', required=True, type=int, help='End ledger sequence')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of ledgers to export at a time.')
@click.option('-r', '--rpc-uri', default='https://soroban-testnet.stellar.org:443', type=str,
              help='The URI of the Soroban RPC')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--events-output', default=None, type=str,
              help='The output file for events. '
                   'If not provided ledgers will not be exported. Use "-" for stdout')
def export_events(
    start_ledger,
    end_ledger,
    batch_size,
    rpc_uri,
    max_workers,
    events_output
):
    """Export events."""
    if events_output is None:
        raise ValueError('events_output must be provided')

    job = ExportEventsJob(
        start_ledger=start_ledger,
        end_ledger=end_ledger,
        batch_size=batch_size,
        soroban_rpc=ThreadLocalProxy(lambda: SorobanRpc(rpc_uri)), # type: ignore
        max_workers=max_workers,
        item_exporter=events_item_exporter(events_output))
    job.run()
