import json
import socket, threading, sys
import datetime


class NetGameServer:
    def __init__(self, port=12345, host=""):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.games = []

        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print("Failed to bind socket ", socket.error)
            sys.exit()

        self.sock.listen(10)

    def exit(self):
        self.sock.close()

    def threadrunner(self, username):
        user = self.users[username]
        client = user["connection"]
        welcome = "User " + username + " connected "
        print(welcome)

        roomlist = self.encode_JSON(self.listplayers())
        for user in self.users.values():
            if user["data"]["playing"] == 0:
                user["connection"].sendall(bytes(roomlist, encoding='utf-8'))

        while True:
            data = self.decode_JSON(client.recv(1024).decode("utf-8"))
            if data["action"] == "connect":
                if self.users[data["data"]["opponent"]]["data"]["playing"] == 0:
                    self.games.append({
                        username:{
                            "master": username,
                            "players": [username, data["opponent"]],
                            "game": user["data"]["game"],
                            "startdatetime": datetime.now()
                        }
                    })
                    break
                else:
                    client.sendall(bytes(self.encode_JSON(self.error("notavailable", "User already ingame.")), encoding='utf-8'))
            elif data["action"] == "connection_established":
                break
            elif data["action"] == "connection_refused":
                client.sendall(bytes(self.encode_JSON(self.error("connection_refused", "Your opponent refused.")),encoding='utf-8'))
            else:
                client.sendall(
                    bytes(self.encode_JSON(self.error("notconnected", "You must connect to a player first.")),
                          encoding='utf-8'))

        user["playing"] = 1
        self.user[self.games[username]["players"][0]] = 1

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    client.close()
                    del self.users[username]
                    for user in self.users:
                        user["connection"].sendall(bytes(self.encode_JSON(self.disconnect(user["username"])), "utf-8"))
                    print(user["username"], "disconnected")
                    break
                print(data.decode("utf-8"))
                for player in self.games["players"]:
                    self.users[player].sendall(data)
            except:
                pass

        client.close()

    def run(self):
        print("Waiting for connections on port", self.port)
        while True:
            client, addr = self.sock.accept()
            content = self.decode_JSON(client.recv(1024).decode("utf-8"))

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
                        "data": {
                            "username": username,
                            "game": content["data"]["game"],
                            "playing": 0

                        }
                    }
                    threading.Thread(target=self.threadrunner, args=(username,)).start()
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

    def listplayers(self, printAllPlayers=True):
        userlist = []
        if printAllPlayers:
            for user in self.users.values():
                userlist.append(user["data"])
        else:
            for user in self.users.values():
                if user["data"]["playing"] == 0:
                    userlist.append(user["data"])

        return {
            "action": "listplayers",
            "data": userlist
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