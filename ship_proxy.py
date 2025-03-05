import socket


SHIP_PROXY_HOST = "0.0.0.0"
SHIP_PROXY_PORT = 8080
OFFSHORE_PROXY_HOST = "127.0.0.1"
OFFSHORE_PROXY_PORT = 9090


def start_ship_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ship_socket:
        ship_socket.bind((SHIP_PROXY_HOST, SHIP_PROXY_PORT))
        ship_socket.listen(5)
        print(f"Ship Proxy listening on port {SHIP_PROXY_PORT}...")

        offshore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        offshore_socket.connect((OFFSHORE_PROXY_HOST, OFFSHORE_PROXY_PORT))
        print("connected to offshore proxy.")

        while True:
            client_conn, _ = ship_socket.accept()
            request = client_conn.recv(4096)
            if not request:
                continue

            offshore_socket.sendall(request)

            response = offshore_socket.recv(4096)

            client_conn.sendall(response)
            client_conn.close()


start_ship_proxy()
