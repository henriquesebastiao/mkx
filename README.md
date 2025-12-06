# MKX - Exploration of IoT and network devices

[![Static Badge](https://img.shields.io/badge/status-stable-%232FBF50)](https://github.com/henriquesebastiao/mkx)
[![GitHub Release](https://img.shields.io/github/v/release/henriquesebastiao/mkx?color=blue)](https://github.com/henriquesebastiao/mkx/releases)
[![GitHub License](https://img.shields.io/github/license/henriquesebastiao/mkx?color=blue)](https://github.com/henriquesebastiao/mkx/blob/main/LICENSE)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=henriquesebastiao%2Fmkx&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/henriquesebastiao/mkx)

MKX is a tool for auditing IoT and network devices, searching for vulnerabilities and information about the target device. Originally developed to obtain information from MikroTik devices, new functionalities have been added that can be useful for analyzing a wide variety of devices and protocols.

To find vulnerabilities in MikroTik devices on the network, MKX can scan target devices using protocols such as MNDP and SNMP, seeking information about the hardware and RouterOS of the devices. The information obtained here can be of great value to anyone analyzing network security. For example, you can find out the firmware version of the device, and then search for any CVEs for this specific version. But below you will see that MKX already implements attacks from some known CVEs.

> [!WARNING]
> This vulnerability analysis script is provided "as is" and is intended solely for educational, research, and testing purposes in controlled environments with proper authorization. Before running this script, please ensure that you have the necessary permission to perform security testing on the target devices. The responsibility for using this script lies entirely with the user. The author is not responsible for any damages, losses, or legal consequences arising from improper or unauthorized use of this code.

## ⚡ Features

### Obtaining Information

- Discovery of MikroTik devices on the local network through the [MikroTik Neighbor Discovery (MNDP)](https://help.mikrotik.com/docs/spaces/ROS/pages/24805517/Neighbor+discovery) protocol that runs on `UDP` port `5678`.
- Obtaining information from a specific MikroTik device or all devices in an IP range using the [SNMP](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol) protocol.
- Obtain information from devices running the [Simple Service Discovery Protocol (SSDP)](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol) and [Universal Plug and Play (UPnP)](https://en.wikipedia.org/wiki/Universal_Plug_and_Play) protocols.

### Attacks

- PoC of [CVE-2018-14847](https://nvd.nist.gov/vuln/detail/CVE-2018-14847) that allows obtaining user credentials in vulnerable versions of RouterOS.
- DDoS attack by sending packets to all ports randomly or to a specific port.
- Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 - [CVE-2023-30800](https://nvd.nist.gov/vuln/detail/CVE-2023-30800).

## ✨ Running

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

## 📃 Getting help

Now you can run MKX and start learning how to use it. Get a list of possible commands with:

```bash
mkx --help

# Or even an explanation of a specific command or subcommand.

mkx [COMMAND] --help
```

MKX is developed using the [Typer](https://typer.tiangolo.com/) library, so you'll have a CLI that, as the Typer developers say, *"You'll love using!"* ✨.

### Main commands

When you run `mkx --help` you will see the main available commands separated into groups, the two main ones being:

- `Exploit` - Commands to execute specific attacks.
- `OSINT - Obtaining Information` - Commands for obtaining information about devices and services on the network.

```console
$ mkx --help
                                                                                              
 Usage: mkx [OPTIONS] COMMAND [ARGS]...                                                       
                                                                                              
 Tool for auditing MikroTik routers, searching for vulnerabilities and information about the  
 target device.                                                                               
                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Returns the version of mkx.                                │
│ --install-completion            Install completion for the current shell.                  │
│ --show-completion               Show completion for the current shell, to copy it or       │
│                                 customize the installation.                                │
│ --help                          Show this message and exit.                                │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ About ────────────────────────────────────────────────────────────────────────────────────╮
│ doc               Open the project repository on GitHub.                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Exploits ─────────────────────────────────────────────────────────────────────────────────╮
│ exploit           Search for credentials of a RouterOS v6.42 vulnerable (CVE-2018-14847).  │
│ ddos              Perform targeted DDoS attacks on devices.                                │
│ kill-web-server   Attack that crashes the web interface of RouterOS versions 6 > 6.49.10   │
│                   (CVE-2023-30800).                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ OSINT - Obtaining Information ────────────────────────────────────────────────────────────╮
│ mikrotik          Search for devices on the network via MikroTik Neighbor Discovery        │
│                   (MNDP).                                                                  │
│ snmp              Get information via SNMP from devices with default community (public).   │
│ upnp              Explore devices on the network with the Universal Plug and Play (UPnP)   │
│                   port open.                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

The mkx commands can contain subcommands; you can also use the `--help` flag to run them and get information on how to execute them.

Here are some examples of subcommand help messages:

### Command to discover information about devices on the network via SNMP

```console
$ mkx snmp --help
                                                                                              
 Usage: mkx snmp [OPTIONS] TARGET [COMMUNITY] [PORT] COMMAND [ARGS]...                        
                                                                                              
 Get information via SNMP from devices with default community (public).                       
                                                                                              
 With this command it is possible to obtain various information from MikroTik devices that    
 have a vulnerable SNMP service.                                                              
 As a target, you can pass an IP address, a network, or a grepable Nmap output file           
 containing the IP addresses to search.                                                       
                                                                                              
 You can scan port 161 on a network with Nmap and save the discovered hosts to a file with    
 the command:                                                                                 
 sudo nmap -sU -p 161 --open -oG nmap-out.txt 192.168.88.1/24                                 
                                                                                              
 Using Nmap to find hosts with vulnerable ports and then passing the file with the IPs to MKX 
 is more efficient than searching for information on all IPs on the network with mkx.         
 This way we will not try to search for information on addresses that do not have the SNMP    
 port open.                                                                                   
                                                                                              
 Examples:                                                                                    
 mkx snmp 172.16.0.1                                                                          
 mkx snmp 172.16.0.1/24 -j                                                                    
 mkx snmp 172.16.0.1/24 -s                                                                    
 mkx snmp /home/user/nmap-out.txt                                                             
                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    target         TEXT         Target IP address or network, or the path to an nmap      │
│                                  output file in grepable format, containing the target IP  │
│                                  addresses.                                                │
│                                  [required]                                                │
│      community      [COMMUNITY]  Information submission community. [default: public]       │
│      port           [PORT]       SNMP UDP port. [default: 161]                             │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --json    -j        Saves the data obtained when searching for information on a network in │
│                     a JSON file.                                                           │
│ --silent  -s        It does not perform verbose printing when searching for information on │
│                     a network, but saves a JSON file with results at the end..             │
│ --help              Show this message and exit.                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Command to perform a DDoS attack via TCP against a specific host.

```console
$ mkx ddos tcp --help
                                                                                              
 Usage: mkx ddos tcp [OPTIONS] TARGET [PORT]                                                  
                                                                                              
 Sends arbitrary packets via TCP to the device causing CPU overload.                          
                                                                                              
 You can send packets to an IP address or domain, on a specific port, or on all ports from 1  
 to 65534 randomly.                                                                           
                                                                                              
 Examples:                                                                                    
 mkx ddos tcp 192.168.88.1                                                                    
 mkx ddos tcp 192.168.88.1 -rv                                                                
 mkx ddos tcp 192.168.88.1 8080                                                               
 mkx ddos tcp server.local                                                                    
                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    target      TEXT    Target IP address or domain. [required]                           │
│      port        [PORT]  TCP port to be attacked. [default: 80]                            │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --random   -r        Attacks random ports between 1 and 65534.                             │
│ --verbose  -v        Enable verbosity.                                                     │
│ --help               Show this message and exit.                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 📜 License

MKX is open source software licensed under the [GPL-3.0](LICENSE) license.