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

def up(x, y):
    x, y = x, (y-1) % 10
    print(f"Moved to ({x}, {y})")
    return (x, y)


def down(x, y):
    x, y = x, (y+1) % 10
    print(f"Moved to ({x}, {y})")
    return (x, y)


def right(x, y):
    print(x, y, (x+1)%10, y)
    x, y = (x+1)%10, y
    print(f"Moved to ({x}, {y})")
    return (x, y)

def left(x, y):
    x, y = (x-1)%10, y
    print(f"Moved to ({x}, {y})")
    return (x, y)


def addmon(name, x, y, word, mass):
    if (name not in cowsay.list_cows()) and (name != "jgsbat"):
        print("Cannot add unknown monster")
        return mass
    print(f"Added monster {name} to ({x}, {y}) saying {word}")
    if mass[x][y] != 0:
        print(f"Replaced the old monster")
    mass[x][y] = (word, name)
    return mass

def encounter(x,y, tup):
    word, name = tup
    if name == "jgsbat":
        print(cowsay.cowsay(word, cowfile=JGSBAT))
    else:
        print(cowsay.cowsay(word, cow=name))
    # cowsay.cow(word)

# поле 10 на 10
field = [[0] * 10 for _ in range(10)]
x_cur, y_cur = 0,0
flag = 1

while True:
    flag = 1
    com = input()
    com = shlex.split(com)
    if com[0] == 'up':
        x_cur, y_cur = up(x_cur, y_cur)
    elif com[0] == 'down':
        x_cur, y_cur = down(x_cur, y_cur)
    elif com[0] == 'left':
        x_cur, y_cur = left(x_cur, y_cur)
    elif com[0] == 'right':
        x_cur, y_cur = right(x_cur, y_cur)
    elif "addmon" in com:
        if len(com) != 9:
            print("Invalid arguments")
            continue
        flag = 0
        # addmon <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>
        name = com[1 + com.index('addmon')]
        word = com[1 + com.index('hello')]
        hitpoints = com[1 + com.index('hp')]
        c_id = com.index('coords')
        x, y = com[c_id + 1], com[c_id + 2]
        x, y = int(x), int(y)

        field = addmon(name, x, y, word, field)
        # print(*field)
    else:
        print("Invalid command")
    # print(flag, (field[x_cur][y_cur])
    if flag and (field[x_cur][y_cur] != 0):
        # оо.. попал
        encounter(x_cur, y_cur, field[x_cur][y_cur])
        break