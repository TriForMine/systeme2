import os
import select
import socket
import sys
import time

import consts

HOST = "127.0.0.1"  # or 'localhost' or '' - Standard loopback interface address
PORT = 2001  # Port to listen on (non-privileged ports are > 1023)
MAXBYTES = 4096
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendToAll(data):
    for s in socketlist:
        if s != serversocket and s != sys.stdin:
            s.send(data)


def sendToOthers(clientsocket, data):
    for s in socketlist:
        if s != serversocket and s != clientsocket and s != sys.stdin:
            s.send(data)


def sendToClient(socket, data):
    socket.send(data)


def handleClientMessage(clientsocket, data):
    message = consts.decodeSocketMsg(data.decode())

    if message["type"] == consts.SocketMsgType.CONNECT:
        pseudos[clientsocket] = message["data"]
        print("Pseudo", pseudos[clientsocket], "is now connected.")
        answer = consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                        "Welcome to the chatroom, " + pseudos[clientsocket] + "!\nThere are " + str(
                                            len(socketlist) - 2) + " other users connected.")
        clientsocket.send(answer.encode())

        newUserMsg = consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                            pseudos[clientsocket] + " has joined the chatroom.")
        sendToOthers(clientsocket, newUserMsg.encode())
    elif message["type"] == consts.SocketMsgType.MESSAGE:
        print(pseudos[clientsocket] + ": ", message["data"])
        answer = consts.encodeSocketMsg(consts.SocketMsgType.MESSAGE,
                                        consts.encodeMessageData(pseudos[clientsocket], message["data"]))
        sendToOthers(clientsocket, answer.encode())
    elif message["type"] == consts.SocketMsgType.COMMAND:
        decodedData = consts.decodeCommandData(message["data"])

        if decodedData["command"] == "list":
            sendToClient(clientsocket, consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                              "Connected users: " + str.join(', ',
                                                                                             pseudos.values())).encode())
        elif decodedData["command"] == "dm":
            if len(decodedData["args"]) < 2:
                sendToClient(clientsocket, consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                                  "Usage: /dm <pseudo> <message>").encode())
            else:
                pseudo = decodedData["args"][0]
                message = str.join(' ', decodedData["args"][1:])
                found = False
                for s in socketlist:
                    if s != serversocket and s != clientsocket and s != sys.stdin and pseudos[s] == pseudo:
                        sendToClient(s, consts.encodeSocketMsg(consts.SocketMsgType.DIRECT_MESSAGE,
                                                               consts.encodeMessageData(pseudos[clientsocket],
                                                                                        message)).encode())
                        found = True
                        break
                if not found:
                    sendToClient(clientsocket, consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                                      "User " + pseudo + " not found.").encode())
        elif decodedData["command"] == "help":
            sendToClient(clientsocket, consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                              "Available commands:\n/list: list all connected users\n/dm <pseudo> <message>: send a direct message to the given user\n/help: show this message").encode())
        else:
            sendToClient(clientsocket,
                         consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE, "Unknown command.").encode())


with serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen()
    socketlist = [sys.stdin, serversocket]
    pseudos = {}

    print("Server is listening on port", PORT, "...")

    while len(socketlist) > 0:
        (readable, _, _) = select.select(socketlist, [], [])
        for s in readable:
            if s == serversocket:  # serversocket receives a connection
                (clientsocket, (addr, port)) = s.accept()
                print("connection from:", addr, port)
                socketlist.append(clientsocket)
            elif s == sys.stdin:  # data is sent from the server console
                data = os.read(0, MAXBYTES)
                if len(data) == 0:
                    break
                # Remove trailing newline
                data = data[:-1]

                decodedData = data.decode()
                if decodedData == "/quit":
                    print("Shutting down server...")
                    sendToAll(consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                     "The server is shutting down.").encode())
                    for s in socketlist:
                        if s != serversocket:
                            s.close()
                    socketlist = []
                elif decodedData.startswith("/wall"):
                    content = decodedData[6:]
                    if len(content) > 0:
                        sendToAll(consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE, content).encode())
                    else:
                        print("Usage: /wall <message>")
                elif decodedData.startswith("/kick"):
                    username = decodedData[6:]
                    if len(username) > 0:
                        sendToAll(consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                         username + " has been kicked.").encode())
                        for s in socketlist:
                            if s != serversocket and s != sys.stdin and pseudos[s] == username:
                                s.close()
                                socketlist.remove(s)
                                pseudos.pop(s)
                                break
                elif decodedData.startswith("/shutdown"):
                    seconds = decodedData[10:]
                    if len(seconds) > 0:
                        seconds = int(seconds)
                        sendToAll(consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                         "The server will shutdown in " + str(
                                                             seconds) + " seconds.").encode())
                        time.sleep(seconds)
                        print("Shutting down server...")
                        sendToAll(consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                         "The server is shutting down.").encode())
                        for s in socketlist:
                            if s != serversocket:
                                s.close()
                        socketlist = []
                    else:
                        print("Usage: /shutdown <seconds>")
                else:
                    print("Unknown command.")
            else:  # data is sent from given client
                data = s.recv(MAXBYTES)
                if len(data) > 0:
                    handleClientMessage(s, data)
                else:  # client has disconnected
                    print(pseudos[clientsocket], "has disconnected.")
                    leftMessage = consts.encodeSocketMsg(consts.SocketMsgType.SERVER_MESSAGE,
                                                         pseudos[clientsocket] + " has left the chatroom.")
                    sendToOthers(clientsocket, leftMessage.encode())
                    s.close()
                    pseudos.pop(s)
                    socketlist.remove(s)
