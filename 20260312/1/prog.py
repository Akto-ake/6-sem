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
class Monster:
    def __init__(self, name, word, hp):
        self.name = name
        self.word = word
        self.hp = hp

    def encounter(self):
        if self.name == "jgsbat":
            return cowsay.cowsay(self.word, cowfile=JGSBAT)
        return cowsay.cowsay(self.word, cow=self.name)


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, x1, y1):
        self.x = (self.x + x1) % 10
        self.y = (self.y + y1) % 10
        return self.x, self.y


class Game:
    def __init__(self):
        self.field = [[None] * 10 for _ in range(10)]
        self.player = Player()

    def move_player(self, dx, dy):
        x, y = self.player.move(dx, dy)
        output = [f"Moved to ({x}, {y})"]

        monster = self.field[x][y]
        if monster:
            output.append(monster.encounter())

        return "\n".join(output)

    def add_monster(self, name, x, y, word, hp):
        if (name not in cowsay.list_cows()) and (name != "jgsbat"):
            return "Cannot add unknown monster"

        output = [f"Added monster {name} to ({x}, {y}) saying {word}"]

        if self.field[x][y]:
            output.append("Replaced the old monster")

        self.field[x][y] = Monster(name, word, hp)
        return "\n".join(output)
    
    def attack(self):
        x = self.player.x
        y = self.player.y
        monster = self.field[x][y]

        if not monster:
            return "No monster here"

class CMD(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "> "

    def __init__(self):
        self.game = Game()
        super().__init__()

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

        print(self.game.add_monster(name, x, y, word, hitpoints))

    def do_EOF(self, arg):
        return 1


if __name__ == "__main__":
    CMD().cmdloop()