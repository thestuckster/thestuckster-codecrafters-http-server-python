from socket import socket

from app.request import Request
from app.response import Response


def handle_echo(request: Request, client: socket):
    parts = request.target.split("echo/")
    txt = parts[1]

    headers = {
        "Content-Type": "text/plain",
        "Content-Length": str(len(txt)),
    }

    if "Accept-Encoding" in request.headers:
        headers["Content-Encoding"] = request.headers["Accept-Encoding"]

    response = Response(request.http_version, 200, "OK", headers, txt)
    client.send(response.to_response_bytes())
