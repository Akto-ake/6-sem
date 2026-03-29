import sys
import cmd
import io
import socket
import shlex
import cowsay
import readline
import threading

JGSBAT = cowsay.read_dot_cow(io.StringIO(r"""
$the_cow = <<EOC;
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     \\'--'//
         (((""  "")))
EOC
"""))

weapons = {
    "sword": 10,
    "spear": 15,
    "axe": 20,
}


def move_answer(x, y, name=None, word=None):
    print(f"Moved to ({x}, {y})")

    if name:
        if name == "jgsbat":
            print(cowsay.cowsay(word, cowfile=JGSBAT))
        else:
            print(cowsay.cowsay(word, cow=name))


def addmon_answer(name, x, y, word, replace):
    print(f"Added monster {name} to ({x}, {y}) saying {word}")
    if replace == "True":
        print("Replaced the old monster")


def attack_answer(name, ans, damage=None, hp=None):
    if ans == "False":
        print(f"No {name} here")
        return

    print(f"Attacked {name},  damage {damage} hp")
    if hp == "0":
        print(f"{name} died")
    else:
        print(f"{name} now has {hp}")


class CMD(cmd.Cmd):
    prompt = "> "
    intro = "<<< Welcome to Python-MUD 0.1 >>>"

    def emptyline(self):
        pass
    
    def __init__(self, sock):
        self.socket = sock
        self.field_size = 10
        self.waiting_answer = False
        self.closing = False
        self.last_cmd = ""
        super().__init__()

    def do_EOF(self, arg):
        self.closing = True
        return 1
    
    def precmd(self, line):
        self.last_cmd = line.strip()
        return line

    def do_up(self, arg):
        self.waiting_answer = True
        self.socket.sendall("move 0 -1\n".encode())

    def do_down(self, arg):
        self.waiting_answer = True
        self.socket.sendall("move 0 1\n".encode())

    def do_left(self, arg):
        self.waiting_answer = True
        self.socket.sendall("move -1 0\n".encode())

    def do_right(self, arg):
        self.waiting_answer = True
        self.socket.sendall("move 1 0\n".encode())

    def do_addmon(self, arg):
        com = shlex.split(arg)

        if len(com) != 8:
            print("Invalid arguments")
            return

        name = com[0]
        word = com[1 + com.index('hello')]
        hitpoints = int(com[1 + com.index('hp')])
        c_id = com.index('coords')
        x, y = int(com[c_id + 1]), int(com[c_id + 2])

        if hitpoints <= 0:
            print("Invalid arguments")
            return

        if not (0 <= x < self.field_size and 0 <= y < self.field_size):
            print("Invalid arguments")
            return

        self.waiting_answer = True
        self.socket.sendall(f'addmon {name} hp {hitpoints} coords {x} {y} hello {word}\n'.encode())

    def do_attack(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print("Invalid arguments")
            return

        name = args[0]

        if len(args) == 1:
            weapon = "sword"
            damage = weapons[weapon]
        elif len(args) == 3 and args[1] == "with":
            weapon = args[2]
            if weapon not in weapons:
                print("Unknown weapon")
                return
            damage = weapons[weapon]
        else:
            print("Invalid arguments")
            return
        
        self.waiting_answer = True
        self.socket.sendall(f'attack {name} {weapon} {damage}\n'.encode())
    
def msg_receiver(cmdline, sock):
    buf = ""

    while not cmdline.closing:
        data = sock.recv(1024).decode()
        if not data:
            break

        buf += data

        while "\0" in buf:
            msg, buf = buf.split("\0", 1)
            msg = msg.rstrip("\n")

            line = readline.get_line_buffer()

            if cmdline.waiting_answer:
                restore_line = ""
                cmdline.waiting_answer = False
            elif line.strip() == cmdline.last_cmd:
                restore_line = ""
            else:
                restore_line = line

            sys.stdout.write("\r\033[2K")
            sys.stdout.write(msg)
            sys.stdout.write("\n")
            if not cmdline.closing:
                sys.stdout.write(cmdline.prompt + restore_line)
            sys.stdout.flush()
                          
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} username [host [port]]")
        sys.exit(1)

    username = sys.argv[1]
    host = "localhost" if len(sys.argv) < 3 else sys.argv[2]
    port = 1337 if len(sys.argv) < 4 else int(sys.argv[3])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f"{username}\n".encode())
        response = s.recv(1024).decode()
        print(response, end="")

        if response.startswith("Hello"):
            cmdline = CMD(s)
            timer = threading.Thread(target=msg_receiver, args=(cmdline, s), daemon=True)
            timer.start()
            cmdline.cmdloop()