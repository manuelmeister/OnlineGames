from gameserver.netgameapi import *

import pygame, sys
import pygame.locals



class TicTacToe:
    def __init__(self):
        #initial board
        pygame.init()
        self.screen_width=600
        self.screen_height=600
        self.board = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.pos0=list(range(0, int(self.screen_width/3)))
        self.pos1=list(range(int(self.screen_width/3), int(self.screen_width/3*2)))
        self.pos2=list(range(int(self.screen_width/3*2), self.screen_width))

        #colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # basic font
        self.basicFont = pygame.font.SysFont(None, 200)

        self.startdisplay()

        # draw the window onto the screen
        pygame.display.update()

        # actionlist


    def startdisplay(self):
        self.startFont = pygame.font.SysFont(None, 100)
        self.board.fill(self.WHITE)
        text = self.startFont.render('Start TicTacToe', True, self.BLACK, self.WHITE)
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
        pygame.draw.line(self.board, self.BLACK, [((1/3)*600),0], [((1/3)*600),600], 2)
        pygame.draw.line(self.board, self.BLACK, [((2/3)*600),0], [((2/3)*600),600], 2)
        pygame.draw.line(self.board, self.BLACK, [0,((1/3)*600)], [600,((1/3)*600)], 2)
        pygame.draw.line(self.board, self.BLACK, [0,((2/3)*600)], [600,((2/3)*600)], 2)
        pygame.draw.line(self.board, self.BLACK, [0,0], [0,600], 2)

        self.inputfield = list(range(9))
        self.outputfield = list(range(9))
        for i in range(9):

            # Generate ButtonFields
            xposition=200*(i%3)+1
            if i in [0,1,2]:
                yposition=1
            if i in [3,4,5]:
                yposition=201
            if i in [6,7,8]:
                yposition=401
            self.inputfield[i] = pygame.draw.rect(self.board, self.WHITE, (xposition,yposition,198,198))

            # textSurfaceObj = self.basicFont.render('X', True, self.RED)
            # self.field[i] = textSurfaceObj.get_rect()
            # self.field[i].center = (xposition,yposition)
            # self.board.blit(textSurfaceObj, self.field[i])

        pygame.display.update()
        self.mainloop()

    def action(self, fieldnumber):

        for i in range(1):
            if not actionlist[fieldnumber] == 0:
                break
            if self.player == 1:
                self.X("X", fieldnumber)
            elif self.player == 2:
                self.X("O", fieldnumber)
            # for i in actionlist:
            #     if not i ==

    def X(self, character, fieldnumber):

        # Create OutputFields
        xposition=200*(fieldnumber%3)+50
        if fieldnumber in [0,1,2]:
            yposition=40
        if fieldnumber in [3,4,5]:
            yposition=240
        if fieldnumber in [6,7,8]:
            yposition=440
        self.outputfield[fieldnumber] = pygame.draw.rect(self.board, self.WHITE, (xposition,yposition,100,100))


        text = self.basicFont.render(character, True, self.BLACK, self.WHITE)
        # self.field[fieldnumber].centerx = 100
        # self.field[fieldnumber].centery = 100
        self.board.blit(text, self.outputfield[fieldnumber])
        pygame.display.update()
        if self.player == 1:
            actionlist[fieldnumber]=1
            self.player = 2
        elif self.player == 2:
            actionlist[fieldnumber]=2
            self.player = 1
        print(actionlist)

    def mainloop(self):
        self.player = 1
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for i in range(9):
                    if event.type == pygame.MOUSEBUTTONDOWN and self.inputfield[i].collidepoint(pygame.mouse.get_pos()):
                        self.action(i)


                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     print(pygame.mouse.get_pos())
                #     mousex=pygame.mouse.get_pos()[0]
                #     mousey=pygame.mouse.get_pos()[1]
                #     self.action(mousex, mousey)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos0 and mousey in self.pos0:
                #     self.action(0,0)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos0 and mousey in self.pos1:
                #     self.action(0,1)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos0 and mousey in self.pos2:
                #     self.action(0,2)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos1 and mousey in self.pos0:
                #     self.action(1,0)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos1 and mousey in self.pos1:
                #     self.action(1,1)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos1 and mousey in self.pos2:
                #     self.action(1,2)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos2 and mousey in self.pos0:
                #     self.action(2,0)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos2 and mousey in self.pos1:
                #     self.action(2,1)
                # if event.type == pygame.MOUSEBUTTONDOWN and mousex in self.pos2 and mousey in self.pos2:
                #     self.action(2,2)


global actionlist
actionlist = [0,0,0,0,0,0,0,0,0]
tictactoe = TicTacToe()








