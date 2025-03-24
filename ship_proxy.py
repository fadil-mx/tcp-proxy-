import socket
import threading
import select

# Proxy Configuration
SHIP_PROXY_HOST = "0.0.0.0"  # Listen on all interfaces
SHIP_PROXY_PORT = 8080  # Ship Proxy Port
OFFSHORE_PROXY_HOST = "127.0.0.1"  # Local offshore proxy for testing
OFFSHORE_PROXY_PORT = 9090  # Offshore Proxy Port
MAX_SIZE = 4096  # Max size of the payload
RETRY_LIMIT = 3  # Number of retries for failed requests


def handle_client(client_socket):
    try:
        request = client_socket.recv(4096).decode("utf-8")
        lines = request.split("\n")
        first_line = lines[0]

        if first_line.startswith("CONNECT"):
            # Handle HTTPS CONNECT request
            try:
                host, port = first_line.split()[1].split(":")
                port = int(port) if port else 443
                print(f"[*] CONNECT request to {host}:{port}")

                # Establish connection to the target
                conn = socket.create_connection((host, port))
                client_socket.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")

                # Forward data between client and target
                sockets = [client_socket, conn]
                while True:
                    r, w, e = select.select(sockets, [], sockets, 5)
                    if e:
                        break
                    for s in r:
                        data = s.recv(4096)
                        if len(data) == 0:
                            break
                        if s is client_socket:
                            conn.sendall(data)
                        else:
                            client_socket.sendall(data)

                conn.close()
                client_socket.close()
            except Exception as e:
                print(f"[!] Error handling CONNECT: {e}")
                client_socket.close()
        else:
            # Handle HTTP request
            url = first_line.split(" ")[1]
            target_host, target_port = OFFSHORE_PROXY_HOST, OFFSHORE_PROXY_PORT
            proxy_socket = socket.create_connection((target_host, target_port))
            proxy_socket.send(request.encode("utf-8"))

            while True:
                response = proxy_socket.recv(4096)
                if len(response) == 0:
                    break
                client_socket.send(response)

            proxy_socket.close()
            client_socket.close()

    except Exception as e:
        print(f"[!] Error handling client: {e}")
        client_socket.close()


def start_proxy(ship_proxy_host, ship_proxy_port):
    # Create a socket to listen for connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ship_proxy_host, ship_proxy_port))
    server.listen(5)
    print(f"[*] Ship Proxy listening on {ship_proxy_host}:{ship_proxy_port}")

    while True:
        # Accept incoming connections
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Handle client in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_proxy(SHIP_PROXY_HOST, SHIP_PROXY_PORT)
