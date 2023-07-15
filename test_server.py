import socket


def start_server(host, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the host and port
        server_socket.bind((host, port))
    except socket.error as e:
        print(f"[!!] Failed to bind on {host}:{port}")
        print(f"[!!] Error: {e}")
        return

    print(f"[*] Listening on {host}:{port}")

    # Start listening for incoming connections
    server_socket.listen(5)

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Handle the client connection in a separate thread
        handle_client(client_socket)


def handle_client(client_socket):
    # Receive and send data in a loop until the client disconnects
    while True:
        # Receive data from the client
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

    # Close the client socket
    client_socket.close()
    print("[*] Client disconnected")


def main():
    host = '127.0.0.1'
    port = 9000
    start_server(host, port)


if __name__ == '__main__':
    main()
