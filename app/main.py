import socket
import threading

from app.handlers.file_handler import handle_file
from app.request import parse_incoming_request
from app.request import Request
from app.handlers.echo_handler import handle_echo
from app.handlers.user_agent_handler import handle_user_agent_request


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening at localhost:4221")

    while True:
        client, addr = server_socket.accept()  # wait for client
        threading.Thread(target=lambda: handle_incoming_request(client, addr)).start()


def handle_incoming_request(client, addr):
    data = client.recv(4096)
    request = parse_incoming_request(data)
    route_request(request, client)
    client.close()


def route_request(request: Request, client):
    # TODO: come up with better routing later
    if "echo" in request.target:
        handle_echo(request, client)
    elif "user-agent" in request.target:
        handle_user_agent_request(request, client)
    elif "files" in request.target:
        handle_file(request, client)
    elif request.target != "/":
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
