import gzip

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
        # add http status line
        response = "{version} {code} {phrase}\r\n".format(version=self.http_version, code=self.status_code,
                                                          phrase=self.status_phrase)

        encoded_body = None
        if self.body is not None:
            encoded_body = self.compress_body()

        #add headers to response
        for key, value in self.headers.items():
            response += "{key}: {value}\r\n".format(key=key, value=value)
        # add end of headers delim
        response += "\r\n"

        encoded_response = response.encode()
        return encoded_response + encoded_body if encoded_body is not None else encoded_response


    def compress_body(self) -> bytes | None:
        if "Content-Encoding" in self.headers:
            compressed_bytes = gzip.compress(self.body, compresslevel=9)
            self.headers["Content-Length"] = len(compressed_bytes)
            return compressed_bytes
        else:
            return self.body


    def _set_compression_header(self):
        if self.headers is not None and "Content-Encoding" in self.headers:
            accepted_encodings = self.headers["Content-Encoding"].split(", ")
            # we only support gzip encoding for now
            if "gzip" not in accepted_encodings:
                print("we only support gzip")
                del self.headers["Content-Encoding"]
            else:
                self.headers["Content-Encoding"] = "gzip"