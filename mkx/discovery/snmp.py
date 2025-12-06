import asyncio
import json as json_m
import os
import sys
from datetime import datetime
from ipaddress import IPv4Network
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

from mkx.core.helps import SNMP_HELP
from mkx.core.network import check_cidr, check_ip, get_ips_nmap_grepable_output


def fint(value):
    return int(value)


def fmemory(value):
    mb = round(int(value) / 1024, 2)
    if mb >= 1024:
        return f'{round(mb / 1024, 2)} GB'
    return f'{mb} MB', int(value)


def ffrequency(value):
    mb = round(int(value), 2)
    if mb >= 1000:
        return f'{round(mb / 1000, 2)} GHz'
    return f'{mb} MHz', int(value)


def fcpuload(value) -> str:
    return f'{value}%', int(value)


def fvoltage(value) -> str:
    voltage = round(int(value) / 10, 1)
    return f'{voltage} V', voltage


def ftemperature(value) -> str:
    return f'{value} °C', int(value)


def fnote(value) -> str:
    if value[:2] != '0x':
        return value
    return bytes.fromhex(value[2:]).decode('utf-8')


def save_snmp(data: dict) -> str:
    now = datetime.now()
    file_name = f'mkx-snmp-{now.strftime("%Y%m%d_%H%M%S")}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json_m.dump(data, file, indent=4)
    return file_name


SNMP_ITENS = [
    ['Identity', '.1.3.6.1.2.1.1.5.0', None],
    ['RouterOS Version', '.1.3.6.1.4.1.14988.1.1.4.4.0', None],
    ['Model', '.1.3.6.1.4.1.14988.1.1.7.9.0', None],
    ['Board Name', '.1.3.6.1.4.1.14988.1.1.7.8.0', None],
    ['License Level', '.1.3.6.1.4.1.14988.1.1.4.3.0', fint],
    ['Software ID', '.1.3.6.1.4.1.14988.1.1.4.1.0', None],
    ['Serial Number', '.1.3.6.1.4.1.14988.1.1.7.3.0', None],
    ['Build Time', '.1.3.6.1.4.1.14988.1.1.7.6.0', None],
    ['Uptime', '.1.3.6.1.2.1.1.3.0', fint],
    ['Total Memory', '.1.3.6.1.2.1.25.2.3.1.5.65536', fmemory],
    ['CPU', '.1.3.6.1.2.1.47.1.1.1.1.7.65536', None],
    ['CPU Frequency', '.1.3.6.1.4.1.14988.1.1.3.14.0', ffrequency],
    ['CPU Load', '.1.3.6.1.2.1.25.3.3.1.2.1', fcpuload],
    ['USB', '.1.3.6.1.2.1.47.1.1.1.1.2.262145', None],
    ['Voltage', '.1.3.6.1.4.1.14988.1.1.3.100.1.3.13', fvoltage],
    ['Temperature', '.1.3.6.1.4.1.14988.1.1.3.100.1.3.14', ftemperature],
    ['Note', '.1.3.6.1.4.1.14988.1.1.7.5.0', fnote],
]


