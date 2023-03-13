import os
import signal
import time


def handler(sig_num, frame):
    print("Coucou !")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    print(os.getpid())
    time.sleep(30)