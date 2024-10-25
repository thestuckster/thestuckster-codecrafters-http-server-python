class Request:
    
    method = None
    target = None
    http_version = None
    headers = None
    
    def __init__(self, method: str, target: str, http_version: str, headers: dict):
        self.method = method
        self.target = target
        self.http_version = http_version
        self.headers = headers
        
        
    def has_header(self, key: str) -> bool:
        return self.headers is not None and key in self.headers



def parse_incoming_request(data: bytes) -> Request:
    
    # GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
    data_string = data.decode("utf-8")
    method, target, http_version = _parse_request_line(data_string)
    headers = _parse_headers(data_string)
    
    return Request(method, target, http_version, headers)
    

def _parse_request_line(data: str) -> tuple:
    #GET /index.html HTTP/1.1\r\n
    end_of_request_line = data.find("\r\n")
    request_line = data[:end_of_request_line]
    parts = request_line.split(" ")
    
    return parts[0], parts[1], parts[2]


def _parse_headers(data: str) -> dict:
    # Host: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
    
    headers = {}
    
    end_of_request_line = data.find("\r\n")
    headers_string = data[end_of_request_line:]
    headers_key_values = headers_string.split("\r\n")
    for key_value in headers_key_values:
        parts = key_value.split(":")
        headers[parts[0]] = parts[1]