import time, sys, signal, os

counter = 0


def handler(signum, frame):
    global counter
    counter += 1


if __name__ == "__main__":
    n = int(sys.argv[1])
    signal.signal(signal.SIGUSR1, handler)
    pid = os.fork()
    if pid == 0:
        for i in range(0, n):
            os.kill(os.getppid(), signal.SIGUSR1)
        sys.exit(0)
    else:
        os.waitpid(pid, 0)
        print(counter)
