import sys
import cmd
import socket
import shlex
import readline
import threading
import time


weapons = {
    "sword": 10,
    "spear": 15,
    "axe": 20,
}


def addmon_answer(name, x, y, word, replace):
    """add and may be replace monster"""
    print(f"Added monster {name} to ({x}, {y}) saying {word}")
    if replace == "True":
        print("Replaced the old monster")


def attack_answer(name, ans, damage=None, hp=None):
    """Attack the monster if there is one"""
    if ans == "False":
        print(f"No {name} here")
        return

    print(f"Attacked {name},  damage {damage} hp")
    if hp == "0":
        print(f"{name} died")
    else:
        print(f"{name} now has {hp}")


class CMD(cmd.Cmd):
    '''a class with commands for the client'''
    prompt = "> "
    intro = "<<< Welcome to Python-MUD 0.1 >>>"

    def emptyline(self):
        '''processing an empty string'''
        pass

    def __init__(self, sock, stdin=None):
        '''initialization class with commands'''
        self.socket = sock
        self.field_size = 10
        self.waiting_answer = False
        self.closing = False
        self.last_cmd = ""
        super().__init__(stdin=stdin)

    def do_EOF(self, arg):
        """end of input processing"""
        # self.closing = True
        self.socket.shutdown(socket.SHUT_WR)
        #  иначе выводил какой то доп символ
        print()
        return 1

    def precmd(self, line):
        '''processing the last line when exiting'''
        time.sleep(1)
        self.last_cmd = line.strip()
        return line

    def do_up(self, arg):
        '''move up'''
        self.waiting_answer = True
        self.socket.sendall("move 0 -1\n".encode())

    def do_down(self, arg):
        '''move down'''
        self.waiting_answer = True
        self.socket.sendall("move 0 1\n".encode())

    def do_left(self, arg):
        '''move left'''
        self.waiting_answer = True
        self.socket.sendall("move -1 0\n".encode())

    def do_right(self, arg):
        '''move right'''
        self.waiting_answer = True
        self.socket.sendall("move 1 0\n".encode())

    def do_addmon(self, arg):
        '''add monster to x, y coords with n xp and hello words'''
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
        '''attack monster, if it is'''
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

    def do_sayall(self, arg):
        '''chattiiiiiiiiing'''
        args = shlex.split(arg)

        if len(args) != 1:
            print("Invalid arguments")
            return

        self.socket.sendall(f"sayall {shlex.quote(args[0])}\n".encode())
 
    def do_movemonsters(self, arg):
        args = shlex.split(arg)

        if len(args) != 1:
            print("Invalid arguments")
            return

        if args[0] not in ("on", "off"):
            print("Invalid arguments")
            return

        self.waiting_answer = True
        self.socket.sendall(f"movemonsters {args[0]}\n".encode())

    def do_locale(self, arg):
        args = shlex.split(arg)

        if len(args) != 1:
            print("Invalid arguments")
            return

        self.waiting_answer = True
        self.socket.sendall(f"locale {args[0]}\n".encode())

def msg_receiver(cmdline, sock):
    '''processing messages'''
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
    args = sys.argv[1:]
    cmd_file = None

    if '--file' in args:
        pos = args.index('--file')
        if pos + 1 >= len(args):
            print(f"Usage: {sys.argv[0]} username [host [port]] [--file filename]")
            sys.exit(1)
        cmd_file = args[pos + 1]
        del args[pos:pos + 2]

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} username [host [port]] [--file filename]")
        sys.exit(1)

    username = args[0]
    host = "localhost" if len(args) < 2 else args[1]
    port = 1337 if len(args) < 3 else int(args[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f"{username}\n".encode())
        response = s.recv(1024).decode()
        print(response, end="")

        if response.startswith("Hello"):
            if cmd_file is not None:
                with open(cmd_file) as file:
                    cmdline = CMD(s, stdin=file)
                    cmdline.prompt = ''
                    cmdline.use_rawinput = False
                    timer = threading.Thread(target=msg_receiver, args=(cmdline, s))
                    timer.start()
                    cmdline.cmdloop()
                    timer.join()
            else:
                cmdline = CMD(s)
                timer = threading.Thread(target=msg_receiver, args=(cmdline, s))
                timer.start()
                cmdline.cmdloop()
                timer.join()