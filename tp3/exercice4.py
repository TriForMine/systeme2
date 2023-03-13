import atexit
import signal
import time

signal_exit = ''
default_int_handler = signal.getsignal(signal.SIGINT)
default_term_handler = signal.getsignal(signal.SIGTERM)
default_abrt_handler = signal.getsignal(signal.SIGABRT)
default_quit_handler = signal.getsignal(signal.SIGQUIT)


def int_handler(signum, frame):
    global signal_exit
    signal_exit = 'INT'
    default_int_handler(signum, frame)


def term_handler(signum, frame):
    global signal_exit
    signal_exit = 'TERM'
    default_term_handler(signum, frame)


def abrt_handler(signum, frame):
    global signal_exit
    signal_exit = 'ABRT'
    default_abrt_handler(signum, frame)


def quit_handler(signum, frame):
    global signal_exit
    signal_exit = 'QUIT'
    default_quit_handler(signum, frame)


def all_done():
    print('The program is done! With signal: ', signal_exit)


signal.signal(signal.SIGINT, int_handler)
signal.signal(signal.SIGTERM, term_handler)
signal.signal(signal.SIGABRT, abrt_handler)
signal.signal(signal.SIGQUIT, quit_handler)
atexit.register(all_done)

while True:
    print('Doing stuff...')
    time.sleep(1)
