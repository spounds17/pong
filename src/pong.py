import math, pygame, sys
from pygame.locals import *

import os, sys, inspect

print os.name
if os.name == 'nt': # Windows    
    print "Windows OS detected"
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    lib_dir= '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
    sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))    
else:
    print "MAC OS detected"
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    lib_dir = os.path.abspath(os.path.join(src_dir,'../lib'))    
    sys.path.insert(0, lib_dir)
    
import time, thread
import Leap


WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 700
LINE_THICKNESS = 10
PADDLE_SIZE = 150
PADDLE_OFFSET = 60

GREEN = (34,139,34)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


RIGHT_HAND_X_OFFSET = 750.0
RIGHT_HAND_Y_OFFSET = 200.0

HAND_OFFSET = 150.0

LEFT_HAND_X_OFFSET = -200.0
LEFT_HAND_Y_OFFSET = 100.0

RIGHT = WINDOW_HEIGHT/HAND_OFFSET * 2
LEFT = -WINDOW_HEIGHT/HAND_OFFSET * 2
UP = -WINDOW_HEIGHT/HAND_OFFSET * 2
DOWN = WINDOW_HEIGHT/HAND_OFFSET * 2

def drawArena():
    DISPLAY_SURF.fill(GREEN)
    pygame.draw.rect(DISPLAY_SURF, WHITE, ((0,0),
                    (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2 )
    pygame.draw.line(DISPLAY_SURF, WHITE, ((WINDOW_WIDTH/2),0),
                    ((WINDOW_WIDTH/2),WINDOW_HEIGHT), (LINE_THICKNESS/4))


def drawPaddle(paddle, color):
    if paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
            paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS
    elif paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS
    if color == "RED":
        pygame.draw.rect(DISPLAY_SURF, RED, paddle)
    elif color == "BLUE":
        pygame.draw.rect(DISPLAY_SURF, BLUE, paddle)
    else:
        pygame.draw.rect(DISPLAY_SURF, WHITE, paddle)


def movePaddle(paddle, deltaY, deltaX):
   
    paddle.y = WINDOW_HEIGHT/2-math.floor(deltaY)
    paddle.x = WINDOW_HEIGHT/2-math.floor(deltaX)
    if paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
            paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS
    elif paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS

def drawBall(ball):
    pygame.draw.rect(DISPLAY_SURF, WHITE, ball)


def moveBall(ball, xDir, yDir, speed):
    ball.x += math.floor(speed*xDir)
    ball.y += math.floor(speed*yDir)
    return ball


def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top <= (LINE_THICKNESS) or ball.bottom >= (WINDOW_HEIGHT - LINE_THICKNESS):
        ballDirY *= (-1)
    if ball.left <= (LINE_THICKNESS) or ball.right >= (WINDOW_WIDTH - LINE_THICKNESS):
        ballDirX *= (-1)
    return ballDirX, ballDirY


def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ball.colliderect(paddle1):
        return -1
    if ball.colliderect(paddle2):
        return -1
    return 1


def checkPointScored(ball, score1, score2, ballDirX):
    if ball.left <= LINE_THICKNESS:
        return 2
    elif ball.right >= WINDOW_WIDTH - LINE_THICKNESS:
        return 1
    else:
        return 0


def displayScore(score1, score2):
    resultSurf1 = BASIC_FONT.render('Left Hand = %s' %(score1), True, WHITE)
    resultRect1 = resultSurf1.get_rect()
    resultRect1.topleft = (35, 35)
    DISPLAY_SURF.blit(resultSurf1, resultRect1)

    resultSurf2 = BASIC_FONT.render('Right Hand = %s' %(score2), True, WHITE)
    resultRect2 = resultSurf2.get_rect()
    resultRect2.topleft = (WINDOW_WIDTH - 170, 35)
    DISPLAY_SURF.blit(resultSurf2, resultRect2)


def reset():
    ballx = WINDOW_WIDTH/2 - LINE_THICKNESS/2
    bally = WINDOW_HEIGHT/2 - LINE_THICKNESS/2

def main():
    pygame.init()
    controller = Leap.Controller()
    frame = controller.frame()
    while(not frame.is_valid):
        frame = controller.frame()
    global DISPLAY_SURF
    global BASIC_FONT, BASIC_FONT_SIZE
    BASIC_FONT_SIZE = 20
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    score1=0
    score2=0

    ballx = WINDOW_WIDTH/2 - LINE_THICKNESS/2
    bally = WINDOW_HEIGHT/2 - LINE_THICKNESS/2

    playerOnePosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    playerTwoPosition = (WINDOW_HEIGHT - PADDLE_SIZE) / 2

    ballDirX = LEFT
    ballDirY = UP
    
    speed = 1    

    playerOnePaddle = pygame.Rect(PADDLE_OFFSET, playerOnePosition,
                                  LINE_THICKNESS, PADDLE_SIZE)
    playerTwoPaddle = pygame.Rect(WINDOW_WIDTH - PADDLE_OFFSET - LINE_THICKNESS,
                                  playerTwoPosition, LINE_THICKNESS,
                                  PADDLE_SIZE)
    ball = pygame.Rect(ballx, bally, LINE_THICKNESS, LINE_THICKNESS)

    drawArena()
    drawPaddle(playerOnePaddle, "BLUE")
    drawPaddle(playerTwoPaddle, "RED")
    drawBall(ball)

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        drawArena()
        drawPaddle(playerOnePaddle, "RED")
        drawPaddle(playerTwoPaddle, "BLUE")
        drawBall(ball)

        frame = controller.frame()
        if frame.is_valid:
            for hand in frame.hands:
                handType = "Left hand" if hand.is_left else "Right hand"
                if handType == "Left hand":
                    #we are player 1
                    position = hand.palm_position
                    #print "positiony1 is %s" %(position.y-HAND_OFFSET)
                    deltaX = (position.y-LEFT_HAND_Y_OFFSET) 
                    deltaY = (-position.x-LEFT_HAND_X_OFFSET) 
                    movePaddle(playerOnePaddle, deltaX, deltaY)
                    
                else:
                    #we are player 2
                    position = hand.palm_position
                    #print "positiony2 is %s" %(position.y-HAND_OFFSET)
                    deltaY = (position.y-RIGHT_HAND_Y_OFFSET) 
                    deltaX = (-position.x-RIGHT_HAND_X_OFFSET) 
                    movePaddle(playerTwoPaddle, deltaY, deltaX)


        ball = moveBall(ball, ballDirX, ballDirY, speed)

        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)

        ballDirX = ballDirX * checkHitBall(ball, playerOnePaddle, playerTwoPaddle, ballDirX)

        point = checkPointScored(ball, score1, score2, ballDirX)
        if point == 1:
            score1+=1
            speed +=.3
            ball.x = WINDOW_WIDTH/2 - LINE_THICKNESS/2
            ball.y = WINDOW_HEIGHT/2 - LINE_THICKNESS/2
        if point == 2:
            score2+=1
            speed += .3
            ball.x = WINDOW_WIDTH/2 - LINE_THICKNESS/2
            ball.y = WINDOW_HEIGHT/2 - LINE_THICKNESS/2
        displayScore(score1, score2)


        pygame.display.update()

if __name__=='__main__':
    main()
