import time, sys, signal, os

if __name__ == "__main__":
    pid_pere = os.getpid()
    pid = os.fork()
    if pid == 0:  # Fils
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while True:
            time.sleep(1)
            try:
                os.kill(pid_pere, 0)
            except OSError:
                print("Fils détecte fin père")
                break
    else:
        bytes = os.read(0, 1)
        while len(bytes) != 0:
            os.write(1, bytes)
            bytes = os.read(0, 1)
        sys.exit(0)
