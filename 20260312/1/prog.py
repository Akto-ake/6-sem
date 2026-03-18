import cmd
import cowsay
import io
import shlex

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


class CMD(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.field = [[0] * 10 for _ in range(10)]
        self.x_cur = 0
        self.y_cur = 0

    def _move(self, dx, dy):
        self.x_cur = (self.x_cur + dx) % 10
        self.y_cur = (self.y_cur + dy) % 10
        print(f"Moved to ({self.x_cur}, {self.y_cur})")

        if self.field[self.x_cur][self.y_cur] != 0:
            self.encounter(self.field[self.x_cur][self.y_cur])

    def encounter(self, monster):
        word, name, hp = monster
        if name == "jgsbat":
            print(cowsay.cowsay(word, cowfile=JGSBAT))
        else:
            print(cowsay.cowsay(word, cow=name))

    def do_up(self, arg):
        """up"""
        return self._move(0, -1)

    def do_down(self, arg):
        """down"""
        return self._move(0, 1)

    def do_left(self, arg):
        """left"""
        return self._move(-1, 0)

    def do_right(self, arg):
        """right"""
        return self._move(1, 0)

    def do_addmon(self, arg):
        """
        addmon <name> hello <some words> hp <hitpoints> coords <x> <y>
        """
        com = shlex.split(arg)

        if len(com) != 9:
            print("Invalid arguments")
            return

        name = com[1 + com.index('addmon')]
        word = com[1 + com.index('hello')]
        hitpoints = com[1 + com.index('hp')]
        c_id = com.index('coords')
        x, y = com[c_id + 1], com[c_id + 2]
        x, y = int(x), int(y)

        if (name not in cowsay.list_cows()) and (name != "jgsbat"):
            print("Cannot add unknown monster")
            return

        print(f"Added monster {name} to ({x}, {y}) saying {word}")
        if self.field[x][y] != 0:
            print("Replaced the old monster")

        self.field[x][y] = (word, name, hitpoints)

    def do_EOF(self, arg):
        print()
        return 1


if __name__ == "__main__":
    CMD().cmdloop()