async def snmp(
    oid: str,
    ip_address: str,
    snmp_community: str,
    snmp_port: int,
    network: bool = False,
):
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
        if not network:
            rich.print(
                '[bold red][[/bold red]'
                '[bold yellow]-[/bold yellow]'
                '[bold red]][/bold red]'
                ' [bold red]The SNMP port used for [/bold red]'
                f'[bold white]{ip_address}[/bold white]'
                ' [bold red]appears to not be open or the '
                'community is wrong![/bold red] '
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
        else:
            rich.print(
                '[bold red][[/bold red]'
                '[bold yellow]-[/bold yellow]'
                '[bold red]][/bold red]'
                ' [bold red]The SNMP port used for [/bold red]'
                f'[bold white]{ip_address}[/bold white]'
                ' [bold red]appears to not be open or '
                'the community is wrong! - UNSUCCESSFUL[/bold red] '
            )
        return None
    return str(varBinds[0]).split('=')[1].strip()


command = typer.Typer(
    help=SNMP_HELP,
    short_help='Get information via SNMP from devices with default community (public).',
    no_args_is_help=True,
)


@command.callback(invoke_without_command=True)
def main(
    target: Annotated[
        str,
        typer.Argument(
            help='Target IP address or network, or the path to an nmap '
            'output file in grepable format, '
            'containing the target IP addresses.'
        ),
    ],
    community: Annotated[str, typer.Argument(help='Information submission community.')] = 'public',
    port: Annotated[int, typer.Argument(help='SNMP UDP port.')] = 161,
    json: Annotated[
        bool,
        typer.Option(
            '--json',
            '-j',
            help='Saves the data obtained when searching'
            ' for information on a network in a JSON file.',
        ),
    ] = False,
    silent: Annotated[
        bool,
        typer.Option(
            '--silent',
            '-s',
            help='It does not perform verbose printing when searching'
            ' for information on a network, but saves a'
            ' JSON file with results at the end..',
        ),
    ] = False,
):
    if check_ip(target):
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
    else:
        network = []

        if check_cidr(target):
            network = [str(ip) for ip in IPv4Network(target, strict=False).hosts()]
        elif os.path.isfile(target):
            network = list(get_ips_nmap_grepable_output(target))
        else:
            rich.print(
                '[bold red][[/bold red]'
                '[bold yellow]*[/bold yellow]'
                '[bold red]][/bold red]'
                ' You have entered an [bold red]invalid[/bold red] target.'
            )
            rich.print(
                '[bold red][[/bold red]'
                '[bold yellow]*[/bold yellow]'
                '[bold red]][/bold red]'
                ' You should enter an IP address, network '
                'or the path to an nmap output file in grepable format.'
            )
            rich.print(
                '[bold red][[/bold red]'
                '[bold yellow]*[/bold yellow]'
                '[bold red]][/bold red]'
                ' Run [bold white]mkx snmp '
                '--help[/bold white] for more information.'
            )
            typer.Exit(1)

        output = dict()

        if silent:
            rich.print(
                '[bold green][[/bold green]'
                '[bold yellow]*[/bold yellow]'
                '[bold green]][/bold green]'
                ' Searching for SNMP information on the network '
                f'[bold white]{target}[/bold white]'
            )

        try:
            for address in network:
                if not silent:
                    rich.print(
                        '[bold green][[/bold green]'
                        '[bold yellow]*[/bold yellow]'
                        '[bold green]][/bold green]'
                        ' Searching for information via SNMP from '
                        f'[bold white]{address}[/bold white]:'
                    )

                output[address] = dict()

                for item in SNMP_ITENS:
                    result = asyncio.run(
                        snmp(
                            item[1],
                            address,
                            community,
                            port,
                            network=True,
                        )
                    )

                    if result is None:
                        output[address] = None
                        break
                    if 'No Such Object currently exists at this OID' in result:
                        continue
                    if item[2] is None:
                        formatted_result = result
                    else:
                        formatted_result = item[2](result)

                    human_readable_result = formatted_result

                    if isinstance(formatted_result, tuple):
                        human_readable_result = formatted_result[0]
                        formatted_result = formatted_result[1]

                    output[address][item[0]] = formatted_result

                    if not silent:
                        rich.print(
                            '[bold white][[/bold white]'
                            '[bold green]+[/bold green]'
                            '[bold white]][/bold white]'
                            f'[bold green] {item[0]}:[/bold green]',
                            end=' ',
                        )
                        print(human_readable_result)
                if not silent:
                    print()
            if json or silent:
                file = save_snmp(output)
                if silent:
                    rich.print(
                        '[bold green][[/bold green]'
                        '[bold yellow]+[/bold yellow]'
                        '[bold green]][/bold green]'
                        ' Search completed'
                    )
                rich.print(
                    '[bold green][[/bold green]'
                    '[bold yellow]+[/bold yellow]'
                    '[bold green]][/bold green]'
                    f' Result saved in [yellow]{file}[/yellow]'
                )
        except KeyboardInterrupt:
            rich.print(
                '\n[bold red][[/bold red]'
                '[bold yellow]-[/bold yellow]'
                '[bold red]][/bold red]'
                ' Search interrupted by user'
            )
            if json or silent:
                file = save_snmp(output)
                rich.print(
                    '[bold green][[/bold green]'
                    '[bold yellow]+[/bold yellow]'
                    '[bold green]][/bold green]'
                    f' Result saved in [yellow]{file}[/yellow]'
                )
                typer.Exit(1)
