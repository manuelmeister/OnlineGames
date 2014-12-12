import pygame, sys, time
from random import *

class Board:
    def __init__(self):
        pygame.init()

        self.title="Board"
        pygame.display.set_caption(self.title)


        self.screen_width=1000
        self.header_height=200
        self.xcount=30
        self.ycount=20

        self.borderwidth=3 #in pixel

        #colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREY = (150, 150, 150)

        self.screen_height=int(self.screen_width/self.xcount)*self.ycount+self.header_height
        self.MWFontheigt=int(self.screen_width/self.xcount)
        self.MWTextFontheigt=pygame.font.SysFont(None, int(self.screen_width/self.xcount))
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.MWFont = pygame.font.SysFont(None, self.MWFontheigt)
        self.TitleFont = pygame.font.SysFont(None, int(self.header_height/2+1))

        self.board.fill(self.WHITE)

        TITLE_SURF, TITLE_RECT = self.makeText(self.title, self.BLACK, self.WHITE, 10, 0, self.TitleFont)

        self.board.blit(TITLE_SURF, TITLE_RECT)

        self.create_coords(self.screen_width,self.xcount,self.ycount,0,self.header_height)
        print(self.coords)

        self.user_action_list=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.user_action_list.append(0)
        print("actionlist:    ", self.user_action_list)

        self.automatic_action_list=[]
        for i in range(self.coords["xcount"]*self.coords["ycount"]):
            self.automatic_action_list.append(0)
        print("actionlist2:   ", self.automatic_action_list)

        pygame.display.update()
        self.initial_gui()

        self.mainloop()







    def create_coords(self, windowlength, xcount, ycount, top=0, left=0):
        self.coords = {}
        squarelength=int(windowlength/xcount)
        self.coords["squarelength"]=squarelength
        self.coords["xcount"]=xcount
        self.coords["ycount"]=ycount

        for i in range(ycount):
            for j in range(xcount):
                self.coords[(j, i)] = [j*squarelength+top, i*squarelength+left]
                #self.coords[xcount*i+j]=[j*squarelength+top, i*squarelength+left]


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
        for i in range(self.xcount):
            for j in range(self.ycount):
                pygame.draw.rect(self.board, self.WHITE, (self.coords[(i, j)][0],self.coords[(i, j)][1],self.coords["squarelength"],self.coords["squarelength"]))
                pygame.draw.rect(self.board, self.BLACK, (self.coords[(i, j)][0],self.coords[(i, j)][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)
                time.sleep(0.0001)
                pygame.display.update()




    def fill_rect(self, i, j, color, text=""):
        if i >= 0 and i <= self.coords["xcount"]*self.coords["xcount"]-1:
            pygame.draw.rect(self.board, color, (self.coords[(i, j)][0],self.coords[(i, j)][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[(i, j)][0],self.coords[(i, j)][1],self.coords["squarelength"],self.coords["squarelength"]),self.borderwidth)

            if text!="":
                TITLE_SURF, TITLE_RECT = self.makeText(text, self.BLACK, self.GREY, self.coords[(i, j)][0]+10,self.coords[(i, j)][1]+5, self.MWTextFontheigt)
                self.board.blit(TITLE_SURF, TITLE_RECT)

        pygame.display.update()


    def game_over(self):
        pass


    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                mousex=pygame.mouse.get_pos()[0]
                mousey=pygame.mouse.get_pos()[1]

                for i in range(self.xcount):
                    for j in range(self.ycount):

                        xrange=range(self.coords[(i, j)][0],self.coords[(i, j)][0]+self.coords["squarelength"])
                        yrange=range(self.coords[(i, j)][1],self.coords[(i, j)][1]+self.coords["squarelength"])
                        if event.type == pygame.MOUSEBUTTONDOWN and mousex in xrange and mousey in yrange:
                            if self.user_action_list[i]==0:
                                self.fill_rect(i, j, self.BLUE)





board = Board()

