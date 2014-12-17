
from tkinter import *
import threading
from threading import Thread
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
        self.playername=username
        self.txtScreen.insert(END, "connecting...\n")
        self.main.update()
        #try:
        self.api = NetGameApi(username, "tictactoe", lambda: self.reciever)
        time.sleep(.42)
        self.api.makeConnection()
        self.tcpthread = Thread(name='tcp', target=self.api.startReceiving())
        self.tcpthread.start()
        #except:
            #self.txtScreen.insert(END, "connection failed\n")


    def reciever(self, content):
        print(content)

        if content["action"] == "listplayers":
            self.choose_player(content["data"])

        if content["action"] == "gameinvitation":
            username = content["data"]["master"]
            self.txtScreen.insert(END, "would you like to accept this game invitation?")
            self.ok_boolean=FALSE
            self.ok(username)
            if self.ok_boolean:
                self.api.acceptGameInvitation(username)
                self.initialize_tictactoe(1)
            else:
                self.api.refuseGameInvitation(username)
                pass


        if content["action"] == "connect_accepted":
            try:
                self.main.destroy()
            except:
                pass
            self.initialize_tictactoe(2)


        if content["action"] == "gamedata":
            self.tictactoe.update_board(content["data"])
            self.tictactoe.mainloop()

    def ok(self, username):
        self.okwindow = Tk()
        self.okwindow.title('Anfrage')
        self.txtOkScreen=Text(self.okwindow, height=4, width=20, bg="#bbbbbb")
        self.txtOkScreen.pack(side=TOP)
        self.txtOkScreen.insert(END, str(username)+" invited you to play a game")
        self.cmdOk = Button(self.main, width=10, command=self.ok_bool_function, text="Ok")
        self.cmdOk.pack(side=RIGHT)
        self.cmdNotOk = Button(self.main, width=10, command=self.not_ok_bool_function, text="Abort")
        self.cmdNotOk.pack(side=RIGHT)
        self.txtScreen.insert(END, "Please choose your Username\n")
        self.gui_choose_player_thread = Thread(name='choose_player', target=self.main.mainloop())

    def ok_bool_function(self):
        try:
            self.okwindow.destroy()
        except:
            pass
        self.ok_boolean=True

    def not_ok_bool_function(self):
        try:
            self.okwindow.destroy()
        except:
            pass
        self.ok_boolean=False


    def initialize_tictactoe(self, player):
        self.tictactoe = tictactoe2.TicTacToe(1)




    def choose_player(self,playerlist):
        try:
            self.txtInput.destroy()
            self.cmdSubmit.destroy()
            self.playerlist=playerlist
            self.lstPlayerListe = Listbox(self.main)
            i = 0
            for player in self.playerlist:
                self.lstPlayerListe.insert(i, player["username"] + "  " +  str(player["playing"]))
                i+=1
            self.lstPlayerListe.pack()
            self.cmdConnect = Button(self.main, width=10, command=self.connet_to_player, text="Connect")
            self.cmdConnect.pack(side=RIGHT)
            self.txtScreen.insert(END, "connected as " + str(player["username"]))
            self.main.update()
            print("updated")
        except:
            pass


    def connet_to_player(self):

        playernumber=int(self.lstPlayerListe.curselection()[0])
        print(self.playerlist[playernumber]["username"])
        self.api.connectToPlayer(self.playerlist[playernumber]["username"])
        self.txtScreen.insert(END, "wait for your connection...")



gamestation = Gui()
