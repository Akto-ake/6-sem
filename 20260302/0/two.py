import shlex

line = input("")
cmd, *args = shlex.split(line)
print(cmd, args)

# print(shlex.split(input()))