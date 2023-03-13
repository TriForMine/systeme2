import os, signal, time

if __name__ == "__main__":
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    pid = os.getpid()
    print("pid", pid)
    while True:
        time.sleep(1)