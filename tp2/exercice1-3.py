import os, signal, sys, time

counter = 0


def handler(sig, ignore):
    global counter
    counter += 1
    time.sleep(0.1)  # simuler du travail pour le handler


def parent():
    try:
        os.wait()  # attend que le fils se termine
    except:
        pass  # ignore l'exception si le fils est déjà mort
    print("counter= {}".format(counter))
    sys.exit(0)


def child():
    for i in range(5):
        os.kill(os.getppid(), signal.SIGUSR2)
        time.sleep(0.1)
        print("send SIGUSR2 to parent")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGUSR2, handler)  # régler le handler avant le
    pid = os.fork()  # début du fils
    if pid == 0:
        child()
    else:
        parent()
