import pygame, sys, time
from random import *

class Minesweeper:
    def __init__(self):
        pygame.init()


        pygame.display.set_caption("minesweeper")


        self.screen_width=800
        self.screen_height=900
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREY = (150, 150, 150)
        self.BSFontheigt=100
        self.BSFont = pygame.font.SysFont(None, self.BSFontheigt)

        self.board.fill(self.WHITE)

        TITLE_SURF, TITLE_RECT = self.makeText('Minesweeper', self.BLACK, self.WHITE, 10, 0)

        self.board.blit(TITLE_SURF, TITLE_RECT)

        self.coords=self.create_coords(self.screen_width,10,10,0,100)
        print(self.coords)

        self.actionlist=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.actionlist.append(0)
        print("actionlist:    ", self.actionlist)

        self.actionlist2=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.actionlist2.append(0)
        print("actionlist2:   ", self.actionlist2)

        self.mineslist = []
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.mineslist.append(0)
        self.set_random_mines()
        print("mineslist:     ", self.mineslist)

        self.minestestlist = []
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.minestestlist.append(0)
        self.test_rect_list()
        print("minestestlist: ", self.minestestlist)

        pygame.display.update()
        self.initial_gui()

        self.mainloop()


    def set_random_mines(self):
        for i in range(5):
            mine_position = randint(0,self.coords["xcount"]*self.coords["ycount"]-1)
            self.mineslist[mine_position]=1
            self.fill_rect(mine_position, self.RED)
        return self.mineslist




    def create_coords(self, windowlength, xcount, ycount, top=0, left=0):
        coords = {}
        squarelength=int(windowlength/xcount)
        coords["squarelength"]=squarelength
        coords["xcount"]=xcount
        coords["ycount"]=ycount

        for i in range(ycount):
            for j in range(xcount):
                coords[xcount*i+j]=[j*squarelength+top, i*squarelength+left]

        return coords


    def test_rect_list(self):
        xcount=self.coords["xcount"]
        for i in range(len(self.minestestlist)):
            counter=0
            test_list=[i-1-xcount+0, i-1-xcount+1, i-1-xcount+2, i-1, i+1, i+1+xcount+0, i+1+xcount-1, i+1+xcount-2]
            for j in test_list:
                try:

                    if self.mineslist[j] == 1 and j >= 0 and j <= 99:
                        counter+=1
                except:
                    pass
            self.minestestlist[i] = counter

    def test_rect(self, i):
        print(i)
        xcount=self.coords["xcount"]
        test_list=[i-1-xcount+0, i-1-xcount+1, i-1-xcount+2, i-1, i+1, i+1+xcount+0, i+1+xcount-1, i+1+xcount-2]
        if self.actionlist[i]==0:
            if self.minestestlist[i] > 0:
                self.fill_rect(i, self.GREY, str(self.minestestlist[i]))
                self.actionlist[i]=1
            elif self.minestestlist[i] == 0:
                self.fill_rect(i, self.BLUE)
                self.actionlist[i]=1
                for j in test_list:
                    self.test_rect(j)

        else:
            return







    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def makeText(self, text, color, bgcolor, top, left):
        # create the Surface and Rect objects for some text.
        textSurf = self.BSFont.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)



    def initial_gui(self):
        self.squarecount=self.coords["xcount"]*self.coords["ycount"]
        for i in range(self.squarecount):
            pygame.draw.rect(self.board, self.WHITE, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)
            time.sleep(0.01)
            pygame.display.update()



    def choose_rect(self, i, color, text=""):

        self.actionlist[i]=1
        if self.actionlist[i] == self.mineslist[i]:
            pygame.draw.rect(self.board, self.RED, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)
            self.game_over()
        pygame.draw.rect(self.board, color, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
        pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)

        if text!="":
            TITLE_SURF, TITLE_RECT = self.makeText(text, self.BLACK, self.GREY, self.coords[i][0]+10,self.coords[i][1]+5)

            self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()

        self.test_rect(i)

        self.actionlist[i]=1



    def fill_rect(self, i, color, text=""):
        pygame.draw.rect(self.board, color, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
        pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)

        if text!="":
            TITLE_SURF, TITLE_RECT = self.makeText(text, self.BLACK, self.GREY, self.coords[i][0]+10,self.coords[i][1]+5)
            self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()






    def game_over(self):


        counter=0
        for i in self.mineslist:

            if i == 1 and self.actionlist2[counter] == 0:
                self.fill_rect(counter, self.RED)
            elif i == 0 and self.actionlist2[counter] == 0:
                self.fill_rect(counter, self.BLUE)
            counter+=1

        TITLE_SURF, TITLE_RECT = self.makeText('GAME OVER', self.BLACK, self.WHITE, 100, self.screen_height/2-self.BSFontheigt)
        self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()



        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def mainloop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                mousex=pygame.mouse.get_pos()[0]
                mousey=pygame.mouse.get_pos()[1]

                for i in range(self.squarecount):

                    xrange=range(self.coords[i][0],self.coords[i][0]+self.coords["squarelength"])
                    yrange=range(self.coords[i][1],self.coords[i][1]+self.coords["squarelength"])
                    if event.type == pygame.MOUSEBUTTONDOWN and mousex in xrange and mousey in yrange:
                        if self.actionlist[i]==0:
                            self.choose_rect(i, self.BLUE)





minesweeper = Minesweeper()
