import os

from app.request import Request
from app.response import Response

def handle_file(request: Request, client):
    file_name = request.target.split("/files/")[1]

    response: Response | None = None
    if not _file_exists(_get_relative_file_path(file_name)):
        response = _build_not_found_response(request)
    else:
        response = _build_file_response(request, file_name)

    if response is not None:
        client.sendall(response.to_response_bytes())

def _file_exists(file_name: str) -> bool:
    return os.path.isfile(file_name)

def _build_not_found_response(request: Request) -> Response:
    return Response(request.http_version, 404, "Not Found", {}, None)


def _build_file_response(request: Request, file_name) -> Response:
    path = _get_relative_file_path(file_name)
    file_size = os.stat(path).st_size

    with open(path, "r") as f:
        data = f.read()

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Length": file_size
        }

        return Response(request.http_version, 200, "OK", headers, data)


def _get_relative_file_path(file_name: str) -> str:
    return os.getcwd() + "/../tmp/" + file_name