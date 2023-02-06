import errno, os, sys

if __name__ == "__main__":
    nbChildren = 20
    for i in range(nbChildren):
        pid = os.fork()
        if pid == 0:  # child
            sys.exit(100 + i)
        try:  # parent waits for all of its children to terminate
            while True:
                pid, status = os.waitpid(-1, 0)
                if os.WIFEXITED(status):
                    print(
                        "child {} terminated normally with exit status={}".format(
                            pid, os.WEXITSTATUS(status)
                        )
                    )
                else:
                    print("child {} terminated abnormally".format(pid))
        except OSError as e:
            print(
                "waitpid error: {}, {}".format(
                    errno.errorcode[e.errno], os.strerror(e.errno)
                ),
                file=sys.stderr,
            )
            if e.errno == errno.ECHILD:
                print("No more children left. Bye", file=sys.stderr)
    sys.exit(0)
