import os
import sys
import time


def argument_parser():
    arguments = {}

    currentArg = None
    command = None
    commandArgs = []

    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            if arg == '-s':
                arguments[arg] = True
            else:
                arguments[arg] = None
                currentArg = arg
        else:
            if currentArg is None:
                if command is None:
                    command = arg
                else:
                    commandArgs.append(arg)
            else:
                arguments[currentArg] = arg
                currentArg = None

    if command is None:
        print('Usage: mytime [-n <n>] [-s] <command> [<args>]')
        exit(1)

    return arguments, command, commandArgs


if __name__ == '__main__':
    (args, command, commandArgs) = argument_parser()
    print(args, command, commandArgs)

    count = 1

    if '-n' in args:
        count = int(args['-n'])

    print('Running ' + command + ' ' + ' '.join(commandArgs) + ' ' + str(count) + ' times')

    times = []

    for i in range(count):
        executeTime = time.time()
        result = os.system(command + ' ' + ' '.join(commandArgs))
        executeTime = time.time() - executeTime
        times.append(executeTime)
        if '-s' in args:
            print(str(i) + '/' + str(count) + ' Result: ' + str(result) + ' Time elapsed: ' + str(executeTime) + ' s')

    meanTime = sum(times) / len(times)

    print('Time elapsed: ' + str(meanTime) + ' s')
    print('Time elapsed: ' + str(meanTime * 1000) + ' ms')
