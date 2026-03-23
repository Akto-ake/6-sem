import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer, _get_best_family
import socket

def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=ThreadingHTTPServer,
         protocol="HTTP/1.0", port=int(sys.argv[1]), bind=None):
    ServerClass.address_family, addr = _get_best_family(bind, port)
    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        hostinfo = socket.gethostbyname(socket.gethostname())
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {hostinfo} port {port} "
            f"(http://{hostinfo}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

test()