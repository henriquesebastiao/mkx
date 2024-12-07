# MKX - Mikrotik Exploit

MKX is a tool for auditing Mikrotik routers, searching for vulnerabilities and information about the target device.

To find vulnerabilities in Mikrotik devices on the network, MKX can scan target devices using protocols such as MNDP and SNMP, seeking information about the hardware and RouterOS of the devices. The information obtained here can be of great value to anyone analyzing network security. For example, you can find out the firmware version of the device, and then search for any CVEs for this specific version. But below you will see that MKX already implements attacks from some known CVEs.

> [!WARNING]
> This vulnerability analysis script is provided "as is" and is intended solely for educational, research, and testing purposes in controlled environments with proper authorization. Before running this script, please ensure that you have the necessary permission to perform security testing on the target devices. The responsibility for using this script lies entirely with the user. The author is not responsible for any damages, losses, or legal consequences arising from improper or unauthorized use of this code.

## Features

### Obtaining Information

- Discovery of Mikrotik devices on the local network through the MikroTik Neighbor Discovery (MNDP) protocol that runs on UDP port 5678.
- Obtaining information from a specific Mikrotik device or all devices in an IP range using the SNMP protocol.

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

Now you can run MKX and start learning how to use it. Get a list of possible commands with:

```bash
mkx --help

# Or even the explanation of a specific command
# mkx [COMMAND] --help
```

For detailed information on how to use the tool, see the [Wiki](https://github.com/henriquesebastiao/mkx/wiki).
