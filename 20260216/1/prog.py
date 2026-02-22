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


path = sys.argv[1]
if len(sys.argv) == 2:
    print(names_br(path))