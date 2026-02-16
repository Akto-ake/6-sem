from pathlib import Path
import sys

#data = sorted(Path(".").glob('*.py'))
#print(data)

for obj in Path(sys.argv[1]).glob(".git/objects/??/*"):
    print(obj)

