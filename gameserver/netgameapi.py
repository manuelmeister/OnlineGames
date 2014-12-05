import json
import socket
from threading import Thread
import time


class NetGameApi:
    def __init__(self, username, gametype, receivingFunction):
        self.receivingFunction = receivingFunction()
        self.username = username
        self.gametype = gametype
        self.output = ''
        self.newInstance()

    def newInstance(self):
        self.model = Model('localhost', 12345)
        self.model.connect()

    def decode_JSON(self, string):
        return json.loads(string)

    def makeConnection(self):
        dictionary = {
            "action": "connection",
            "data": {
                "username": self.username,
                "game": self.gametype
            }
        }
        self.model.send(dictionary)

    def connectToPlayer(self, playername):
        dictionary = {
            "action": "connect",
            "data": {
                "username": playername
            }
        }
        self.model.send(dictionary)

    def submitGameData(self, content):
        dictionary = {
            "action": "gamedata",
            "data": content
        }
        self.model.send(dictionary)

    def askForUsername(self):
        #give input
        pass

    def startReceiving(self):
        data_received = True
        while data_received:
            try:
                data_received = self.model.receive()
                if not data_received:
                    break
                output = self.decode_JSON(data_received.decode("utf-8"))
                self.receivingFunction(output)

            except socket.error:
                break

class Model(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.sock.connect(self.conn)

    def close(self):
        self.sock.close()

    def receive(self):
        data = self.sock.recv(1024)
        if not data:
            return False
        else:
            return data

    def send(self, content):
        self.sock.sendto(bytes(json.dumps(content), encoding='utf-8'), self.conn)
