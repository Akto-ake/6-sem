import sys
import zlib
import glob
import os
from pathlib import Path

# Первый параметр — путь к каталогу с репозиторием.
# Без других параметров программа выводит имена всех веток;
# дальнейшие требования относятся к запуску программы со вторым параметром — именем ветки.
# master
# lomaster

def names_br(path):
    br = []
    for i in glob.glob(path + "/.git/refs/heads/*"):
        br.append(os.path.basename(i))
    return '\n'.join(br)

# Вывести объект-последний коммит (последний коммит указанной ветки).
# tree 3182cbd0e8b2baecbdc693008ed832b25546e225
# parent f97190bd4dea21041d1cd7fcf822cd4ac6e7716b
# author Ivan Samovarov <isamovarov@mail.ru>
# committer Elec Tropoezd <elec@tropoe.zd>

# Added a very important feature.

def last_comm(path, name_br):
    id = id_comm(path, name_br)

    ob = f'{path}/.git/objects/{id[:2]}/{id[2:]}'

    with open(ob, "rb") as f:
        ob = zlib.decompress(f.read())
    
    _, _, body = ob.partition(b'\x00')
    return body.decode()

# Вывести объект-дерево, на который указывает последний коммит ветки (поддеревья обрабатывать не нужно).
# blob cf1ab25da0349f84a3fdd40032f0ce99db813b8b    LICENSE
# blob f99151731324e7ac98281272c68f2b599dbf868d    Makefile
# tree b6e86ab64d77628cff4cfcaaf9133533733f8553    Tests

def show_tree(path, name_br):
    id = id_comm(path, name_br)
    sha_len = len(id) // 2
    ob = f'{path}/.git/objects/{id[:2]}/{id[2:]}'
    with open(ob, "rb") as f:
        ob = zlib.decompress(f.read())
    head, _, body = ob.partition(b'\x00')

    for stroka in body.decode().split('\n'):
        if stroka.startswith('tree'):
            new_id = stroka.split()[1]
            break
    
    new_ob = f'{path}/.git/objects/{new_id[:2]}/{new_id[2:]}'
    with open(new_ob, "rb") as f:
        new_ob = zlib.decompress(f.read())
    head, _, body = new_ob.partition(b'\x00')

    position = 0
    while position < len(body):
        new_head, _, new_body = body[position:].partition(b'\x00')
        new_kind, new_size = new_head.split()

        sha = new_body[:sha_len].hex()
        position += len(new_head) + 1 + sha_len

        ob = f'{path}/.git/objects/{sha[:2]}/{sha[2:]}'

        with open(ob, "rb") as f:
            ob = zlib.decompress(f.read())
        ob_head, _, _ = ob.partition(b'\x00')
        ob_kind, _ = ob_head.split()

    print(f'{ob_kind.decode()} {sha}    {new_size.decode()}')
    return

def id_comm(path, name_br):
    file = f'{path}/.git/refs/heads/{name_br}'
    with open(file, "r") as f:
        id = f.read()[:-1]
    return id

# Пройти по истории от последнего к начальному коммиту ветки, для каждого коммита вывести объект-дерево
# В случае нескольких родительских коммитов выбирать первый, топологией не заморачиваться.
# "TREE" большими буквами выделяет строку, где сказано, дерево для какого коммита выводится.
# TREE for commit f5980e79c7f010f38d249390248936dd0ae58a3a
# blob cf1ab25da0349f84a3fdd40032f0ce99db813b8b    LICENSE
# blob f99151731324e7ac98281272c68f2b599dbf868d    Makefile
# tree b6e86ab64d77628cff4cfcaaf9133533733f8553    Tests
# TREE for commit f97190bd4dea21041d1cd7fcf822cd4ac6e7716b
# blob cf1ab25da0349f84a3fdd40032f0ce99db813b8b    LICENSE
# blob 2cb7f6e3ff1a5d1ab379d953dbc7b5738d1dfed3    Makefile
# tree b6e86ab64d77628cff4cfcaaf9133533733f8553    Tests

def tree_history(path, name_br):
    id = id_comm(path, name_br)
    sha_len = len(id) // 2

    while id != ('0' * len(id)):
        print(f'TREE for commit {id}')
        
        # -------
        ob = f'{path}/.git/objects/{id[:2]}/{id[2:]}'
        with open(ob, "rb") as f:
            ob = zlib.decompress(f.read())
        head, _, body = ob.partition(b'\x00')
        new = body.decode()
        # -------
        id = ('0' * len(id))
        for line in new.split('\n'):
            if line.startswith("tree"):
                tree_id = line.split()[1]
            if line.startswith("parent"):
                id = line.split()[1]
        show_tree_safe(path, tree_id, sha_len)
    return

def show_tree_safe(path, name_br, sha_len):
    new_ob = f'{path}/.git/objects/{name_br[:2]}/{name_br[2:]}'
    with open(new_ob, "rb") as f:
        new_ob = zlib.decompress(f.read())

    head, _, body = new_ob.partition(b'\x00')

    position = 0
    while position < len(body):
        new_head, _, new_body = body[position:].partition(b'\x00')
        new_kind, new_size = new_head.split()

        sha = new_body[:sha_len].hex()
        position += len(new_head) + 1 + sha_len

        ob = f'{path}/.git/objects/{sha[:2]}/{sha[2:]}'
        with open(ob, "rb") as f:
            ob = zlib.decompress(f.read())
        ob_head, _, _ = ob.partition(b'\x00')
        ob_kind, _ = ob_head.split()

    print(f'{ob_kind.decode()} {sha}    {new_size.decode()}')
    return

path = sys.argv[1]
if len(sys.argv) == 2:
    print(names_br(path))
elif len(sys.argv) == 3:
    name_br = sys.argv[2]
    lastcommit = last_comm(path, name_br)
    print(lastcommit)
    show_tree(path, name_br)
    tree_history(path, name_br)
