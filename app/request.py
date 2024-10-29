class Request:
    method: str = None
    target: str = None
    http_version: str = None
    headers: dict = None
    body: bytes = None
    body_raw: str = None

    def __init__(self, method: str, target: str, http_version: str, headers: dict, body: str | None = None):
        self.method = method
        self.target = target
        self.http_version = http_version
        self.headers = headers

        if body is not None:
            self.body = body.encode()
            self.body_raw = body


def parse_incoming_request(data: bytes) -> Request:
    # GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
    data_string = data.decode("utf-8")
    method, target, http_version = _parse_request_line(data_string)
    headers = _parse_headers(data_string)
    body = _parse_request_body(data_string)

    return Request(method, target, http_version, headers, body)


def _parse_request_line(data: str) -> tuple:
    # GET /index.html HTTP/1.1\r\n
    end_of_request_line = data.find("\r\n")
    request_line = data[:end_of_request_line]
    parts = request_line.split(" ")

    return parts[0], parts[1], parts[2]


def _parse_headers(data: str) -> dict:
    # Host: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n

    headers = {}

    end_of_request_line = data.find("\r\n")
    headers_string = data[end_of_request_line + 2:]
    headers_key_values = headers_string.split("\r\n")
    for key_value in headers_key_values:
        # skip empty values, this is a parsing issue.
        if key_value == "":
            continue
        parts = key_value.split(":")
        if len(parts) != 2:
            continue  # this is likely the body so we should ignore it for now
        headers[parts[0]] = parts[1].strip()

    return headers


def _parse_request_body(data: str) -> str | None:
    end_of_headers_index = data.rfind("\r\n")
    body = data[end_of_headers_index + 2:]
    return body if body != "" else None
