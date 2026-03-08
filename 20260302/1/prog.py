import cowsay

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
    if name not in cowsay.char_names:
        print("Cannot add unknown monster")
        return mass
    print(f"Added monster {name} to ({x}, {y}) saying {word}")
    if mass[x][y] != 0:
        print(f"Replaced the old monster")
    mass[x][y] = (word, name)
    return mass

def encounter(x,y, tup):
    word, name = tup
    print(cowsay.get_output_string(name, word))
    # cowsay.cow(word)

# поле 10 на 10
field = [[0] * 10 for _ in range(10)]
x_cur, y_cur = 0,0
flag = 1

while True:
    flag = 1
    com = input()
    if com == 'up':
        x_cur, y_cur = up(x_cur, y_cur)
    elif com == 'down':
        x_cur, y_cur = down(x_cur, y_cur)
    elif com == 'left':
        x_cur, y_cur = left(x_cur, y_cur)
    elif com == 'right':
        x_cur, y_cur = right(x_cur, y_cur)
    elif com.startswith("addmon "):
        com_mass = com.split()
        if len(com_mass) != 5:
            print("Invalid arguments")
            continue
        flag = 0
        name, x, y, word = com_mass[1], int(com_mass[2]), int(com_mass[3]), com_mass[4]
        field = addmon(name, x, y, word, field)
        # print(*field)
    else:
        print("Invalid command")
    # print(flag, (field[x_cur][y_cur])
    if flag and (field[x_cur][y_cur] != 0):
        # оо.. попал
        encounter(x_cur, y_cur, field[x_cur][y_cur])
        break
