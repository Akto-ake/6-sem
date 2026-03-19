import sys
import cmd
import io
import socket
import shlex
import cowsay
import readline

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

    def __init__(self, sock):
        self.socket = sock
        self.field_size = 10
        super().__init__()

    def do_EOF(self, arg):
        return 1

    def do_up(self, arg):
        """up"""
        self.socket.sendall(f"move 0 -1\n".encode())
        response = self.socket.recv(1024).rstrip().decode()
        move_answer(*shlex.split(response))

    def do_down(self, arg):
        """down"""
        self.socket.sendall(f"move 0 1\n".encode())
        response = self.socket.recv(1024).rstrip().decode()
        move_answer(*shlex.split(response))

    def do_left(self, arg):
        """left"""
        self.socket.sendall(f"move -1 0\n".encode())
        response = self.socket.recv(1024).rstrip().decode()
        move_answer(*shlex.split(response))

    def do_right(self, arg):
        """right"""
        self.socket.sendall(f"move 1 0\n".encode())
        response = self.socket.recv(1024).rstrip().decode()
        move_answer(*shlex.split(response))

    def do_addmon(self, arg):
        """
        addmon <name> hello <some words> hp <hitpoints> coords <x> <y>
        """
        com = shlex.split(arg)

        if len(com) != 8:
            print("Invalid arguments")
            return

        name = com[0]
        word = com[1 + com.index('hello')]
        hitpoints = com[1 + com.index('hp')]
        hitpoints = int(hitpoints)
        c_id = com.index('coords')
        x, y = com[c_id + 1], com[c_id + 2]
        x, y = int(x), int(y)

        if hitpoints <= 0:
            print("Invalid arguments")
            return

        if not (0 <= x < self.field_size and 0 <= y < self.field_size):
            print("Invalid arguments")
            return

        self.socket.sendall(f'addmon {name} hp {hitpoints} coords {x} {y} hello {word}\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        addmon_answer(*response)

    def do_attack(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print("Invalid arguments")
            return
        
        name = args[0]

        if len(args) == 1:
            damage = weapons["sword"]
        elif len(args) == 3 and args[1] == "with":
            weapon = args[2]
            if weapon not in weapons:
                print("Unknown weapon")
                return
            damage = weapons[weapon]
        else:
            print("Invalid arguments")
            return

        self.socket.sendall(f'attack {name} {damage}\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        attack_answer(name, *response)


    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line[:endidx])
        output = []
        if len(args) == 3 and (args[1] == "with"):
            for i in self.game.player.weapon:
                if i.startswith(text):
                    output.append(i)
        if len(args) == 1:
            for i in (cowsay.list_cows() + ["jgsbat"]):
                if i.startswith(text):
                    output.append(i)
        return output

if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        CMD(s).cmdloop()
