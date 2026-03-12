import cmd
import readline
from shlex import split

from pathlib import Path
# cwd = Path(".")

# print(list(cwd.glob("..")))

class SizeCmdl(cmd.Cmd):
    prompt = "==>"

    def do_size(self, arg):
        """Print file size"""
        args = split(arg)
        for i in args:
            print(f"{i}: {Path(i).stat().st_size}")
        
    def do_EOF(self, arg):
        print("\nBye\n")
        return 1

if __name__ == "__main__":
    SizeCmdl().cmdloop()
