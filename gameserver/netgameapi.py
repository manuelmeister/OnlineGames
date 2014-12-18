import json
import socket
import time


class NetGameApi:
    def __init__(self, username, gametype, receivingFunction, host='localhost', port=12345):
        self.username = username
        self.gametype = gametype
        self.receivingFunction = receivingFunction()
        self.host = host
        self.port = port
        self.output = ''
        self.newInstance()

    def newInstance(self):
        self.model = Model(self.host, self.port)
        self.model.connect()

    def decode_JSON(self, string):
        return json.loads(string)

    def makeConnection(self):
        time.sleep(.42)
        dictionary = {
            "action": "connection",
            "data": {
                "username": self.username,
                "game": self.gametype
            }
        }
        self.model.send(dictionary)

    def getPlayerList(self, game = 'all', notInGame = True):
        dictionary = {
            "action": "getplayerlist",
            "data": {
                "game": game,
                "playing": notInGame
            }
        }
        self.model.send(dictionary)

    def connectToPlayer(self, playername):
        dictionary = {
            "action": "connect",
            "data": {
                "master": self.username,
                "opponent": playername
            }
        }
        print(dictionary)
        self.model.send(dictionary)

    def connectionEstablished(self, playername):
        dictionary = {
            "action": "connecttion_established",
            "data": {
                "opponent": playername
            }
        }
        self.model.send(dictionary)

    def acceptGameInvitation(self, username):
        dictionary = {
            "action": "connect_established",
            "data": {
                "opponent": username
            }
        }
        self.model.send(dictionary)

    def refuseGameInvitation(self, username):
        dictionary = {
            "action": "connect_refused",
            "data": {
                "opponent": username
            }
        }
        self.model.send(dictionary)

    def submitGameData(self, content):
        dictionary = {
            "action": "gamedata",
            "data": content
        }
        self.model.send(dictionary)

    def startReceiving(self):
        data_received = True
        while data_received:
            try:
                data_received = self.model.receive()
                if not data_received:
                    break
                output = self.decode_JSON(data_received.decode("utf-8"))
                print(output)
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
        data = self.sock.recv(2048)
        if not data:
            return False
        else:
            return data

    def send(self, content):
        self.sock.sendto(bytes(json.dumps(content), encoding='utf-8'), self.conn)
