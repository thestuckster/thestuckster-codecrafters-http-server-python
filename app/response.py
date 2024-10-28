class Response:
    http_version: str = None
    status_code: int = None
    status_phrase: str = None
    headers: dict = None
    body_raw: str = None
    body: bytes = None

    def __init__(self, http_version: str, status_code: int, status_phrase: str, headers: dict, body: str | None):
        self.http_version = http_version
        self.status_code = status_code
        self.status_phrase = status_phrase
        self.headers = headers
        self._set_compression_header()

        if body is not None:
            self.body = body.encode()
            self.body_raw = body

    def to_response_bytes(self) -> bytes:
        response = "{version} {code} {phrase}\r\n".format(version=self.http_version, code=self.status_code,
                                                          phrase=self.status_phrase)

        for key, value in self.headers.items():
            response += "{key}: {value}\r\n".format(key=key, value=value)

        # add end of request delim
        response += "\r\n"
        if self.body is not None:
            response += self.body_raw

        return response.encode()

    def _set_compression_header(self):
        if self.headers is not None and "Content-Encoding" in self.headers:
            accepted_encodings = self.headers["Content-Encoding"].split(", ")
            # we only support gzip encoding for now
            if "gzip" not in accepted_encodings:
                print("we only support gzip")
                del self.headers["Content-Encoding"]
            else:
                self.headers["Content-Encoding"] = "gzip"