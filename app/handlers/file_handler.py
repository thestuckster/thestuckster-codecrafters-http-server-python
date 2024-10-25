import os

from app.request import Request
from app.response import Response

def handle_file(request: Request, client):
    file_name = request.target.split("/files/")[1]

    response: Response | None = None
    if not _file_exists("/tmp/" + file_name):
        response = _build_not_found_response(request)
    else:
        response = _build_file_response(request, file_name)

    if response is not None:
        client.sendall(response.to_response_bytes())

def _file_exists(file_name: str) -> bool:
    return os.path.isfile(file_name)

def _build_not_found_response(request: Request) -> Response:
    return Response(request.http_version, 400, "Not Found", {}, None)


def _build_file_response(request: Request, file_name) -> Response:
    file_size = os.stat("/tmp/" + file_name).st_size

    with open("/tmp/" + file_name, "r") as f:
        data = f.read()

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Length": file_size
        }

        return Response(request.http_version, 200, "OK", headers, data)