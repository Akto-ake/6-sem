
"""Project"""
import sys
import calendar

def restmonth(year: int, month: int):
    """documentation"""

    header, days, *dates = calendar.month(year, month).split("\n")
    gap, sep = "\n    ", " ".join(["=="] * 7)
    dates[0] = dates[0].replace('   ', r"\ ")
    res = [f".. table:: {header.strip()}\n", sep, days, sep, *dates[:-1], sep]
    return gap.join(res)

if __name__ == "__main__":
    print(restmonth(sys.argv[1], sys.argv[2])))
