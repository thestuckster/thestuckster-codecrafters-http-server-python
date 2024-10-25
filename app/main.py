import socket
import threading

from app.request import parse_incoming_request
from app.request import Request
from app.handlers.echo_handler import handle_echo
from app.handlers.user_agent_handler import handle_user_agent_request

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("socker created at localhost:4221")

    while True:
        client, addr = server_socket.accept()  # wait for client
        threading.Thread(target=lambda: handle_incoming_request(client, addr)).start()
        # # get a message from the client
        # data = client.recv(4096)
        # request = parse_incoming_request(data)
        #
        # # send a message to the client
        # # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        # route_request(request, client)


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
    elif request.target != "/":
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
