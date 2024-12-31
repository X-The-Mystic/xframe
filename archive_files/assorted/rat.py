import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

HOST = local_ip  # replace by "127.0.0.1" if you want to use same machine

PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(2048)
            msg = data.decode()
            if msg == "exit":
                print("Bye")
                break
            print("Message received: ", msg)
            conn.sendall(data)
