import time
import signal


def handler(signum, frame):
    print("Signal handler called with signal", signum)
    raise SystemExit(1)


signal.signal(signal.SIGINT, handler)
signal.pause()
