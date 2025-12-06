import socket
import threading
import time
from typing import Annotated

import rich
import rich.table
import typer

from mkx.core import settings
from mkx.core.helps import MIKROTIK_DISCOVER_HELP

MAC_START = b'\x00\x01\x00\x06'
IDENTITY_START = b'\x00\x05\x00'
IDENTITY_END = b'\x00\x07\x00'
VERSION_END = b'\x00\x08\x00\x08'
SOFTWARE_ID_START = b'\x00\x0b\x00'
BOARD_START = b'\x00\x0c\x00'
BOARD_END = b'\x00\x0e\x00'
INTERFACE_START = b'\x00\x10\x00'
INTERFACE_END = b'\x00\x11\x00'

search = True

command = typer.Typer(
    help=MIKROTIK_DISCOVER_HELP,
    short_help='Search for devices on the network via MikroTik Neighbor Discovery (MNDP).',
)
console = rich.console.Console()


def discovery(sock_discovery):
    global search
    while search:
        sock_discovery.sendto(b'\x00\x00\x00\x00', ('255.255.255.255', settings.NEIGHBOR_PORT))
        time.sleep(1)


@command.callback(invoke_without_command=True)
def main(
    table: Annotated[
        bool,
        typer.Option('--table', '-t', help='Prints a table with the search results.'),
    ] = False,
):
    table_result = rich.table.Table(
        'MAC Address',
        'IP Address',
        'Identity',
        'Version',
        'Model',
        'Software ID',
        'Interface',
    )
    devices = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('0.0.0.0', settings.NEIGHBOR_PORT))

    threading.Thread(target=discovery, args=(sock,)).start()

    rich.print(
        '[bold green][[/bold green]'
        '[bold yellow]*[/bold yellow]'
        '[bold green]][/bold green]'
        ' Looking for MikroTik devices (MAC servers)\n'
    )

    global search
    while search:
        try:
            data, addr = sock.recvfrom(1024)

            # Get MAC Address
            if MAC_START in data:
                start = data.index(MAC_START) + 4
                mac = data[start : start + 6]

                if mac not in devices:
                    devices.append(mac)

                    mac_decoded = ':'.join('%02x' % b for b in mac)

                    # Get Identity of device
                    start = data.index(IDENTITY_START) + 4
                    identity = data[start : data.index(IDENTITY_END)].decode(encoding='utf-8')

                    # Get RouterOS Version
                    start = data.index(IDENTITY_END) + 4
                    version = data[start : data.index(VERSION_END)].decode(encoding='utf-8')
                    version = ' '.join(version.split()[0:2])

                    # Get Board model
                    start = data.index(BOARD_START) + 4
                    model = data[start : data.index(BOARD_END)].decode(encoding='utf-8')

                    # Get Software ID
                    start = data.index(SOFTWARE_ID_START) + 4
                    software_id = data[start : data.index(BOARD_START)].decode(encoding='utf-8')

                    # Get interface
                    start = data.index(INTERFACE_START) + 4
                    interface = data[start : data.index(INTERFACE_END)].decode(encoding='utf-8')

                    if settings.VERBOSE:
                        rich.print(
                            '[bold white][[/bold white]'
                            '[bold green]+[/bold green]'
                            '[bold white]][/bold white]',
                            end=' ',
                        )
                        rich.print(f'[bold green]{addr[0]}[/bold green]', end=' --> ')
                        print(
                            f'{mac_decoded} - {identity} - {version} - '
                            f'{model} - {software_id} - {interface}'
                        )

                    table_result.add_row(
                        mac_decoded,
                        addr[0],
                        identity,
                        version,
                        model,
                        software_id,
                        interface,
                    )

        except KeyboardInterrupt:
            search = False

            rich.print(
                '\n[bold red][[/bold red]'
                '[bold yellow]-[/bold yellow]'
                '[bold red]][/bold red]'
                ' Stopping search '
            )
            rich.print(
                '[bold green][[/bold green]'
                '[bold yellow]*[/bold yellow]'
                '[bold green]][/bold green]'
                '[bold green] Search completed with [/bold green]'
                f'[bold white]{len(devices)}[/bold white]'
                '[bold green] results[/bold green]\n'
            )

            if table:
                console.print(table_result)

            break
