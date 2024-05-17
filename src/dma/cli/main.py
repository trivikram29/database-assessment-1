from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Literal

from rich import prompt
from rich.table import Table

from dma.cli._utils import RICH_CLICK_INSTALLED, console

if TYPE_CHECKING or not RICH_CLICK_INSTALLED:  # pragma: no cover
    import click
    from click import Context, group, pass_context
else:  # pragma: no cover
    import rich_click as click
    from rich.traceback import install as rich_click_traceback_install
    from rich_click import Context, group, pass_context
    from rich_click.cli import patch as rich_click_patch

    rich_click_traceback_install(suppress=["click", "rich_click", "rich"])
    rich_click_patch()
    click.rich_click.USE_RICH_MARKUP = True
    click.rich_click.USE_MARKDOWN = True
    click.rich_click.SHOW_ARGUMENTS = True
    click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
    click.rich_click.SHOW_ARGUMENTS = True
    click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
    click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
    click.rich_click.ERRORS_SUGGESTION = ""
    click.rich_click.ERRORS_EPILOGUE = ""
    click.rich_click.MAX_WIDTH = 80
    click.rich_click.SHOW_METAVARS_COLUMN = True
    click.rich_click.APPEND_METAVARS_HELP = True


__all__ = ("app",)


@group(name="DMA", context_settings={"help_option_names": ["-h", "--help"]})
@pass_context
def app(ctx: Context) -> None:
    """Database Migration Assessment"""


