import os

if __name__ == '__main__':
    for i in os.environ:
        print(i, os.environ[i])