import math, pygame, sys
from pygame.locals import *

import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir,'../lib'))

sys.path.insert(0, lib_dir)
import time, thread
import Leap

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
LINE_THICKNESS = 30
PADDLE_SIZE = 100
PADDLE_OFFSET = 60
HAND_OFFSET = 200.0

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def movePaddle(paddle, deltaY):
    #print "moving paddle from y=%s by %s to %s" % (paddle.y, -math.floor(deltaY), paddle.y+math.floor(deltaY))
    paddle.y = WINDOW_HEIGHT/2-math.floor(deltaY)
    if paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
            paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS
    elif paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS

def drawPaddle(paddle):
    pygame.draw.rect(DISPLAY_SURF, WHITE, paddle)

def drawArena():
    DISPLAY_SURF.fill(BLACK)
    pygame.draw.rect(DISPLAY_SURF, WHITE, ((0,0),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2 )
    pygame.draw.line(DISPLAY_SURF, WHITE, ((WINDOW_WIDTH/2),0),
                    ((WINDOW_WIDTH/2),WINDOW_HEIGHT), (LINE_THICKNESS/4))

def main():
    pygame.init()
    controller = Leap.Controller()
    frame = controller.frame()
    while(not frame.is_valid):
        frame = controller.frame()    
    
    
                
    global DISPLAY_SURF
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    
    playerOnePosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    playerTwoPosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    
    playerOnePaddle = pygame.Rect(PADDLE_OFFSET, playerOnePosition, LINE_THICKNESS, PADDLE_SIZE)
    playerTwoPaddle = pygame.Rect(WINDOW_WIDTH - PADDLE_OFFSET - LINE_THICKNESS, playerTwoPosition, LINE_THICKNESS, PADDLE_SIZE)    

    drawArena()
    drawPaddle(playerOnePaddle)
    
    DISPLAY_SURF.fill(BLACK)
    pygame.draw.rect(DISPLAY_SURF, WHITE, ((0,0), (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2 )
    pygame.draw.line(DISPLAY_SURF, WHITE, ((WINDOW_WIDTH/2),0), ((WINDOW_WIDTH/2),WINDOW_HEIGHT), (LINE_THICKNESS/4))

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        drawArena()
        drawPaddle(playerOnePaddle)
        frame = controller.frame()
        if frame.is_valid:
                for hand in frame.hands:
                    handType = "Left hand" if hand.is_left else "Right hand"
                    if handType == "Left hand":
                        #we are player 1
                        position = hand.palm_position
                        #print "positiony1 is %s" %(position.y-HAND_OFFSET)
                        deltaY = (position.y-HAND_OFFSET)
                        movePaddle(playerOnePaddle, deltaY)
                    else:
                        #we are player 2
                        position = hand.palm_position
                        #print "positiony2 is %s" %(position.y-HAND_OFFSET)
                        deltaY = (position.y-HAND_OFFSET)
                        movePaddle(playerTwoPaddle, deltaY)          
        
        pygame.display.update()

if __name__=='__main__':
    main()
