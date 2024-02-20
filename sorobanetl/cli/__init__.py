import click
from sorobanetl.cli.export_ledgers_and_transactions import export_ledgers_and_transactions


@click.group()
def soroban():
    """All commands related with stack-like chains."""
    pass

soroban.add_command(export_ledgers_and_transactions, "export_ledgers_and_transactions")