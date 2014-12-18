import json
import socket
import threading
import sys


class NetGameServer:
    def __init__(self, port=12345, host=""):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.games = {}

        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print("Failed to bind socket ", socket.error)
            sys.exit()

        self.sock.listen(10)

    def exit(self):
        self.sock.close()

    def threadrunner(self, username, client, addr):
        user = self.users[username]
        welcome = "User " + username + " connected "
        print(welcome)

        # generate roomlist and send back
        roomlist = self.encode_JSON(self.listplayers(False, user["data"]["game"]))
        for user in self.users.values():
            if user["data"]["playing"] == 0:
                user["connection"].sendall(bytes(roomlist, encoding='utf-8'))

        while True:
            client.setblocking(1)
            raw = client.recv(2048).decode("utf-8")
            data = self.decode_JSON(raw)
            self.opponent = self.users[data["data"]["opponent"]]

            print(raw)

            # when the other player accepts
            if data["action"] == "connection_established":
                if self.games[username]["active"] == True:
                    #exit while loop and start listening for gamedata
                    break

            # master asks to connect to opponent
            elif data["action"] == "connect":
                if self.opponent["data"]["playing"] == 0:

                    # server sends GameInvitation to opponent
                    print(self.opponent["connection"].sendall(
                        bytes(self.encode_JSON(self.connect(username)), encoding='utf-8')))

                    #game gets added (inactive)
                    self.gameHost = username
                    self.games[username] = {
                        "master": username,
                        "players": [username, data["data"]["opponent"]],
                        "game": user["data"]["game"],
                        "active": False,
                        "startdatetime": False
                    }


                else:
                    client.sendall(
                        bytes(self.encode_JSON(self.error("notavailable", "User already ingame.")), encoding='utf-8'))

            #opponent accepts connect from master
            elif data["action"] == "connect_accepted":

                #send connect established to master
                self.opponent["connection"].sendto(
                    bytes(self.encode_JSON(
                        self.established(username)), encoding='utf-8'))

                #activate game
                self.gameHost = data["data"]["opponent"]
                self.games[self.gameHost]["active"] = True

                #break while and starts listening to client
                break

            #opponent refuses connect from master
            elif data["action"] == "connection_refused":
                self.opponent["connection"].sendto(
                    bytes(self.encode_JSON(
                        self.error("connection_refused", "Your opponent refused.")),
                          encoding='utf-8'))

        user["playing"] = 1

        #start listening for gamedata
        while True:
            try:
                data = client.recv(2048)
                if not data:
                    client.close()
                    del self.users[username]
                    for user in self.users:
                        user["connection"].sendall(bytes(self.encode_JSON(self.disconnect(user["username"])), "utf-8"))
                    print(user["username"], "disconnected")
                    break
                print(data.decode("utf-8"))

                #checks if the player is sending gamedata
                if data["action"] == "gamedata":
                    for player in self.games[self.gameHost]["players"]:
                        if player != username:
                            self.users[player]["connection"].sendall(data)

                #other actions are currently not allowed
                else:
                    client.sendall(
                        bytes(self.encode_JSON(
                            self.error("action_not_allowed", "This action is currently not possible.")),
                              encoding='utf-8'))


            except:
                pass

        client.close()


    def run(self):
        print("Waiting for connections on port", self.port)
        while True:
            client, addr = self.sock.accept()
            content = self.decode_JSON(client.recv(2048).decode("utf-8"))

            if content["action"] == "connection":
                username = content["data"]["username"]
                username_taken = False
                for name in self.users.keys():
                    if name == username:
                        username_taken = True

                if username_taken:
                    client.sendall(
                        bytes(self.encode_JSON(self.error("doubleusername", "Please connect first")), encoding='utf-8'))
                    client.close()
                else:
                    self.users[username] = {
                        "connection": client,
                        "address": addr,
                        "data": {
                            "username": username,
                            "game": content["data"]["game"],
                            "playing": 0

                        }
                    }
                    threading.Thread(target=self.threadrunner, name=username, args=(username, client, addr)).start()
            else:
                client.sendall(bytes(self.encode_JSON(self.error("Please connect first")), encoding='utf-8'))
                client.close()


    def decode_JSON(self, string):
        return json.loads(string)


    def encode_JSON(self, object):
        return json.dumps(object)


    def error(self, string, message):
        return {
            "action": "error",
            "data": {
                "errorinfo": string,
                "helpmessage": message
            }
        }


    def listplayers(self, printAllPlayers=True, currentGame=False):
        userlist = []
        if printAllPlayers:
            if currentGame:
                for user in self.users.values():
                    if user["data"]["game"] == currentGame:
                        userlist.append(user["data"])
            else:
                for user in self.users.values():
                    userlist.append(user["data"])

        else:
            if currentGame:
                for user in self.users.values():
                    if user["data"]["playing"] == 0:
                        if user["data"]["game"] == currentGame:
                            userlist.append(user["data"])
            else:
                for user in self.users.values():
                    if user["data"]["playing"] == 0:
                        userlist.append(user["data"])

        return {
            "action": "listplayers",
            "data": userlist
        }


    def connect(self, user):
        return {
            "action": "gameinvitation",
            "data": {
                "master": user
            }
        }


    def established(self, username):
        return {
            "action": "connection_established",
            "data": {
                "username": username
            }
        }


    def disconnect(self, user):
        return {
            "action": "disconnect",
            "data": {
                "username": user
            }
        }


if __name__ == "__main__":
    server = NetGameServer()
    server.run()