# MKX - MikroTik Exploit

[![Build](https://github.com/henriquesebastiao/mkx/actions/workflows/build.yml/badge.svg)](https://github.com/henriquesebastiao/mkx/actions/workflows/build.yml)
[![Static Badge](https://img.shields.io/badge/status-stable-%232FBF50)](https://github.com/henriquesebastiao/mkx)
[![GitHub Release](https://img.shields.io/github/v/release/henriquesebastiao/mkx?color=blue)](https://github.com/henriquesebastiao/mkx/releases)
[![GitHub License](https://img.shields.io/github/license/henriquesebastiao/mkx?color=blue)](https://github.com/henriquesebastiao/mkx/blob/main/LICENSE)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=henriquesebastiao%2Fmkx&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/henriquesebastiao/mkx)

MKX is a tool for auditing IoT and network devices, searching for vulnerabilities and information about the target device. Originally developed to obtain information from MikroTik devices, new functionalities have been added that can be useful for analyzing a wide variety of devices and protocols.

To find vulnerabilities in MikroTik devices on the network, MKX can scan target devices using protocols such as MNDP and SNMP, seeking information about the hardware and RouterOS of the devices. The information obtained here can be of great value to anyone analyzing network security. For example, you can find out the firmware version of the device, and then search for any CVEs for this specific version. But below you will see that MKX already implements attacks from some known CVEs.

> [!WARNING]
> This vulnerability analysis script is provided "as is" and is intended solely for educational, research, and testing purposes in controlled environments with proper authorization. Before running this script, please ensure that you have the necessary permission to perform security testing on the target devices. The responsibility for using this script lies entirely with the user. The author is not responsible for any damages, losses, or legal consequences arising from improper or unauthorized use of this code.

## Features

### Obtaining Information

- Discovery of MikroTik devices on the local network through the [MikroTik Neighbor Discovery (MNDP)](https://help.mikrotik.com/docs/spaces/ROS/pages/24805517/Neighbor+discovery) protocol that runs on `UDP` port `5678`.
- Obtaining information from a specific MikroTik device or all devices in an IP range using the [SNMP](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol) protocol.
- Obtain information from devices running the [Simple Service Discovery Protocol (SSDP)](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol) and [Universal Plug and Play (UPnP)](https://en.wikipedia.org/wiki/Universal_Plug_and_Play) protocols.

### Attacks

- PoC of [CVE-2018-14847](https://nvd.nist.gov/vuln/detail/CVE-2018-14847) that allows obtaining user credentials in vulnerable versions of RouterOS.
- DDoS attack by sending packets to all ports randomly or to a specific port.
- Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 - [CVE-2023-30800](https://nvd.nist.gov/vuln/detail/CVE-2023-30800).

## Running

You can install MKX with your preferred Python package manager, here we will use [pipx](https://github.com/pypa/pipx):

```bash
pipx install mkx
```

If you don't want to install the tool on your machine, you can run a docker container with MKX already pre-installed:

```bash
docker run -it --name mkx ghcr.io/henriquesebastiao/mkx:latest
```

> [!NOTE]
> When using the docker version, if you want to run features that listen to devices on your local network, run the container with the `--network host` option.

## Getting help

Now you can run MKX and start learning how to use it. Get a list of possible commands with:

```bash
mkx --help

# Or even an explanation of a specific command or subcommand.

mkx [COMMAND] --help
```

MKX is developed using the [Typer](https://typer.tiangolo.com/) library, so you'll have a CLI that, as the Typer developers say, *"You'll love using!"* ✨.

```txt
$ poetry run mkx --help     
                                                                                
 Usage: mkx [OPTIONS] COMMAND [ARGS]...                                         
                                                                                
 Tool for auditing MikroTik routers, searching for vulnerabilities and          
 information about the target device.                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Returns the version of mkx.                  │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ About ──────────────────────────────────────────────────────────────────────╮
│ doc               Open the project repository on GitHub.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Exploits ───────────────────────────────────────────────────────────────────╮
│ exploit           Search for credentials of a RouterOS v6.42 vulnerable      │
│                   (CVE-2018-14847).                                          │
│ ddos              Perform targeted DDoS attacks on devices.                  │
│ kill-web-server   Attack that crashes the web interface of RouterOS versions │
│                   6 > 6.49.10 (CVE-2023-30800).                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ OSINT - Obtaining Information ──────────────────────────────────────────────╮
│ discover          Search for devices on the network via MikroTik Neighbor    │
│                   Discovery (MNDP).                                          │
│ snmp              Get information via SNMP from devices with default         │
│                   community (public).                                        │
│ upnp              Explore devices on the network with the Universal Plug and │
│                   Play (UPnP) port open.                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```