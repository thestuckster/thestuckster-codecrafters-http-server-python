import socket

from app.request import parse_incoming_request
from app.request import Request


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, addr = server_socket.accept() # wait for client

    # get a message from the client
    data = client.recv(4096)
    request = parse_incoming_request(data)

    # send a message to the client
    # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    validate_route(request, client)


def validate_route(request: Request, client):
    if request.target != "/":
        client.sendAll(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    
    

if __name__ == "__main__":
    main()
