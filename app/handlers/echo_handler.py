from app.request import Request
from app.response import Response


def handle_echo(request: Request, client):
    parts = request.target.split("echo/")
    txt = parts[1]

    headers = {
        "Content-Type": "text/plain",
        "Content-Length": str(len(txt)),
    }
    response = Response(request.http_version, 200, "OK", headers, txt)
    client.sendall(response.to_response_bytes())
