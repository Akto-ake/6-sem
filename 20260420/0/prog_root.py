import shlex
from math import sqrt
import asyncio
import socket
import sys

def sqroots(coeffs: str) -> str:
    a, b, c = coeffs.split(" ")
    a, b, c = int(a), int(b), int(c)

    D = b**2 - 4 * a * c
        
    if D > 0:
        x1 = (-b - sqrt(D))/(2*a)
        x2 = (-b + sqrt(D))/(2*a)
        return ' '.join([ str(x1), str(x2) ])
        
    if D == 0:
        return str( -b/(2*a) )

    return ''

def sqrootnet(coeffs: str, s: socket.socket) -> str:
    s.sendall((coeffs + "\n").encode())
    return s.recv(128).decode().strip()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 1337))
        s.sendall(sys.argv[1].encode() + b'\n')
        print(s.recv(1024).rstrip().decode())