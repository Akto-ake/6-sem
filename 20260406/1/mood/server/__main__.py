import io
import shlex
import cowsay
import asyncio
import random

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

DIRECTIONS = {
    "right": (1, 0),
    "left": (-1, 0),
    "up": (0, -1),
    "down": (0, 1),
}


class Player:
    '''class for each player'''
    def __init__(self):
        '''init player'''
        self.x = 0
        self.y = 0

    def move(self, x1, y1):
        '''move player to x, y '''
        self.x = (self.x + x1) % 10
        self.y = (self.y + y1) % 10
        return self.x, self.y


class Monster:
    '''class for each monster'''
    def __init__(self, name, word, hp):
        '''init monster'''
        self.name = name
        self.word = word
        self.hp = hp


class Game:
    '''The interaction class of players, monsters, and so on'''
    def __init__(self):
        '''make field and dict of players'''
        self.field = [[None] * 10 for _ in range(10)]
        self.players = {}

    def add_player(self, name):
        '''add player to game'''
        self.players[name] = Player()

    def remove_player(self, name):
        '''remove player from game'''
        del self.players[name]

    def move_player(self, i, x1, y1):
        '''move player to x,y'''
        x, y = self.players[i].move(x1, y1)
        monster = self.encounter[x][y]

        res = f"Moved to ({x}, {y})"
        if monster:
            if monster.name == "jgsbat":
                res += "\n" + cowsay.cowsay(monster.word, cowfile=JGSBAT)
            else:
                res += "\n" + cowsay.cowsay(monster.word, cow=monster.name)
        return res

    def addmon(self, name, x, y, hp, word):
        '''add element of class Monster'''
        replaced = self.field[x][y] is not None
        self.field[x][y] = Monster(name, word, hp)
        return replaced

    def attack(self, i, monster_name, damage):
        '''attack monster with weapon'''
        player = self.players[i]
        monster = self.field[player.x][player.y]

        if not monster or monster.name != monster_name:
            return False, 0, 0

        damage_done = min(monster.hp, damage)
        monster.hp -= damage_done
        hp_left = monster.hp

        if hp_left == 0:
            self.field[player.x][player.y] = None

        return True, damage_done, hp_left
    
    def where_monsters(self):
        '''all monsters with coordinates'''
        res = []
        for x in range(10):
            for y in range(10):
                monster = self.field[x][y]
                if monster is not None:
                    res.append((x, y, monster))
        return res

    def answer_monster(self, monster):
        '''monster words'''
        if monster.name == "jgsbat":
            return cowsay.cowsay(monster.word, cowfile=JGSBAT)
        return cowsay.cowsay(monster.word, cow=monster.name)
    
    def encounter(self, i):
        '''monster and player on the same place'''
        player = self.players[i]
        monster = self.field[player.x][player.y]

        if monster is None:
            return ""

        res = f"Moved to ({player.x}, {player.y})"
        res += "\n" + self.answer_monster(monster)
        return res
    
    def move_monster(self):
        '''move random monster to random direction'''
        monsters = self.where_monsters()
        if not monsters:
            return "", [], ""

        # check avaible move
        can_move = False
        for x, y, _ in monsters:
            for dx, dy in DIRECTIONS.values():
                new_x = (x + dx) % 10
                new_y = (y + dy) % 10
                if self.field[new_x][new_y] is None:
                    can_move = True
                    break
            if can_move:
                break

        if not can_move:
            return "", [], ""

        # now move
        while True:
            x, y, monster = random.choice(monsters)
            direction, (dx, dy) = random.choice(list(DIRECTIONS.items()))
            new_x = (x + dx) % 10
            new_y = (y + dy) % 10

            if self.field[new_x][new_y] is not None:
                continue

            self.field[x][y] = None
            self.field[new_x][new_y] = monster

            player_with_mon = []
            for i, player in self.players.items():
                if player.x == new_x and player.y == new_y:
                    player_with_mon.append(i)

            response = f"{monster.name} moved one cell {direction}"
            return response, player_with_mon, self.answer_monster(monster)



class Client:
    '''class of player'''
    def __init__(self, writer):
        '''init player'''
        self.writer = writer
        self.queue = asyncio.Queue()


clients = {}
game = Game()


async def send_msgs(me):
    '''send messages from client'''
    while True:
        msg = await me.queue.get()
        me.writer.write((msg + "\0").encode())
        await me.writer.drain()


async def broadcast(msg, skip=None):
    '''sending messages to everyone'''
    for name, client in clients.items():
        if name != skip:
            await client.queue.put(msg)


async def wandering_monsters():
    '''move random monsters every 30 seconds'''
    while True:
        await asyncio.sleep(30)

        response, player_with_mon, mon_ans = game.move_monster()
        player_msg = {}
        for i in player_with_mon:
            if i in game.players:
                player = game.players[i]
                player_msg[i] = (f"Moved to ({player.x}, {player.y})\n{mon_ans}")

        if response:
            await broadcast(response)
            for i, msg in player_msg.items():
                if i in clients:
                    await clients[i].queue.put(msg)


async def echo_client(reader, writer):
    '''connecting the client'''
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

    me = Client(writer)
    clients[name] = me
    game.add_player(name)

    print(f"Connected: {addr} as {name}")

    writer.write(f"Hello, {name}\n".encode())
    await writer.drain()

    sender = asyncio.create_task(send_msgs(me))
    await broadcast(f"{name} entered the MUD")

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
            await me.queue.put(response)

        elif cmd == "addmon":
            mon_name = args[1]
            word = args[1 + args.index("hello")]
            hitpoints = int(args[1 + args.index("hp")])
            c_id = args.index("coords")
            x = int(args[c_id + 1])
            y = int(args[c_id + 2])

            replaced = game.addmon(mon_name, x, y, hitpoints, word)

            response = f"{name} added monster {mon_name} with {hitpoints} hp"
            if replaced:
                response += "\nReplaced the old monster"

            await broadcast(response)

        elif cmd == "attack":
            mon_name = args[1]
            weapon = args[2]
            damage = int(args[3])

            ok, damage_done, hp_left = game.attack(name, mon_name, damage)

            if not ok:
                await me.queue.put(f"No {mon_name} here")
                continue

            response = (
                f"{name} attacked {mon_name} with {weapon}, "
                f"damage {damage_done} hp"
            )
            if hp_left == 0:
                response += f"\n{mon_name} died"
            else:
                response += f"\n{mon_name} now has {hp_left} hp"

            await broadcast(response)

        elif cmd == "sayall":
            msg = args[1]
            await broadcast(f"{name}: {msg}")

        else:
            await me.queue.put("Invalid command")

    print(f"Disconnected: {addr} as {name}")
    del clients[name]
    game.remove_player(name)
    await broadcast(f"{name} left the MUD")
    sender.cancel()
    writer.close()
    await writer.wait_closed()


async def main():
    '''main'''
    server = await asyncio.start_server(echo_client, "0.0.0.0", 1337)
    mover = asyncio.create_task(wandering_monsters())
    
    try:
        async with server:
            await server.serve_forever()
    finally:
        mover.cancel()


if __name__ == "__main__":
    asyncio.run(main())
