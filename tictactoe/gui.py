
from tkinter import *
import threading
from gameserver.netgameapi import *
import tictactoe


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



        self.main.mainloop()

    def connect(self):
        username = self.txtInput.get()
        self.txtScreen.insert(END, "connecting...\n")

        self.api = NetGameApi(username, "tictactoe", lambda: self.reciever)
        self.tcpthread = Thread(name='tcp', target=self.api.startReceiving())
        #self.tcpthread.start()
        self.api.makeConnection()
        # except:
        #     self.txtScreen.insert(END, "Connection failed!\n")


    def reciever(self, data):

        print(data)

    def initialize_tictactoe(self):
        global actionlist
        actionlist = [0,0,0,0,0,0,0,0,0]
        self.tictactoe = tictactoe.TicTacToe()




gamestation = Gui()
