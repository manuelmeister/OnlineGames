import socket
from threading import Thread
from tkinter import *
import time


class Controller(object):
    def __init__(self):
        Thread.__init__(self)
        self.model = Model('localhost', 12345)
        self.view = View()

        self.view.start()
        self.model.connect()

        self.view.cmdSubmit.bind_class("Button", "<Button-1>", self.submitMessage)
        self.view.cmdSubmit.bind_class("Entry", "<Return>", self.submitMessage)

        self.tcpthread = Thread(name='tcp', target=self.startReceiving())
        self.tcpthread.start()

    def newInstance(self):
        self.model = Model('localhost', 12345)
        self.model.connect()
        self.tcpthread = Thread(name='tcp', target=self.startReceiving())
        self.tcpthread.start()

    def submitMessage(self, event):
        message = self.view.txtInput.get()
        if message == 'exit':
            self.model.close()
            sys.exit()
        self.model.send(message)
        self.view.txtInput.delete(0, END)

    def startReceiving(self):
        data_received = True
        while data_received:
            data_received = self.model.receive()
            if data_received == b"/reconnect":
                self.model.close()
                self.newInstance()
                break
            self.view.writeLine(data_received.decode("utf-8"))
            time.sleep(.5)

class View(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.app = None
        self.txtChat = None
        self.txtInput = None
        self.cmdSubmit = None

    def callback(self):
        self.app.quit()

    def run(self):
        self.app = Tk()
        self.app.protocol("WM_DELETE_WINDOW", self.callback())

        self.app.title("ChatUp")

        self.txtChat = Text(self.app, height=20, width=50, bg="#bbbbbb")
        self.txtChat.pack(side=TOP)

        self.txtInput = Entry(self.app, width=50)
        self.txtInput.pack(side=LEFT)

        self.cmdSubmit = Button(self.app, width=10, text="Submit")
        self.cmdSubmit.pack(side=RIGHT)

        self.app.mainloop()

    def writeLine(self, strMessage):
        self.txtChat.insert(END, strMessage + "\n")
        self.txtChat.see(END)


class Model(object):
    def __init__(self, host, port):
        Thread.__init__(self)
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
        data = self.sock.recv(64)
        return data

    def send(self, content):
        self.sock.sendto(bytes(content, encoding='utf-8'), self.conn)


if __name__ == "__main__":
    controller = Controller()