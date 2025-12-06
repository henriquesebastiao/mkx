from typing import Annotated, Optional

import typer
from rich import print
from rich.console import Console

from mkx.attacks import ddos, exploit, kill_web_server
from mkx.core.settings import __version__
from mkx.discovery import mac_server_discover, snmp, upnp

app = typer.Typer(
    help='CLI for exploring IoT and network devices.',
    no_args_is_help=True,
    rich_markup_mode='rich',
)

console = Console()

app.add_typer(exploit.command, name='exploit', rich_help_panel='Exploits')
app.add_typer(
    mac_server_discover.command,
    name='mikrotik',
    rich_help_panel='OSINT - Obtaining Information',
)
app.add_typer(snmp.command, name='snmp', rich_help_panel='OSINT - Obtaining Information')
app.add_typer(upnp.command, name='upnp', rich_help_panel='OSINT - Obtaining Information')
app.add_typer(ddos.command, name='ddos', rich_help_panel='Exploits')
app.add_typer(kill_web_server.command, name='kill-web-server', rich_help_panel='Exploits')


def get_version(value: bool):
    if value:
        print(f'[bold blue]mkx[/bold blue] version: [green]{__version__}[/green]')
        print('CLI for exploring IoT and network devices.')


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


@app.command(help='Open the project repository on GitHub.', rich_help_panel='About')
def doc():
    print('Opening the mkx repository on GitHub.')
    typer.launch('https://github.com/henriquesebastiao/mkx')
