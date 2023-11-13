import json
from socket import socket





def send_json_message(
    sock: socket.socket,
    json_message: Dict[str, Any],
) -> None:
    """Send json packet to server"""
    message = (json.dumps(json_message) + '\n').encode()
    sock.sendall(message)
    print(f'{len(message)} bytes sent')
def main() -> None:
    with socket.socket() as sock:
        sock.connect((IP, PORT))
        json_message = {"a":2,"b":"count"}#[2,[[["a"]]],2,"b"] #generate_json_message
        send_json_message(sock, json_message)
        data = sock.recv(1024)
        print(str(data))
        sleep(1)