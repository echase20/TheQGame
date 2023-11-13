from socket import socket

class Server():
    pass
def main():
    print("Server Waiting For Connection")
    client_socket, addr = server_socket.accept()
    print("client connected from", addr)

    data = client_socket.recv(1024)
    data_new = data.decode("utf-8")
    client_socket.send(bytes(output, "utf-8"))
    client_socket.close()

if __name__ == '__main__':

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", int(port)))
    server_socket.listen(1)
    main()