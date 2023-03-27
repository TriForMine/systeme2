import os
import select
import socket
import sys

import consts

MAXBYTES = 4096

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "hote port")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

PSEUDO = input("Veuillez entrer votre pseudo: ")

sockaddr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP

with s:
    s.connect(sockaddr)
    print("connected to:", sockaddr)

    inArray = [sys.stdin, s]

    # Send username
    s.send(consts.encodeSocketMsg(consts.SocketMsgType.CONNECT, PSEUDO).encode())


    def showMessage(username, message):
        os.write(1, ("\033[32m" + username + "\033[0m: " + message + "\n").encode())


    def showDirectMessage(username, message):
        os.write(1, ("\033[34m" + "DM from " + username + "\033[0m: " + message + "\n").encode())


    def showServerMessage(message):
        os.write(1, ("\033[33m[SERVER]\033[0m " + message + "\n").encode())


    def handleMessage(data):
        message = consts.decodeSocketMsg(data.decode())
        if message["type"] == consts.SocketMsgType.SERVER_MESSAGE:
            showServerMessage(message["data"])
        elif message["type"] == consts.SocketMsgType.MESSAGE:
            data = consts.decodeMessageData(message["data"])
            showMessage(data["username"], data["message"])
        elif message["type"] == consts.SocketMsgType.DIRECT_MESSAGE:
            data = consts.decodeMessageData(message["data"])
            showDirectMessage(data["username"], data["message"])


    while True:
        inReady, _, _ = select.select(inArray, [], [])

        if sys.stdin in inReady:
            data = os.read(0, MAXBYTES)
            if len(data) == 0:
                break
            # Remove trailing newline
            data = data[:-1]

            decodedData = data.decode()
            if decodedData.startswith('/'):
                if decodedData.startswith('/quit'):
                    break
                else:
                    command = decodedData[1:].split(' ')
                    args = command[1:]
                    commandName = command[0]
                    s.send(consts.encodeSocketMsg(consts.SocketMsgType.COMMAND,
                                                  consts.encodeCommandData(commandName, args)).encode())
            else:
                s.send(consts.encodeSocketMsg(consts.SocketMsgType.MESSAGE, data.decode()).encode())
        else:
            data = s.recv(MAXBYTES)
            if len(data) == 0:
                break
            handleMessage(data)
