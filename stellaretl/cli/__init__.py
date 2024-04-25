import click
from stellaretl.cli.export_events import export_events
from stellaretl.cli.export_ledgers_and_transactions import export_ledgers_and_transactions


@click.group()
def stellar():
    """All commands related with stellar-like chains."""
    pass

stellar.add_command(export_ledgers_and_transactions, "export_ledgers_and_transactions")
stellar.add_command(export_events, "export_events")