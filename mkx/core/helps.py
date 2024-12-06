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
