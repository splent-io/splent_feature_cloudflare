"""
CLI commands contributed by splent_feature_cloudflare.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:cloudflare`` group.

Usage::

    splent feature:cloudflare hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_cloudflare!")


cli_commands = [hello]
