
#!/usr/bin/env python3
#
#  INSTALL THIS SCRIPT ON DP1 SERVER
#

import os
import iperf3
from rich.console import Console
from rich.style import Style 
from rich.text import Text
from rich import print
from rich.panel import Panel
from datetime import datetime

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def run_iperf_test(server, count, port=5201, duration=10, protocol = "tcp"):
    """
    Initiates an iperf3 client to test bandwidth to a specified server.

    Args:
        server (str): The IP address or hostname of the iperf3 server.
        port (int): The port on which the iperf3 server is listening. Default is 5201.
        duration (int): Duration of the test in seconds. Default is 10.

    Returns:
        str: A summary of the test results or an error message.
    """
    console = Console()
    test_duration = 10
    client = iperf3.Client()
    client.server_hostname = server
    client.zerocopy = True
    client.verbose = True
    client.reverse = True
    client.port = port
    client.protocol = protocol
    client.num_streams = 10
    client.duration = int(test_duration)

    message = f"\n\nTesting vmnic{count}"
    print(message)
    console.print("Processing, Please Wait....", style="bold magenta")

    result = client.run()

    if protocol == "tcp":
       sent_mbps = int(result.sent_Mbps)
       received_mbps = int(result.received_Mbps)
       rt = int(result.retransmits)
       return (f" Outgoing Traffic: {sent_mbps} Mbps, Incoming Traffic: {received_mbps} Mbps, Retransmits: {rt}")
    else:
       jitter_count = int(result.jitter_ms)
       packet_loss = int(result.lost_packets)
       return (f" Jitter: {jitter_count} ms , Lost Packets: {packet_loss}")

def main():
    console = Console()
    print('\033[?25l', end="")
    now = datetime.now()
    formatted = now.strftime("%B %d, %Y - %I:%M %p")
    servers = [
        '10.0.0.2',
        '10.0.1.2',
        '10.0.2.2',
        '10.0.3.2',
        '10.0.4.2',
        '10.0.5.2',
        '10.0.6.2',
        '10.0.7.2',
    ]
    clear_screen()
    console.print(formatted, style="bold white")
    print("\n")
    panel = Panel(Text("SPEEDTEST CONTROL PLANE 1 & 2", justify="center"), style="bold bright_blue")
    print(panel)
    panel2 = Panel(Text("TCP TEST", justify="center"), style="bold bright_yellow")
    print(panel2)
    count = 0
    for server in servers:
        result = run_iperf_test(server,count)
        print(result)
        count = count+1
    print('\n\nTest Completed !\n\n')
    console.print("To proceed to the next step, please press <ENTER>", style="blink bold green")
    input()
    clear_screen()
    now = datetime.now()
    formatted2 = now.strftime("%B %d, %Y - %I:%M %p")
    console.print(formatted2, style="bold white")
    panel3 = Panel(Text("SPEEDTEST CONTROL PLANE 1 & 2", justify="center"), style="bold bright_blue")
    print(panel3)
    panel4 = Panel(Text("UDP Test", justify="center"), style="bold bright_yellow")
    print(panel4)
    count = 0
    for server in servers:
        result = run_iperf_test(server,count,protocol="udp")
        print(result)
        count = count+1
    console.print('\n\nTest Completed !', style="blink bold green")
    input(' ')
    clear_screen()
    print('\033[?25h', end="")

if __name__ == '__main__':
    main()
