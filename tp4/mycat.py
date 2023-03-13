import os
import sys

if len(sys.argv) > 1:
    files = sys.argv[1:]
    for file in files:
        with open(file, "rb") as f:
            octets = f.read()
            os.write(1, octets)
else:
    while True:
        octets = os.read(0, 100)
        if not octets:
            break
        os.write(1, octets)
