import errno, os, sys, time

lpid = []
nbChildren = 20

for i in range(nbChildren):
    pid = os.fork()
    if pid == 0:  # child
        time.sleep(5)
        sys.exit(100 + i)
    else:
        lpid.append(pid)
        print("child {} created".format(pid))

for p in lpid:  # parent waits for all of its children to terminate
    pid, status = os.waitpid(p, 0)
    if os.WIFEXITED(status):
        print("child {} terminated normally with exit status={}".format(pid, os.WEXITSTATUS(status)))
    else:
         if os.WIFSIGNALED(status):
             sig = os.WTERMSIG(status)
             print("child {} terminated by signal {}".format(pid, sig))
         else:
             print("child {} terminated abnormally".format(pid))

sys.exit(0)
