KILL_WEB_SERVER_HELP = """Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 - (CVE-2023-30800).

The web server used by MikroTik RouterOS version 6 is affected by a heap memory corruption issue.
A remote and unauthenticated attacker can corrupt the server's heap memory by sending a crafted HTTP request.
As a result, the web interface crashes and is immediately restarted.
The issue was fixed in RouterOS 6.49.10 stable.
RouterOS version 7 is not affected.

[bold green]Examples:[/bold green]
mkx kill-web-server 172.16.0.123:80
mkx kill-web-server 172.16.0.123:80,172.16.0.124:80
"""

EXPLOIT_HELP = """Search for credentials of a RouterOS v6.42 vulnerable (CVE-2018-14847).

MikroTik RouterOS through 6.42 allows unauthenticated remote attackers to read arbitrary files and remote authenticated attackers to write arbitrary files due to a directory traversal vulnerability in the WinBox interface.
This makes it possible to read arbitrary password files in plain text.

[bold green]Examples:[/bold green]
mkx exploit 192.168.88.1
mkx exploit 192.168.88.1 8295
mkx exploit server.local
"""

DDOS_TCP_HELP = """Sends arbitrary packets via TCP to the device causing CPU overload.

You can send packets to an IP address or domain, on a specific port, or on all ports from 1 to 65534 randomly.

[bold green]Examples:[/bold green]
mkx ddos tcp 192.168.88.1
mkx ddos tcp 192.168.88.1 -rv
mkx ddos tcp 192.168.88.1 8080
mkx ddos tcp server.local
"""

MIKROTIK_DISCOVER_HELP = """Search for devices on the network via MikroTik Neighbor Discovery (MNDP).

This command lists all discovered neighbours in Layer-2 broadcast domain.
It shows to which interface neighbour is connected, shows its IP/MAC addresses and several MikroTik related parameters.

It is possible to discover the following information from the found devices:
- MAC Address
- IP Address
- Device Identity
- RouterOS Version
- Device Model
- Software ID
- Interface that received the MNDP packet

[bold green]Examples:[/bold green]
mkx mikrotik
mkx mikrotik -t
"""

SNMP_HELP = """Get information via SNMP from devices with default community (public).

With this command it is possible to obtain various information from MikroTik devices that have a vulnerable SNMP service.
As a target, you can pass an IP address, a network, or a grepable Nmap output file containing the IP addresses to search.

You can scan port 161 on a network with Nmap and save the discovered hosts to a file with the command:
[bold]sudo nmap -sU -p 161 --open -oG nmap-out.txt 192.168.88.1/24[/bold]

Using Nmap to find hosts with vulnerable ports and then passing the file with the IPs to MKX is more efficient than searching for information on all IPs on the network with mkx.
This way we will not try to search for information on addresses that do not have the SNMP port open.

[bold green]Examples:[/bold green]
mkx snmp 172.16.0.1
mkx snmp 172.16.0.1/24 -j
mkx snmp 172.16.0.1/24 -s
mkx snmp /home/user/nmap-out.txt
"""

UPNP_DISCOVER_HELP = """
Search for UPnP-enabled devices on the network via SSDP (Simple Service Discovery Protocol).

This command sends a multicast M-SEARCH request to all devices in the local network
and retrieves UPnP service descriptions, control URLs and device metadata.
It allows identifying devices that expose UPnP APIs, port mappings, media services
and WPS information.

Two discovery modes are available:
- Standard Discovery: Parses raw SSDP responses manually and loads each advertised UPnP XML.
- Short Discovery: Uses the upnpy library to retrieve essential UPnP metadata more quickly.

It is possible to discover the following information from the found devices:
- Device Type
- Friendly Name
- Manufacturer & Model Information
- UPnP Service List (SCPD URL, control URL and available SOAP actions)
- Base URL of the device

When using the standard mode, XML files are fetched and parsed individually,
revealing the full API exposed by each device.

[bold green]Examples:[/bold green]
mkx upnp discover
mkx upnp discover --short
mkx upnp discover -s
"""
