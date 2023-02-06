import os
import sys

if __name__ == "__main__":
    print("Pere\n", "PID:", os.getpid(), "\nPPID:", os.getppid(), "\n")

    for i in range(3):
        pid = os.fork()
        if pid == 0:
            print(
                "Fils", i + 1, "\n", "PID:", os.getpid(), "\nPPID:", os.getppid(), "\n"
            )

            if i == 0:
                for j in range(2):
                    pid = os.fork()
                    if pid == 0:
                        print(
                            "Petit-fils",
                            j + 1,
                            "\n",
                            "PID:",
                            os.getpid(),
                            "\nPPID:",
                            os.getppid(),
                            "\n",
                        )
                        sys.exit(0)
                    else:
                        os.waitpid(pid, 0)
                sys.exit(0)
            else:
                sys.exit(0)
        else:
            os.waitpid(pid, 0)
    sys.exit(0)
