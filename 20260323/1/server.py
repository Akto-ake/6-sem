import sys
import cmd
import io
import socket
import shlex
import cowsay
import readline
import asyncio


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, x1, y1):
        self.x = (self.x + x1) % 10
        self.y = (self.y + y1) % 10
        return self.x, self.y


class Monster:
    def __init__(self, name, word, hp):
        self.name = name
        self.word = word
        self.hp = hp


class Game:
    def __init__(self):
        self.field = [[None] * 10 for _ in range(10)]
        self.players = {}

    def add_player(self, name):
        self.players[name] = Player()

    def remove_player(self, name):
        del self.players[name]

    def move_player(self, name, x1, y1):
        x, y = self.players[name].move(x1, y1)
        monster = self.field[x][y]

        if not monster:
            return shlex.join([str(x), str(y)])
        return shlex.join([str(x), str(y), monster.name, monster.word])

    def addmon(self, name, x, y, hp, word):
        replaced = "False"
        if self.field[x][y]:
            replaced = "True"

        self.field[x][y] = Monster(name, word, hp)
        return shlex.join([name, str(x), str(y), word, replaced])

    def attack(self, player_name, name, damage):
        player = self.players[player_name]
        monster = self.field[player.x][player.y]

        if not monster or monster.name != name:
            return "False"

        damage_res = min(monster.hp, damage)
        monster.hp -= damage_res

        if monster.hp == 0:
            self.field[player.x][player.y] = None

        return shlex.join(["True", str(damage_res), str(monster.hp)])


clients = {}
game = Game()


async def echo_client(reader, writer):
    addr = writer.get_extra_info("peername")

    data = await reader.readline()
    if not data:
        writer.close()
        await writer.wait_closed()
        return

    name = data.decode().rstrip("\n")

    if name in clients:
        writer.write("Username is already taken\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    clients[name] = writer
    game.add_player(name)

    print(f"Connected: {addr} as {name}")
    writer.write(f"Hello, {name}\n".encode())
    await writer.drain()

    while not reader.at_eof():
        data = await reader.readline()
        if not data:
            break

        args = shlex.split(data.decode().rstrip("\n"))
        if not args:
            continue

        cmd = args[0]

        if cmd == "move":
            x1, y1 = int(args[1]), int(args[2])
            response = game.move_player(name, x1, y1)

        elif cmd == "addmon":
            mon_name = args[1]
            word = args[1 + args.index('hello')]
            hitpoints = args[1 + args.index('hp')]
            hitpoints = int(hitpoints)
            c_id = args.index('coords')
            x, y = args[c_id + 1], args[c_id + 2]
            x, y = int(x), int(y)

            response = game.addmon(mon_name, x, y, hitpoints, word)

        elif cmd == "attack":
            mon_name, damage = args[1], args[2]
            response = game.attack(name, mon_name, int(damage))

        else:
            response = "Invalid command"

        writer.write((response + "\n").encode())
        await writer.drain()

    print(f"Disconnected: {addr} as {name}")
    del clients[name]
    game.remove_player(name)
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo_client, "0.0.0.0", 1337)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
