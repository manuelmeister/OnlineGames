
from tkinter import *
import threading
from gameserver.netgameapi import *
import gameserver
from functools import partial



class Gui:
    def __init__(self):
        self.initial_gui()

    def initial_gui(self):
        try:
            self.main.destroy()
        except:
            pass
        self.main = Tk()
        self.main.title('WayUp GameStation')
        self.txtScreen=Text(self.main, height=20, width=50, bg="#bbbbbb")
        self.txtScreen.pack(side=TOP)
        self.strInput = str()
        self.txtInput = Entry(self.main,  width=40, textvariable=self.strInput)
        self.txtInput.pack(side = LEFT)
        self.cmdSubmit = Button(self.main, width=10, command=self.connect, text="Submit")
        self.cmdSubmit.pack(side=RIGHT)
        self.txtScreen.insert(END, "Please choose your Username")



        self.main.mainloop()

    def connect(self):
        username = self.txtInput.get()
        self.api = NetGameApi(username, "tictactoe", lambda: self.reciever)
        try:
            self.main.destroy()
        except:
            pass
        self.main = Tk()
        self.main.title('connecting...')
        self.txtScreen=Text(self.main, height=20, width=50, bg="#bbbbbb")
        self.txtScreen.pack(side=TOP)
        self.txtScreen.insert(END, "Please wait for your connection...")
        threading.Thread(target=self.listener, args=()).start()
        self.main.mainloop()


    def reciever(self, jsonfile):
        data = self.api.json_decode(jsonfile)
        print(data)


    def listener(self):
        # NOT API, LÜKU'S LISTENER!

        while True:
            host = 'localhost'
            port = 12345
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(1)
            conn, addr = s.accept()
            print('\rConnected by', addr[0], "\nIch : ", end="")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Connection to", addr[0],"closed\n")
                    conn.close()
                    break
                print('\rReceived by', addr[0], ";", "timestamp:", time.asctime(time.localtime(time.time())), "\n", data.decode("utf-8"), "\nIch : ", end="")



gamestation = Gui()
