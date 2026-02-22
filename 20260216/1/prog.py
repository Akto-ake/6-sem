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
    file = path + "/.git/refs/heads/" + name_br
    with open(file, "r") as f:
        id = f.read()[:-1]
    
    ob = f'{path}/.git/objects/{id[:2]}/{id[2:]}'

    with open(ob, "rb") as f:
        ob = zlib.decompress(f.read())
    
    head, _, body = ob.partition(b'\x00')
    kind, _ = head.split()

    print(id, kind.decode())
    print(body.decode())
    return


path = sys.argv[1]
if len(sys.argv) == 2:
    print(names_br(path))
    exit
name_br = sys.argv[2]
last_comm(path, name_br)
