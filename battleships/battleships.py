import pygame, sys, time

class Battleships:
    def __init__(self):
        pygame.init()


        pygame.display.set_caption("battleships")


        self.screen_width=800
        self.screen_height=900
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BSFont = pygame.font.SysFont(None, 100)

        self.board.fill(self.WHITE)

        TITLE_SURF, TITLE_RECT = self.makeText('Battleships', self.BLACK, self.WHITE, 10, 0)

        self.board.blit(TITLE_SURF, TITLE_RECT)

        self.coords=self.create_coords(self.screen_width,10,10,0,100)
        print(self.coords)
        self.actionlist=[]
        for i in range(self.coords["xcount"]*self.coords["xcount"]):
            self.actionlist.append(0)
        print(self.actionlist)

        pygame.display.update()


        self.initial_gui()

        self.set_your_game()

        self.mainloop()


    def set_your_game(self):
        TITLE_SURF, TITLE_RECT = self.makeText('Battleships', self.BLACK, self.WHITE, 10, 0)

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
        print(self.squarecount)
        for i in range(self.squarecount):
            pygame.draw.rect(self.board, self.WHITE, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
            pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)
            time.sleep(0.01)
            pygame.display.update()

    def fill_rect(self, i):
        pygame.draw.rect(self.board, self.BLUE, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]))
        pygame.draw.rect(self.board, self.BLACK, (self.coords[i][0],self.coords[i][1],self.coords["squarelength"],self.coords["squarelength"]),5)
        pygame.display.update()
        self.actionlist[i]=1
        print(self.actionlist)

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
                        self.fill_rect(i)





battleships = Battleships()
