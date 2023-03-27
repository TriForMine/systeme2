import select
import socket

import consts

HOST = "127.0.0.1"  # or 'localhost' or '' - Standard loopback interface address
PORT = 2000  # Port to listen on (non-privileged ports are > 1023)
MAXBYTES = 4096
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen()
socketlist = [serversocket]
pseudos = {}

print("Server is listening on port", PORT, "...")


def sendToAll(data):
    for s in socketlist:
        if s != serversocket:
            s.send(data)


def sendToOthers(clientsocket, data):
    for s in socketlist:
        if s != serversocket and s != clientsocket:
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
                    if s != serversocket and s != clientsocket and pseudos[s] == pseudo:
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


while len(socketlist) > 0:
    (readable, _, _) = select.select(socketlist, [], [])
    for s in readable:
        if s == serversocket:  # serversocket receives a connection
            (clientsocket, (addr, port)) = s.accept()
            print("connection from:", addr, port)
            socketlist.append(clientsocket)
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
