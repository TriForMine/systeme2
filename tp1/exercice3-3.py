import os
import sys

if __name__ == "__main__":
    n = sys.argv[1]
    n = int(n)

    print("------ Arbre -------")
    for i in range(n):
        pid = os.fork()
        if pid != 0:
            sys.exit(0)
        else:
            print("Je suis le fils", os.getpid(), "de", os.getppid())
