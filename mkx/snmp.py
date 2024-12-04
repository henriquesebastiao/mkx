import asyncio
import sys
from typing import Annotated

import rich
import typer
from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)


def fmemory(value) -> str:
    mb = round(int(value) / 1024, 2)
    if mb >= 1024:
        return f'{round(mb / 1024, 2)} GB'
    return f'{mb} MB'


def ffrequency(value) -> str:
    mb = round(int(value), 2)
    if mb >= 1000:
        return f'{round(mb / 1000, 2)} GHz'
    return f'{mb} MHz'


def fcpuload(value) -> str:
    return f'{value}%'


def fvoltage(value) -> str:
    return f'{round(int(value) / 10, 1)} V'


def ftemperature(value) -> str:
    return f'{value} °C'


def fnote(value) -> str:
    if value[:2] != '0x':
        return value
    return bytes.fromhex(value[2:]).decode('utf-8')


SNMP_ITENS = [
    ['Identity', '.1.3.6.1.2.1.1.5.0', None],
    ['Model', '.1.3.6.1.2.1.1.1.0', None],
    ['Total Memory', '.1.3.6.1.2.1.25.2.3.1.5.65536', fmemory],
    ['CPU', '.1.3.6.1.2.1.47.1.1.1.1.7.65536', None],
    ['CPU Frequency', '.1.3.6.1.4.1.14988.1.1.3.14.0', ffrequency],
    ['CPU Load', '.1.3.6.1.2.1.25.3.3.1.2.1', fcpuload],
    ['USB', '.1.3.6.1.2.1.47.1.1.1.1.2.262145', None],
    ['Voltage', '.1.3.6.1.4.1.14988.1.1.3.100.1.3.13', fvoltage],
    ['Temperature', '.1.3.6.1.4.1.14988.1.1.3.100.1.3.14', ftemperature],
    ['Software ID', '.1.3.6.1.4.1.14988.1.1.4.1.0', None],
    ['License Level', '.1.3.6.1.4.1.14988.1.1.4.3.0', None],
    ['Note', '.1.3.6.1.4.1.14988.1.1.7.5.0', fnote],
]


async def snmp(oid: str, ip_address: str, snmp_community: str, snmp_port: int):
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        CommunityData(snmp_community, mpModel=0),
        await UdpTransportTarget.create((ip_address, snmp_port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    _, _, _, varBinds = await iterator

    snmpEngine.close_dispatcher()
    if len(varBinds) == 0:
        rich.print(
            '[bold red][[/bold red]'
            '[bold yellow]-[/bold yellow]'
            '[bold red]][/bold red]'
            ' [bold red]The SNMP port used for [/bold red]'
            f'[bold white]{ip_address}[/bold white]'
            ' [bold red]appears to not be open![/bold red] '
        )
        rich.print(
            '[bold red][[/bold red]'
            '[bold yellow]-[/bold yellow]'
            '[bold red]][/bold red]'
            ' Check if the port is open by running: '
            '[bold white]sudo nmap -sU -p PORT'
            f' {ip_address}[/bold white]'
        )
        sys.exit(1)
    return str(varBinds[0]).split('=')[1].strip()


command = typer.Typer(
    help='Get information via SNMP from Mikrotik '
    'devices with default community (public).',
    no_args_is_help=True,
)


@command.callback(invoke_without_command=True)
def main(
    target: Annotated[str, typer.Argument(help='Target IP address.')],
    community: Annotated[
        str, typer.Argument(help='Information submission community.')
    ] = 'public',
    port: Annotated[int, typer.Argument(help='SNMP UDP port.')] = 161,
):
    rich.print(
        '[bold green][[/bold green]'
        '[bold yellow]*[/bold yellow]'
        '[bold green]][/bold green]'
        ' Searching for information via SNMP from '
        f'[bold white]{target}[/bold white]:\n'
    )

    for item in SNMP_ITENS:
        result = asyncio.run(snmp(item[1], target, community, port))
        if 'No Such Object currently exists at this OID' in result:
            continue

        if item[2] is None:
            formatted_result = result
        else:
            formatted_result = item[2](result)

        rich.print(
            '[bold white][[/bold white]'
            '[bold green]+[/bold green]'
            '[bold white]][/bold white]'
            f'[bold green] {item[0]}:[/bold green]',
            end=' ',
        )
        print(formatted_result)
