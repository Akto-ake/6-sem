import unittest
import multiprocessing
import socket
import time
import cowsay
from mood.server.__main__ import run_server


def recv_line(sock):
    data = ""
    while not data.endswith("\n"):
        data += sock.recv(1).decode()
    return data.rstrip("\n")

def recv_msg(sock):
    data = ""
    while not data.endswith("\0"):
        data += sock.recv(1).decode()
    return data.rstrip("\0")

class TestServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=run_server)
        cls.proc.start()
        time.sleep(1)
    
    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 1337))

        self.s.sendall("whoami\n".encode())
        self.assertEqual(recv_line(self.s), "Hello, whoami")
        self.assertEqual(recv_msg(self.s), "whoami entered the MUD")

        self.s.sendall("movemonsters off\n".encode())
        self.assertEqual(recv_msg(self.s), "Moving monsters: off")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.join()

    def tearDown(self):
        self.s.close()

    def test_addmon(self):
        self.s.sendall("addmon dragon hp 52 coords 0 1 hello hi\n".encode())

        self.assertEqual(
            recv_msg(self.s),
            "whoami added monster dragon with 52 hit points",
        )

    def test_move_to_monster(self):
        self.s.sendall("addmon dragon hp 52 coords 0 1 hello hi\n".encode())
        recv_msg(self.s)

        self.s.sendall("move 0 1\n".encode())

        self.assertEqual(
            recv_msg(self.s),
            "Moved to (0, 1)\n" + cowsay.cowsay("hi", cow="dragon"))

    def test_attack_monster(self):
        self.s.sendall("addmon dragon hp 5 coords 1 0 hello hi\n".encode())
        recv_msg(self.s)
        
        self.s.sendall("move 1 0\n".encode())
        recv_msg(self.s)
        
        self.s.sendall("attack dragon axe 20\n".encode())

        self.assertEqual(
            recv_msg(self.s),
            "whoami attacked dragon with axe, damage 5 hit points\n"
            "dragon died",
        )


if __name__ == "__main__":
    unittest.main()