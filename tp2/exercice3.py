import time, sys, signal

compteur = 0


def ALRM_handler(sig_num, frame):
    global compteur
    signal.alarm(2)  # Relancer l'alarme
    compteur += 1
    print(compteur)
    if compteur == 5:
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, ALRM_handler)
    signal.alarm(2)
    bytes = sys.stdin.read(1)
    while len(bytes) != 0:
        sys.stdout.write(bytes)
        bytes = sys.stdin.read(1)
    sys.exit(0)
