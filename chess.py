import numpy as np
import pygame
from Chessboard import Chessboard
import time
import os  # for path check
import random
import sys

# images:
# By en:User:Cburnett - CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=20363776
#


# setup code:
pygame.init()

# leave smaller size at 680 for 60x60 images
winwidth = 700
winheight = 680
pgwin = pygame.display.set_mode((winwidth, winheight))
pygame.display.set_caption("Dave's Chess")
pygame.display.update()

try:
    PATH = "c:/Users/davep/OneDrive/Desktop/Prog/py/gameboard/"
    os.listdir(PATH)
except IOError:
    PATH = "Z:/Dave P/python/gameboard/"

# winners={'white':0,'black':0,'draw':0}
playercolor, aicolor = 'white', 'black'
currentplayer = ''

gameover = False
newgame = True
message1, message2 = '', ''

while True:
    if newgame:
        # game start:
        chessboard = Chessboard(
            pygamewindow=pgwin, imagepath=PATH, setup='standard')
        chessboard.config(bgcolors=('grey', 'red'))
        playerclick = []
        currentplayer = 'white'
        waittime = 1        # in seconds
        starttime = time.time()   # in seconds. this value is only used if ai goes first
        gameover = False
        newgame = False
        message1, message2 = '', ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif (event.type == pygame.MOUSEBUTTONUP):
            if event.button == 1:
                if gameover:     # any click starts a new game
                    newgame = True    # we will start new game at next frame
                elif currentplayer == playercolor:
                    r, c = chessboard.cellfromcoords((*event.pos))
                    if r is not None and c is not None:
                        if len(playerclick) == 0:
                            piece = chessboard[r, c]
                            if piece is not None:
                                # if piece.player == playercolor:    comment this to move either color
                                playerclick.append((r, c))
                                chessboard.highlight(r, c)
                        else:
                            if (r, c) == playerclick[0]:
                                # re-click same cell
                                chessboard.unhighlight(*playerclick[0])
                                playerclick = []
                            else:
                                valid = chessboard.validmoves(*playerclick[0])
                                if (playerclick[0], (r, c)) in valid:
                                    # make the move
                                    chessboard.move(*playerclick[0], r, c)
                                    chessboard.unhighlight(*playerclick[0])
                                    playerclick = []
                                    currentplayer = 'black' if currentplayer == 'white' else 'white'
                                    starttime = time.time()   # in seconds
                                    winner = chessboard.getwinner()
                                    if winner:
                                        message2 = "Checkmate! You win" if winner == 'white' else "Checkmate... Computer wins"
                                        gameover = True
    if gameover:
        message1 = 'Click to play again'
    elif currentplayer == playercolor:
        message1 = 'Click piece to move' if len(
            playerclick) == 0 else 'Click destination'
    else:    # elif currentplayer == aicolor:
        message1 = 'Computer thinking...'
        if time.time()-starttime > waittime:
            possible = []
            for piece in chessboard.pieces[aicolor]:
                for valid in chessboard.validmoves(*chessboard.pieces[piece.player][piece]):
                    possible.append(valid)
            move = random.choice(possible)
            # make the move
            chessboard.move(*move[0], *move[1])
            currentplayer = 'black' if currentplayer == 'white' else 'white'
            winner = chessboard.getwinner()
            if winner:
                message2 = "Checkmate! You win" if winner == 'white' else "Checkmate... Computer wins"
                gameover = True
        else:
            # just wait
            pass

    chessboard.redraw(message1, message2)

pygame.quit()
