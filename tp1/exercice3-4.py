import os
import sys

if __name__ == "__main__":
    n = sys.argv[1]
    n = int(n)

    print("------ Châine -------")

    for i in range(n):
        pid = os.fork()
        if pid == 0:
            print("Je suis le fils", os.getpid(), "de", os.getppid())
            sys.exit(0)
    sys.exit(0)