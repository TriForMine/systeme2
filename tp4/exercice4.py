import os
import sys
import time

fd_read, fd_write = os.pipe()

if os.fork() == 0:
    bytes = os.getpid().to_bytes(4, byteorder='big')
    os.write(fd_write, bytes)
    time.sleep(1)
    sys.exit(0)

if os.fork() == 0:
    pid = os.read(fd_read, 4)
    print("PID frère : ", int.from_bytes(pid, byteorder='big'))
    sys.exit(0)

for i in range(2):
    pid = os.wait()[0]
    print("PID fils : ", pid)
