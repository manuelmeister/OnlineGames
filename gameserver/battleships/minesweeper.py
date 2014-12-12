import pygame, sys, time
from random import *

class Minesweeper:
    def __init__(self):
        pygame.init()


        pygame.display.set_caption("minesweeper")


        self.screen_width=1000
        self.header_height=200
        self.xcount=30
        self.ycount=20
        self.screen_height=int(self.screen_width/self.xcount)*self.ycount+self.header_height
        self.borderwidt=10 #in % of square width
        self.minescount=int((self.xcount*self.ycount)/2)
        self.MWFontheigt=int(self.screen_width/self.xcount)
        self.MWTextFontheigt=pygame.font.SysFont(None, int(self.screen_width/self.xcount))
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREY = (150, 150, 150)

        self.MWFont = pygame.font.SysFont(None, self.MWFontheigt)
        self.TitleFont = pygame.font.SysFont(None, int(self.header_height/2+1))

        self.board.fill(self.WHITE)

        TITLE_SURF, TITLE_RECT = self.makeText('Minesweeper', self.BLACK, self.WHITE, 10, 0, self.TitleFont)

        self.board.blit(TITLE_SURF, TITLE_RECT)

        self.coords=self.create_coords(self.screen_width,self.xcount,self.ycount,0,self.header_height)
        print(self.coords)

        self.user_action_lilst=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.user_action_lilst.append(0)
        print("actionlist:    ", self.user_action_lilst)

        self.automatic_action_list=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.automatic_action_list.append(0)
        print("actionlist2:   ", self.automatic_action_list)

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

        #for research:
        print("debug:         ", list(range(self.xcount*self.ycount)))

        pygame.display.update()
        self.initial_gui()

        self.mainloop()


    def set_random_mines(self):
        for i in range(self.minescount):
            mine_position = randint(0,self.coords["xcount"]*self.coords["ycount"]-1)
            self.mineslist[mine_position]=1
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

                    #if not ()
                    if not (((i%self.xcount == self.xcount-1) and (j%self.xcount == 0)) or ((i%self.xcount == 0) and (j%self.xcount == self.xcount-1))):
                    #if (i%self.xcount) + (j%xcount) + 1 != self.xcount:
                        if self.mineslist[j] == 1 and j >= 0 and j <= self.coords["xcount"]*self.coords["xcount"]-1:
                            counter+=1
                except:
                    pass
            self.minestestlist[i] = counter

    def test_rect(self, i):
        print(i)
        xcount=self.coords["xcount"]
        test_list=[i-1-xcount+0, i-1-xcount+1, i-1-xcount+2, i-1, i+1, i+1+xcount+0, i+1+xcount-1, i+1+xcount-2]
        if i >= 0 and i <= self.coords["xcount"]*self.coords["ycount"]-1:
            if self.automatic_action_list[i]==0 and self.mineslist[i] != 1:
                if self.minestestlist[i] > 0:
                    self.fill_rect(i, self.GREY, str(self.minestestlist[i]))
                    self.automatic_action_list[i]=1
                elif self.minestestlist[i] == 0:
                    self.fill_rect(i, self.BLUE)
                    self.automatic_action_list[i]=1
                    for j in test_list:
                        self.test_rect(j)

        else:
            return







    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def makeText(self, text, color, bgcolor, top, left, fontstyle):
        # create the Surface and Rect objects for some text.
        textSurf = fontstyle.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)



    def initial_gui(self):
        self.squarecount=self.coords["xcount"]*self.coords["ycount"]
        for i in range(self.squarecount):
            pygame.draw.rect(self.board, self.WHITE, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)
            time.sleep(0.0001)
            pygame.display.update()



    def choose_rect(self, i, color, text=""):

        self.user_action_lilst[i]=1
        if self.user_action_lilst[i] == self.mineslist[i]:
            pygame.draw.rect(self.board, self.RED, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)
            self.game_over()
        pygame.draw.rect(self.board, color, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
        pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)

        if text!="":
            counter_surf, counter_rect = self.makeText(text, self.BLACK, self.GREY, self.coords[i][0]+10,self.coords[i][1]+5, self.MWFont)

            self.board.blit(counter_surf, counter_rect)

        pygame.display.update()

        self.test_win()

        self.test_rect(i)


    def test_win(self):
        for i in range(self.xcount*self.ycount):
            if self.automatic_action_list[i] == 1 or self.user_action_lilst[i] == 1 or self.mineslist[i] == 1:
                pass
            else:
                return
        self.win_screen()

    def win_screen(self):
        TITLE_SURF, TITLE_RECT = self.makeText('You Win!', self.BLACK, self.WHITE, 0, int(self.header_height/2)+1, self.MWTextFontheigt)
        self.board.blit(TITLE_SURF, TITLE_RECT)
        pygame.display.update()
        self.play_again()


    def fill_rect(self, i, color, text=""):
        if i >= 0 and i <= self.coords["xcount"]*self.coords["xcount"]-1:
            pygame.draw.rect(self.board, color, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)

            if text!="":
                TITLE_SURF, TITLE_RECT = self.makeText(text, self.BLACK, self.GREY, self.coords[i][0]+10,self.coords[i][1]+5, self.MWTextFontheigt)
                self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()






    def game_over(self):
        counter=0
        for i in range(len(self.mineslist)):
            if self.mineslist[i] == 1:
                self.fill_rect(counter, self.RED)
            else:
                if self.minestestlist[i] == 0:
                    self.fill_rect(counter, self.BLUE)
                elif self.minestestlist[i] > 0:
                    self.fill_rect(counter, self.GREY, str(self.minestestlist[i]))

            counter+=1



        TITLE_SURF, TITLE_RECT = self.makeText('GAME OVER', self.BLACK, self.WHITE, 0, int(self.header_height/2)+1, self.MWTextFontheigt)
        self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()

        print("actionlist:    ", self.user_action_lilst)
        print("actionlist2:   ", self.automatic_action_list)
        print("mineslist:     ", self.mineslist)
        print("minestestlist: ", self.minestestlist)

        self.play_again()


    def play_again(self):
        again_surf, again_rect = self.makeText("play again", self.BLACK, self.BLUE, int(self.screen_width/2), int(self.header_height/2), self.MWTextFontheigt)

        self.board.blit(again_surf, again_rect)
        pygame.draw.rect(self.board, self.BLACK, (again_rect[0],again_rect[1],again_rect[2],again_rect[3]), self.borderwidth)
        print(again_surf)
        print(again_rect)
        pygame.display.update()
        xrange=range(again_rect[0],again_rect[0]+again_rect[2])
        yrange=range(again_rect[1],again_rect[1]+again_rect[3])

        while True:
            for event in pygame.event.get():
                mousex=pygame.mouse.get_pos()[0]
                mousey=pygame.mouse.get_pos()[1]

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and mousex in xrange and mousey in yrange:
                    self.__init__()


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
                        if self.user_action_lilst[i]==0:
                            self.choose_rect(i, self.BLUE)





minesweeper = Minesweeper()
