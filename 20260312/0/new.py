import cmd
import readline
from shlex import split
from calendar import TextCalendar
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
    
    def do_month(self, arg):
        """print a month calendar"""
        args = arg.split()
        try:
            TextCalendar().prmonth(int(args[0]), int(args[1]))
        except Exception:
            print("no args")
        
    def do_year(self, arg):
        """print a year calendar"""
        try:
            TextCalendar().pryear(int(arg))
        except Exception:
            print("no args")

if __name__ == "__main__":
    SizeCmdl().cmdloop()
