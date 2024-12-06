from typing import Annotated, Optional

import typer
from rich import print
from rich.console import Console

from mkx import ddos, exploit, kill_web_server, mac_server_discover, snmp
from mkx.core.settings import __version__

app = typer.Typer(
    help='Scripts for auditing Mikrotik routers.',
    no_args_is_help=True,
    rich_markup_mode='rich',
)

console = Console()

app.add_typer(exploit.command, name='exploit', rich_help_panel='Attacks')
app.add_typer(
    mac_server_discover.command,
    name='discover',
    rich_help_panel='Obtaining Information',
)
app.add_typer(
    snmp.command, name='snmp', rich_help_panel='Obtaining Information'
)
app.add_typer(ddos.command, name='ddos', rich_help_panel='Attacks')
app.add_typer(
    kill_web_server.command, name='kill-web-server', rich_help_panel='Attacks'
)


def get_version(value: bool):
    if value:
        print(
            f'[bold blue]mkx[/bold blue] version: [green]{__version__}[/green]'
        )
        print('Scripts for auditing Mikrotik routers.')


@app.callback(
    invoke_without_command=True,
)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option(
            '--version',
            '-v',
            callback=get_version,
            help='Returns the version of mkx.',
        ),
    ] = None,
): ...


@app.command(
    help='Open the project repository on GitHub.', rich_help_panel='About'
)
def doc():
    print('Opening the mkx repository on GitHub.')
    typer.launch('https://github.com/henriquesebastiao/mkx')
