import time, signal, sys


def capter_INT(sig_num, frame):
    signal.alarm(5)


def capter_ALARM(sig_num, frame):
    print("Alarme!")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, capter_INT)
    signal.signal(signal.SIGALRM, capter_ALARM)
    while True:
        time.sleep(1)
        print("Alive!")
