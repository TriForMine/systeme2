# un shell ultra basique
import os
import sys

fd = os.open("logs.txt", os.O_WRONLY | os.O_CREAT | os.O_APPEND)

if len(sys.argv) == 2:
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        os.dup2(f.fileno(), 0)

while True:
    cmd = input("commande? ")
    if cmd == "exit":
        break
    args = cmd.split(" ")
    if os.fork() == 0:
        os.dup2(fd, 1)
        os.dup2(fd, 2)
        os.execvp(args[0], args)
    os.wait()

os.close(fd)
