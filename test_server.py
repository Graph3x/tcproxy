import socket


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print(f"[*] Listening on {host}:{port}")
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client_socket)


def handle_client(client_socket):
    while True:
        data = client_socket.recv(4096)
        if not data:
            break

        print(data)
        client_socket.send(b"TEST 1\n")

        data = client_socket.recv(4096)
        if not data:
            break

        print(data)
        client_socket.send(b"FLAG{ILIKEBIGCROCODILES}\n")

        data = client_socket.recv(4096)
        if not data:
            break

        print(data)
        client_socket.send(b"asdfasdfasdfasdfasdf*!\n")

    client_socket.close()
    print("[*] Client disconnected")


def main():
    host = '127.0.0.1'
    port = 9000
    start_server(host, port)


if __name__ == '__main__':
    main()
