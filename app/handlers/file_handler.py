import os
import sys

from app.request import Request
from app.response import Response


def handle_file(request: Request, client):
    if request.method == 'GET':
        _get_file(request, client)
    elif request.method == 'POST':
        _create_file(request, client)


def _get_file(request: Request, client):
    file_name = request.target.split("/files/")[1]

    response: Response | None = None
    if not _file_exists(_get_relative_file_path(file_name)):
        response = _build_not_found_response(request)
    else:
        response = _build_file_response(request, file_name)

    if response is not None:
        client.sendall(response.to_response_bytes())


def _create_file(request: Request, client):
    path = _get_relative_file_path(request.target.split("/files/")[1])
    with open(path, "wb") as file:
        file.write(request.body)

    file_size = os.stat(path).st_size
    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Length": file_size,
    }
    client.sendall(Response(request.http_version, 201, "Created", headers, None).to_response_bytes())


def _file_exists(file_name: str) -> bool:
    exists = os.path.isfile(file_name)
    print("Able to find file {file_name}? - {exists}".format(file_name=file_name, exists=exists))
    return exists


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


def _get_file_directory():
    return sys.argv[2]


def _get_relative_file_path(file_name: str) -> str:
    return _get_file_directory() + "/" + file_name
