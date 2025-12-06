import re
from ipaddress import IPv4Network


def get_ips(network: str) -> list[str]:
    network = [str(ip) for ip in IPv4Network('172.16.0.22', strict=False).hosts()]
    return network


def get_ips_nmap_grepable_output(path: str) -> set[str]:
    """Get IP addresses from an Nmap output file in grepable format

    Args:
        path (str): Output file path

    Returns:
        set: Set containing the found IP addresses
    """
    addresses = set()

    with open(path, 'r', encoding='utf-8') as file:
        for linha in file:
            match = re.search(r'Host: (\d+\.\d+\.\d+\.\d+)', linha)
            if match:
                ip = match.group(1)  # Extract the IP from the line
                addresses.add(ip)

    return addresses


def check_ip(ip: str) -> bool:
    """Checks if the string matches an IP address

    Args:
        ip (str): Input string

    Returns:
        bool: Boolean indicating the string is an IP or not
    """
    pattern_ip = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern_ip, ip):
        octetos = ip.split('.')
        if all(0 <= int(octeto) <= 255 for octeto in octetos):
            return True
    return False


def check_cidr(network: str) -> bool:
    """Checks if string matches a network of IP addresses

    Args:
        network (str): Input string

    Returns:
        bool: Boolean indicating the string is an network or not
    """
    pattern_cidr = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    if re.match(pattern_cidr, network):
        ip, netmask = network.split('/')
        if check_ip(ip) and 0 <= int(netmask) <= 32:
            return True
    return False
