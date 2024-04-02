import click

from ordinalsetl.cli.stream import stream


@click.group()
@click.pass_context
def ordinals(ctx):
    """All commands related with bitcoin ordinals."""
    pass

# streaming
ordinals.add_command(stream, "stream")
