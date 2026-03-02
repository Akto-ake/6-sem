while a:= input():
    cmd, *args = a.split()
    print(cmd, len(args), args)