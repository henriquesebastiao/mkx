# MKX - Mikrotik Exploit

MKX is a tool for auditing Mikrotik routers, searching for vulnerabilities and information about the target device.

## Features

### Obtaining Information

- Discovery of other Mikrotik devices on the local network through the MikroTik Neighbor Discovery protocol (MNDP) that runs on port 5678 UDP.
- Obtaining information from a specific Mikrotik device using the SNMP protocol.

### Attacks

- PoC of [CVE-2018-14847](https://nvd.nist.gov/vuln/detail/CVE-2018-14847) that allows obtaining user credentials in vulnerable versions of RouterOS.
- DDoS attack by sending packets to all ports randomly or to a specific port.
- Attack that crashes the web interface of RouterOS versions 6 > 6.49.10 - [CVE-2023-30800](https://nvd.nist.gov/vuln/detail/CVE-2023-30800).
