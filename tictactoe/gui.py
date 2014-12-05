
from tkinter import *
import threading
from gameserver.netgameapi import *
import tictactoe2

#from multiprocessing.pool import ThreadPool
#from functools import partial



class Gui:
    def __init__(self):
        self.initial_gui()

    def initial_gui(self):
        self.main = Tk()
        self.main.title('WayUp GameStation')
        self.txtScreen=Text(self.main, height=20, width=50, bg="#bbbbbb")
        self.txtScreen.pack(side=TOP)
        self.strInput = str()
        self.txtInput = Entry(self.main,  width=40, textvariable=self.strInput)
        self.txtInput.pack(side = LEFT)
        self.cmdSubmit = Button(self.main, width=10, command=self.connect, text="Submit")
        self.cmdSubmit.pack(side=RIGHT)
        self.txtScreen.insert(END, "Please choose your Username\n")
        self.gui_mainloop_thread = Thread(name='gui_mainloop', target=self.main.mainloop())

    def connect(self):
        username = self.txtInput.get()
        self.txtScreen.insert(END, "connecting...\n")

        self.api = NetGameApi(username, "tictactoe", lambda: self.reciever)
        time.sleep(.42)
        self.api.makeConnection()
        self.tcpthread = Thread(name='tcp', target=self.api.startReceiving())
        self.tcpthread.start()


    def reciever(self, data):
        print(data)

        if data == "Username ok":
            playerlist=data
            self.choose_player(playerlist)

        if data == "connect von anderem Player":
            self.initialize_tictactoe(2)

        if data == "Game Start":
            self.initialize_tictactoe(1)

        if data == "player 2 hat gespielt":
            self.tictactoe.update_board()
            self.tictactoe.mainloop()

    def initialize_tictactoe(self, player):
        self.tictactoe = tictactoe2.TicTacToe(1)

    def choose_player(self,playerlist):
        self.playerlist=playerlist
        try:
            self.main.destroy()
        except:
            pass
        self.main = Tk()
        self.main.title('WayUp GameStation')
        self.txtScreen=Text(self.main, height=20, width=50, bg="#bbbbbb")
        self.txtScreen.pack(side=TOP)
        self.lstPlayerListe = Listbox(side=LEFT)
        for i in range(len(self.playerlist)):
            self.lstPlayerListe.insert(i, self.playerlist[i])
        self.lstPlayerListe.pack()
        self.cmdSubmit = Button(self.main, width=10, command=self.connet_to_player, text="Submit")
        self.cmdSubmit.pack(side=RIGHT)
        self.txtScreen.insert(END, "Please choose your Username\n")
        self.gui_choose_player_thread = Thread(name='choose_player', target=self.main.mainloop())


    def connet_to_player(self):
        self.api.connet_to_player() # Api braucht noch entsprechende Funktion
        self.main.destroy()
        self.initialize_tictactoe(1) # Player muss noch erkannt werden!


gamestation = Gui()
