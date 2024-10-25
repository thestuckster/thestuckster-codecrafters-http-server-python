import socket

from app.request import parse_incoming_request
from app.request import Request
from app.handlers.echo_handler import handle_echo


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("socker created at localhost:4221")
    client, addr = server_socket.accept()  # wait for client

    # get a message from the client
    data = client.recv(4096)
    request = parse_incoming_request(data)

    # send a message to the client
    # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    route_request(request, client)


def route_request(request: Request, client):
    if "echo" in request.target:
        handle_echo(request, client)
    elif request.target != "/":
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
