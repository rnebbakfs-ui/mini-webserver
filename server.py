# here we have socket server and request dispatch   
# miniweb/server.py
import socket
from .request import Request
from .response import Response
from .route import Router

class MiniApp:
    def __init__(self):
        self.router = Router()

    def route(self, path, methods=("GET",)):
        return self.router.add_route(path, methods)

    def handle_request(self, raw_text):
        req = Request(raw_text)
        handler = self.router.match(req.method, req.path)
        if not handler:
            return Response("404 Not Found", status=404)
        # handler may return Response or str
        result = handler(req)
        if isinstance(result, Response):
            return result
        return Response(result)

    def run(self, host="127.0.0.1", port=8080):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        print(f"MiniApp listening on http://{host}:{port}")
        try:
            while True:
                client, addr = sock.accept()
                data = b""
                # read (simple approach) — read until client closes or no more data
                client.settimeout(1.0)
                try:
                    while True:
                        chunk = client.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                        # simple optimization: if header says content-length, we could stop earlier
                except socket.timeout:
                    pass
                raw_text = data.decode(errors="ignore")
                response = self.handle_request(raw_text)
                client.sendall(response.to_bytes())
                client.close()
        except KeyboardInterrupt:
            print("Shutting down")
        finally:
            sock.close()
