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


def addmon(x, y, word, mass):
    print(f"Added monster to ({x}, {y}) saying {word}")
    if mass[x][y] != 0:
        print(f"Replaced the old monster")
    mass[x][y] = word
    return mass

def encounter(x,y, word):
    cowsay.cow(word)

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
        if len(com_mass) != 4:
            print("Invalid arguments")
            continue
        flag = 0
        x, y, word = int(com_mass[1]), int(com_mass[2]), com_mass[3]
        field = addmon(x, y, word, field)
        # print(*field)
    else:
        print("Invalid command")
    # print(flag, (field[x_cur][y_cur])
    if flag and (field[x_cur][y_cur] != 0):
        # оо.. попал
        encounter(x_cur, y_cur, field[x_cur][y_cur])
        break
