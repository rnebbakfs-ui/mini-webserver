# Response builder helper

from http import HTTPStatus

class Response:
    # constructor:
    def __init__(self, body="", status=200, headers=None):
        self.body = body if isinstance(body, (str, bytes)) else str(body) # checks if body is either a string or byte
        self.status = status
        self.headers = headers or {} 

    def to_bytes(self):
        # Ensure body is bytes
        body_bytes = self.body.encode() if isinstance(self.body, str) else self.body # It ensures that the body is encoded in bytes
        status_line = f"HTTP/1.1 {self.status} {HTTPStatus(self.status).phrase}\r\n" # using concatenation f"...."
        
        # default headers
        final_headers = {
            "Content-Length": str(len(body_bytes)),
            "Connection": "close",
            **self.headers
        }
        # format:
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in final_headers.items())
        
        return (status_line + header_lines + "\r\n").encode() + body_bytes
         