@app.command(
    name="collect-data",
    no_args_is_help=True,
    short_help="Collect data from a source database..",
)
@click.option(
    "--no-prompt",
    help="Do not prompt for confirmation before executing check.",
    type=bool,
    default=False,
    required=False,
    show_default=True,
    is_flag=True,
)
@click.option(
    "--db-type",
    "-db",
    help="The type of the database to connect to",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--username",
    "-u",
    help="The database user to connect as.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--password",
    "-pw",
    help="The database user password.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--hostname",
    "-h",
    help="The hostname of the database server",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--port",
    "-p",
    help="The port of the database server",
    default=None,
    type=click.INT,
    required=False,
    show_default=False,
)
@click.option(
    "--database",
    "-d",
    help="The name of the database to connect to.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--collection-identifier",
    "-id",
    help="An optional identifier used to tag the collection.  If one is not provided, the identifier will be generated from the database configuration.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
def collect_data(
    no_prompt: bool,
    db_type: Literal["mysql", "postgres", "mssql", "oracle"],
    username: str | None = None,
    password: str | None = None,
    hostname: str | None = None,
    port: int | None = None,
    database: str | None = None,
    collection_identifier: str | None = None,
) -> None:
    """Process a collection of advisor extracts."""
    from dma.collector import tasks as collector_tasks  # noqa: PLC0415

    table = Table(show_header=False)
    table.add_column("title", style="cyan", width=80)
    table.add_row("Google Database Migration Assessment")
    console.print(table)
    console.rule("Starting data collection process", align="left")

    if hostname is None:
        hostname = prompt.Prompt.ask("Please enter a hostname for the database")
    if port is None:
        port = prompt.IntPrompt.ask("Please enter a port for the database")
    if database is None:
        database = prompt.Prompt.ask("Please enter a database name")
    if username is None:
        username = prompt.Prompt.ask("Please enter a username")
    if password is None:
        password = prompt.Prompt.ask("Please enter a password", password=True)
    if no_prompt:
        input_confirmed = True
    if not no_prompt:
        input_confirmed = prompt.Confirm.ask("Are you ready to start the assessment?")
    if input_confirmed:
        asyncio.run(
            collector_tasks.readiness_check(
                console=console,
                db_type=db_type,
                username=username,
                password=password,
                hostname=hostname,
                port=port,
                database=database,
            )
        )
    else:
        console.rule("Skipping execution until input is confirmed", align="left")


@app.command(
    name="readiness-check",
    no_args_is_help=True,
    short_help="Execute the DMS migration readiness checklist.",
)
@click.option(
    "--no-prompt",
    help="Do not prompt for confirmation before executing check.",
    type=bool,
    default=False,
    required=False,
    show_default=True,
    is_flag=True,
)
@click.option(
    "--db-type",
    "-db",
    help="The type of the database to connect to",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--username",
    "-u",
    help="The database user to connect as.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--password",
    "-pw",
    help="The database user password.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--hostname",
    "-h",
    help="The hostname of the database server",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--port",
    "-p",
    help="The port of the database server",
    default=None,
    type=click.INT,
    required=False,
    show_default=False,
)
@click.option(
    "--database",
    "-d",
    help="The name of the database to connect to.",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
def readiness_check(
    no_prompt: bool,
    db_type: Literal["mysql", "postgres", "mssql", "oracle"],
    username: str | None = None,
    password: str | None = None,
    hostname: str | None = None,
    port: int | None = None,
    database: str | None = None,
) -> None:
    """Process a collection of advisor extracts."""
    from dma.collector import tasks as collector_tasks  # noqa: PLC0415

    table = Table(show_header=False)
    table.add_column("title", style="cyan", width=80)
    table.add_row("Google Database Migration Assessment")
    console.print(table)
    console.rule("Starting readiness check process", align="left")
    if hostname is None:
        hostname = prompt.Prompt.ask("Please enter a hostname for the database")
    if port is None:
        port = prompt.IntPrompt.ask("Please enter a port for the database")
    if database is None:
        database = prompt.Prompt.ask("Please enter a database name")
    if username is None:
        username = prompt.Prompt.ask("Please enter a username")
    if password is None:
        password = prompt.Prompt.ask("Please enter a password", password=True)
    if no_prompt:
        input_confirmed = True
    if not no_prompt:
        input_confirmed = prompt.Confirm.ask("Are you ready to start the assessment?")
    if input_confirmed:
        asyncio.run(collector_tasks.readiness_check(console, db_type, username, password, hostname, port, database))
    else:
        console.rule("Skipping execution until input is confirmed", align="left")

@app.command(
    name="connectivity-check",
    no_args_is_help=True,
    short_help="Execute the connectivity check from the target instance.",
)
@click.option(
    "--test-id",
    "-test",
    help="Name of the connectivity test",
    type=click.STRING,
    default=None,
    required=False,
    show_default=False,
)
@click.option(
    "--gcp-project",
    "-project",
    help="Name of the GCP project in which the connectivity test should be created",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--target-db-ip",
    help="IP address of the target DB instance to which data is migrated",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--source-db-ip",
    help="IP address of the source DB instance from which data is migrated",
    default=None,
    type=click.STRING,
    required=False,
    show_default=False,
)
@click.option(
    "--source-db-port",
    help="port on which Source DB instance listens to",
    default=None,
    type=int,
    required=False,
    show_default=False,
)
@click.option(
    "--operation-type",
    help="operation type for the connectivity test. one of create/rerun/delete",
    default="create",
    type=click.STRING,
    required=False,
    show_default=True,
)
def connectivity_check(
    operation_type: Literal["create", "rerun", "delete"],
    test_id: str | None = None,
    gcp_project: str | None = None,
    target_db_ip: str | None = None,
    source_db_ip: str | None = None,
    source_db_port: int | None = None,
) -> None:
    from dma.connectivity import tasks as connectivity_tasks

    table = Table(show_header=False)
    table.add_column("title", style="cyan", width=80)
    table.add_row("Database Connectivity Assessment")
    console.print(table)
    console.rule("Starting connectivity check", align="left")
    if test_id is None:
        test_id = prompt.Prompt.ask("Please enter a name for the connectivity test resource")
    if operation_type is None:
        operation_type = prompt.Prompt.ask("Please provide the operation type. one of create/rerun/delete")
    if gcp_project is None:
        gcp_project = prompt.IntPrompt.ask("Please enter a GCP project name in which the connectivity test will be created")
    if target_db_ip is None:
        target_db_ip = prompt.Prompt.ask("Please enter a target/destination database ip used for the migration")
    if source_db_ip is None:
        source_db_ip = prompt.Prompt.ask("Please enter the source database ip from which the data is migrated")
    if source_db_port is None:
        source_db_port = prompt.Prompt.ask("Please enter the source db port name")

    asyncio.run(connectivity_tasks.connectivity_check(console, operation_type,test_id, gcp_project, target_db_ip, source_db_ip, source_db_port))