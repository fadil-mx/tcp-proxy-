import socket
import threading

# Offshore Proxy Configuration
OFFSHORE_PROXY_HOST = "0.0.0.0"  # Listen on all interfaces
OFFSHORE_PROXY_PORT = 9090  # Offshore Proxy Port
MAX_SIZE = 4096  # Maximum size of payload


def handle_client(client_socket):
    try:
        # Receive request from Ship Proxy
        request = client_socket.recv(MAX_SIZE)
        print(
            f"[*] Received request from Ship Proxy:\n{request.decode(errors='ignore')}"
        )

        # Process the request
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHeii"

        # Send response back to Ship Proxy
        client_socket.send(response)
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()


def start_offshore_proxy(host, port):
    # Create socket to listen for incoming connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Offshore Proxy listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Handle client request in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_offshore_proxy(OFFSHORE_PROXY_HOST, OFFSHORE_PROXY_PORT)
