import pygame, sys
import pygame.locals
from tkinter import Button



class VierGewinnt:
    def __init__(self):
        #initial board
        pygame.init()
        self.screen_width=700
        self.screen_height=600
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))
           
        self.x = [5,5,5,5,5,5,5]
        
             
        self.pos0=list(range(0, int(self.screen_width/7*1)))
        self.pos1=list(range(int(self.screen_width/7*1), int(self.screen_width/7*2)))
        self.pos2=list(range(int(self.screen_width/7*2), int(self.screen_width/7*3)))
        self.pos3=list(range(int(self.screen_width/7*3), int(self.screen_width/7*4)))
        self.pos4=list(range(int(self.screen_width/7*4), int(self.screen_width/7*5)))
        self.pos5=list(range(int(self.screen_width/7*5), int(self.screen_width/7*6)))
        self.pos6=list(range(int(self.screen_width/7*6), int(self.screen_width/7*7)))

        #colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # basic font
        self.basicFont = pygame.font.SysFont(None, 100)

        self.startdisplay()

        # draw the window onto the screen
        pygame.display.update()

        # actionlist


    def startdisplay(self):
        self.startFont = pygame.font.SysFont(None, 100)
        self.board.fill(self.WHITE)
        text = self.startFont.render('Start 4-Gewinnt', True, self.BLACK, self.WHITE)
        textRect = text.get_rect()
        textRect.centerx = self.board.get_rect().centery
        textRect.centery = self.board.get_rect().centery
        self.board.blit(text, textRect)
        pygame.display.update()
        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = True
                    break

        self.initialdisplay()


    def initialdisplay(self):
        self.board.fill(self.WHITE)
        pygame.draw.line(self.board, self.BLACK, [0,0], [0,700], 2)
        for i in range(1,8):
            pygame.draw.line(self.board, self.BLACK, [((i/7)*700),0], [((i/7)*700),700], 2)
        for j in range(1,7):
            pygame.draw.line(self.board, self.BLACK, [0,((j/6)*600)], [700,((j/6)*600)], 2)
        pygame.display.update()
        self.mainloop()

            
    def action(self, xpos, ypos, player):
        if player == 1:
            self.O("O", xpos, ypos, self.RED)
        if player == 2:
            self.O("O", xpos, ypos, self.BLUE)


    def O(self, character, xpos, ypos, Ocolor):
            text = self.basicFont.render(character, True, Ocolor, self.WHITE)
            textRect = text.get_rect()
            textRect.centerx = xpos*100+50
            textRect.centery = ypos*100+50
            self.board.blit(text, textRect)
            pygame.display.update()
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

    def mainloop(self):
        self.player = 1
        while True:
            for event in pygame.event.get():
                mouseX=pygame.mouse.get_pos()[0]
                mouseY=pygame.mouse.get_pos()[1]
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos0:
                    self.action(0,self.x[0], self.player)
                    self.x[0] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos1:
                    self.action(1,self.x[1], self.player)
                    self.x[1] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos2:
                    self.action(2,self.x[2], self.player)
                    self.x[2] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos3:
                    self.action(3,self.x[3], self.player)
                    self.x[3] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos4:
                    self.action(4,self.x[4], self.player)
                    self.x[4] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos5:
                    self.action(5,self.x[5], self.player)
                    self.x[5] -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and mouseX in self.pos6:
                    self.action(6,self.x[6], self.player)
                    self.x[6] -= 1


VierGewinnt = VierGewinnt()





