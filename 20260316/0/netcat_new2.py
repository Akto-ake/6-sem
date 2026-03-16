import sys
import socket
import cmd

class client(cmd.Cmd):
    """connect host port"""
    prompt = '>>'

    def __init__(self, socket):
        self.socket = socket
        return super().__init__()

    def do_print(self, args):
        self.socket.sendall(f"print {args}\n".encode())
        print(self.socket.recv(1024).rstrip().decode())

    def do_info(self, args):
        self.socket.sendall(f"info {args}\n".encode()) 
        print(self.socket.recv(1024).rstrip().decode())
        
    def do_EOF(self, args):
        return 1

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    client(s).cmdloop()