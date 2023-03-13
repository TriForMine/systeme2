import os
import sys

fd_read, fd_write = os.pipe()
if os.fork() == 0:
    # fils
    os.close(fd_write)  # <- important!
    msg = b''
    while True:
        c = os.read(fd_read, 1)
        if c == b'': break
        msg += c
    os.close(fd_read)
    print(msg.decode('utf-8'))
    sys.exit(0)
# père
os.close(fd_read)
os.write(fd_write, b'hello!')
os.close(fd_write)  # <- important!
os.wait()
print('bye')
sys.exit(0)
