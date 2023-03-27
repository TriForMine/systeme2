import json
from enum import Enum


class SocketMsgType(Enum):
    USERNAME = 1
    MESSAGE = 2
    DIRECT_MESSAGE = 3
    SERVER_MESSAGE = 4
    CONNECT = 5
    DISCONNECT = 6
    COMMAND = 7


def encodeMessageData(username: str, message: str):
    return json.dumps({
        "username": username,
        "message": message
    })


def decodeMessageData(data: str):
    return json.loads(data)


def encodeCommandData(command: str, args: list):
    return json.dumps({
        "command": command,
        "args": args
    })


def decodeCommandData(data: str):
    return json.loads(data)


def encodeSocketMsg(msg_type: SocketMsgType, data: str):
    return json.dumps({
        "type": msg_type.value,
        "data": data
    })


def decodeSocketMsg(msg: str):
    decoded = json.loads(msg)
    return {
        "type": SocketMsgType(decoded["type"]),
        "data": decoded["data"]
    }
