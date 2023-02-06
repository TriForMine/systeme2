import os

if __name__ == '__main__':
    os.environ["PATH"] = os.environ["PATH"] + ":/home/tp1"
    os.system("python3 afficheur.py")