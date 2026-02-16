import zlib
from pathlib import Path
import sys

for obj in Path(sys.argv[1]).glob(".git/objects/??/*"):
    data = zlib.decompress(obj.read_bytes)

    header, _, body = data.partition(b'\x00')
    type, s = header.split()
    if type == b'commit':
        print(body.decode())
