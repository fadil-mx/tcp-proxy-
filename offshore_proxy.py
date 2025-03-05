import socket
import requests

OFFSHORE_PROXY_HOST = "0.0.0.0"
OFFSHORE_PROXY_PORT = 9090


def start_offshore_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as offshore_socket:
        offshore_socket.bind((OFFSHORE_PROXY_HOST, OFFSHORE_PROXY_PORT))
        offshore_socket.listen(5)
        print(f"offshore Proxy listening on port {OFFSHORE_PROXY_PORT}")

        while True:
            ship_conn, _ = offshore_socket.accept()
            request = ship_conn.recv(4096)
            if not request:
                continue

            url = request.decode().split("\r\n")[0].split(" ")[1]
            print(f"fetching {url} from the internet...")

            response = requests.get(url)
            ship_conn.sendall(response.content)
            ship_conn.close()


start_offshore_proxy()
