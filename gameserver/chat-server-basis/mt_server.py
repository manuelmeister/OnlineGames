import socket, threading, sys

class ChatServer:
    def __init__(self, port=12345, host=""):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.threads = []

        try:
            self.sock.bind((self.host, self.port))
        except socket.error:
            print("Failed to bind socket ", socket.error)
            sys.exit()

        self.sock.listen(10)

    def exit(self):
        self.sock.close()

    def threadrunner(self, client, addr):
        name = self.users[client]
        welcome = "User "+name+" connected on "+addr[0]+":"+str(addr[1])
        print(welcome)
        for user in self.users:
            user.sendall(welcome.encode("utf-8"))
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    client.close()
                    del self.users[client]
                    for user in self.users:
                        user.sendall(bytes(name, "utf-8") + b" disconnected")
                    break
                print(name, ":", data.decode("utf-8"))
                for user in self.users:
                    user.sendall(bytes(name, "utf-8") + b":" + data)
            except:
                pass

        client.close()

    def run(self):
        print("Waiting for connections on port", self.port)
        while True:
            client, addr = self.sock.accept()
            client.sendall(b"Connected to Server, please type in your Username")
            name = client.recv(1024).decode("utf-8")

            username_taken = False
            for cconnection, cname in self.users.items():
                if cname == name:
                    username_taken = True

            if username_taken:
                client.sendall("Username nicht mehr verfügbar".encode("utf-8"))
                client.sendall(b"/reconnect")
                client.close()
            else:
                self.users[client] = name
                threading.Thread(target=self.threadrunner, args=(client, addr)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.run()