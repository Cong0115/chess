from Gameboard import Gameboard
import numpy as np
from PIL import ImageTk, Image
import copy
import pygame
from commonmath import *


class Chesspiece():
    def __init__(self, player='white', pieceid='', image=''):
        self.player = player
        self.pieceid = pieceid
        self.image = image
        self.hasmoved = False
        # e.g.: my_image = pygame.image.load(path_to_image).convert_alpha()

    def getmoves(self, chessboard, row, col):
        return []

    def _orthomoves(self, chessboard, row, col):
        # get all orthogonal moves for piece at row,col
        # i.e. rooks or queens
        ourcolor = chessboard[row, col].player
        orthomoves = []
        # move left
        c = col-1
        while (c >= 0):
            piece = chessboard[row, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                orthomoves.append(((row, col), (row, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                orthomoves.append(((row, col), (row, c)))
                break
            c -= 1
        # move right
        c = col+1
        while (c < chessboard.shape[1]):
            piece = chessboard[row, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                orthomoves.append(((row, col), (row, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                orthomoves.append(((row, col), (row, c)))
                break
            c += 1
        # move up
        r = row-1
        while (r >= 0):
            piece = chessboard[r, col]
            if piece is None:
                # if we see blank space, add the move and keep looking
                orthomoves.append(((row, col), (r, col)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                orthomoves.append(((row, col), (r, col)))
                break
            r -= 1
        # move down
        r = row+1
        while (r < chessboard.shape[0]):
            piece = chessboard[r, col]
            if piece is None:
                # if we see blank space, add the move and keep looking
                orthomoves.append(((row, col), (r, col)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                orthomoves.append(((row, col), (r, col)))
                break
            r += 1
        return orthomoves

    def _diagmoves(self, chessboard, row, col):
        # get all diagonal moves for piece at row,col
        # i.e. bishops or queens
        ourcolor = chessboard[row, col].player
        diagmoves = []
        # move left+up
        r = row-1
        c = col-1
        while (r >= 0) and (c >= 0):
            piece = chessboard[r, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                diagmoves.append(((row, col), (r, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                diagmoves.append(((row, col), (r, c)))
                break
            r -= 1
            c -= 1
        # move right+up
        r = row-1
        c = col+1
        while (r >= 0) and (c < chessboard.shape[1]):
            piece = chessboard[r, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                diagmoves.append(((row, col), (r, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                diagmoves.append(((row, col), (r, c)))
                break
            r -= 1
            c += 1
        # check: move left+down
        r = row+1
        c = col-1
        while (r < chessboard.shape[0]) and (c >= 0):
            piece = chessboard[r, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                diagmoves.append(((row, col), (r, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                diagmoves.append(((row, col), (r, c)))
                break
            r += 1
            c -= 1
        # check: move right+down
        r = row+1
        c = col+1
        while (r < chessboard.shape[0]) and (c < chessboard.shape[1]):
            piece = chessboard[r, c]
            if piece is None:
                # if we see blank space, add the move and keep looking
                diagmoves.append(((row, col), (r, c)))
            elif piece.player == ourcolor:
                # if our piece: don't add the move, stop looking
                break
            else:  # piece must be other player's
                # if we see other player's piece, add the move and stop looking
                diagmoves.append(((row, col), (r, c)))
                break
            r += 1
            c += 1
        return diagmoves


class Pawn(Chesspiece):
    piecevalue = 1

    def __init__(self, player='white', pieceid='', image='', direction=None):
        super().__init__(player, pieceid, image)
        # direction of travel:
        self.direction = direction
        # this will be set to True if we just moved 2 squares:
        self.enpassantready = False
        # first/last rank (row) of travel:
        self.homerank = 6 if direction == -1 else 1
        self.lastrank = 0 if direction == -1 else 7

    def getmoves(self, chessboard, row, col):
        ourcolor = chessboard[row, col].player
        moves = []
        testcapts = [(-1, -1), (-1, 1)
                     ] if self.direction == -1 else [(1, -1), (1, 1)]
        for cc in testcapts:
            r, c = row+cc[0], col+cc[1]
            if r in range(chessboard.shape[0]) and c in range(chessboard.shape[1]):
                piece = chessboard[r, c]
                if piece is not None:
                    if piece.player != ourcolor:
                        # if we see other player's piece, add the move
                        moves.append(((row, col), (r, c)))
        # movedir = -1 if ourcolor == 'white'else 1
        # homerow = 6 if ourcolor == 'white' else 1
        r = row+self.direction
        if r in range(chessboard.shape[0]) and col in range(chessboard.shape[1]):
            if chessboard[r, col] is None:
                # if we see blank space, add the move, and check 2nd space (if we are on home row)
                moves.append(((row, col), (r, col)))
                r = r+self.direction
                # now check 2nd space if possible
                if r in range(chessboard.shape[0]) and row == self.homerank:
                    if chessboard[r, col] is None:
                        # if we see blank space, add the move
                        moves.append(((row, col), (r, col)))
        return moves


class Rook(Chesspiece):
    piecevalue = 5

    def getmoves(self, chessboard, row, col):
        return self._orthomoves(chessboard, row, col)


class Knight(Chesspiece):
    piecevalue = 3

    def getmoves(self, chessboard, row, col):
        ourcolor = chessboard[row, col].player
        moves = []
        testmoves = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                     (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for cm in testmoves:
            r, c = row+cm[0], col+cm[1]
            if r in range(chessboard.shape[0]) and c in range(chessboard.shape[1]):
                piece = chessboard[r, c]
                if piece is None:
                    # if we see blank space, add the move
                    moves.append(((row, col), (r, c)))
                elif piece.player != ourcolor:
                    # if we see other player's piece, add the move
                    moves.append(((row, col), (r, c)))
        return moves


class Bishop(Chesspiece):
    piecevalue = 3

    def getmoves(self, chessboard, row, col):
        return self._diagmoves(chessboard, row, col)


class Queen(Chesspiece):
    piecevalue = 8

    def getmoves(self, chessboard, row, col):
        return self._orthomoves(chessboard, row, col)+self._diagmoves(chessboard, row, col)


class King(Chesspiece):
    piecevalue = 0

    def getmoves(self, chessboard, row, col):
        ourcolor = chessboard[row, col].player
        moves = []
        testmoves = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                     (1, 0), (-1, -1), (0, -1), (1, -1)]
        for cm in testmoves:
            r, c = row+cm[0], col+cm[1]
            if r in range(chessboard.shape[0]) and c in range(chessboard.shape[1]):
                piece = chessboard[r, c]
                if piece is None:
                    # if we see blank space, add the move
                    moves.append(((row, col), (r, c)))
                elif piece.player != ourcolor:
                    # if we see other player's piece, add the move
                    moves.append(((row, col), (r, c)))
        return moves


class Chessboard(Gameboard):

    def __init__(self, rows=8, cols=8, pygamewindow=None, setup='standard', imagepath=''):
        super().__init__(rows, cols, pygamewindow)
        self.imagepath = imagepath
        self._arrow = None
        #
        self._chessboard = np.empty((self.rows, self.cols), dtype=Chesspiece)
        self.config()
        # this will hold all pieces in a nested dict
        # e.g. pieces={'white':{Piece:(row,col),Piece:(row,col),...}}
        self.pieces = {'white': {}, 'black': {}}
        if setup == 'standard':
            # setup the chessboard with pieces, white on bottom
            self.addpiece(0, 0, Rook(player='black',
                                     pieceid='rook1', image=self.imagepath+'Chess_rdt60.png'))
            self.addpiece(0, 1, Knight(player='black',
                                       pieceid='knight1', image=self.imagepath+'Chess_ndt60.png'))
            self.addpiece(0, 2, Bishop(player='black',
                                       pieceid='bishop1', image=self.imagepath+'Chess_bdt60.png'))
            self.addpiece(0, 3, Queen(player='black',
                                      pieceid='queen1', image=self.imagepath+'Chess_qdt60.png'))
            self.addpiece(0, 4, King(player='black',
                                     pieceid='king', image=self.imagepath+'Chess_kdt60.png'))
            self.addpiece(0, 5, Bishop(player='black',
                                       pieceid='bishop2', image=self.imagepath+'Chess_bdt60.png'))
            self.addpiece(0, 6, Knight(player='black',
                                       pieceid='knight2', image=self.imagepath+'Chess_ndt60.png'))
            self.addpiece(0, 7, Rook(player='black',
                                     pieceid='rook2', image=self.imagepath+'Chess_rdt60.png'))
            #
            for i in range(8):
                self.addpiece(1, i, Pawn(
                    player='black', pieceid='pawn'+str(i+1), image=self.imagepath+'Chess_pdt60.png', direction=1))
            #            #
            for i in range(8):
                self.addpiece(6, i, Pawn(
                    player='white', pieceid='pawn'+str(i+1), image=self.imagepath+'Chess_plt60.png', direction=-1))
            #
            self.addpiece(7, 0, Rook(player='white',
                                     pieceid='rook1', image=self.imagepath+'Chess_rlt60.png'))
            self.addpiece(7, 1, Knight(player='white',
                                       pieceid='knight1', image=self.imagepath+'Chess_nlt60.png'))
            self.addpiece(7, 2, Bishop(player='white',
                                       pieceid='bishop1', image=self.imagepath+'Chess_blt60.png'))
            self.addpiece(7, 3, Queen(player='white',
                                      pieceid='queen1', image=self.imagepath+'Chess_qlt60.png'))
            self.addpiece(7, 4, King(player='white',
                                     pieceid='king', image=self.imagepath+'Chess_klt60.png'))
            self.addpiece(7, 5, Bishop(player='white',
                                       pieceid='bishop2', image=self.imagepath+'Chess_blt60.png'))
            self.addpiece(7, 6, Knight(player='white',
                                       pieceid='knight2', image=self.imagepath+'Chess_nlt60.png'))
            self.addpiece(7, 7, Rook(player='white',
                                     pieceid='rook2', image=self.imagepath+'Chess_rlt60.png'))
        elif setup == 'flipped':
            # setup the chessboard with pieces, black on bottom
            pass
        elif setup == 'puzzle1':
            self.addpiece(4, 4, King(player='black',
                                     pieceid='king', image=self.imagepath+'Chess_kdt60.png'))
            self.addpiece(7, 2, Bishop(player='white',
                                       pieceid='bishop1', image=self.imagepath+'Chess_blt60.png'))
            self.addpiece(7, 3, Queen(player='white',
                                      pieceid='queen1', image=self.imagepath+'Chess_qlt60.png'))
            self.addpiece(7, 4, King(player='white',
                                     pieceid='king', image=self.imagepath+'Chess_klt60.png'))
            self.addpiece(7, 5, Bishop(player='white',
                                       pieceid='bishop2', image=self.imagepath+'Chess_blt60.png'))

    def __getitem__(self, key):
        return self._chessboard[key]

    def config(self, bgcolors=['gray', 'red'],
               grid=3,
               gridcolor='black',
               border=60,
               bordercolor='white',
               highlightcolor='green'):
        super().config(bgcolors=bgcolors,
                       playercolors=[],
                       markstyles=[],
                       grid=grid,
                       gridcolor=gridcolor,
                       border=border,
                       bordercolor=bordercolor,
                       highlightcolor=highlightcolor)
        if self._screen:
            # update our BG image
            # put this in init, change to self._font
            self._bgimage = pygame.Surface((self._pgwidth, self._pgheight))
            self._bgimage.fill(self._bordercolor)
            pygame.draw.rect(self._bgimage, self._gridcolor, (self._cellorigin[0]-self._grid, self._cellorigin[1]-self._grid,
                                                              self._boardsize[0],
                                                              self._boardsize[1]), width=0)
            # draw the cell backgrounds
            for r in range(self.rows):
                for c in range(self.cols):
                    x, y = self._coordsfromcell(r, c)
                    pygame.draw.rect(self._bgimage, self._bgcolors[(r+c) % len(self._bgcolors)], (x, y,
                                                                                                  self._cellsize,
                                                                                                  self._cellsize), width=0)

    def drawmark(self, row, col):
        piece = self._chessboard[row, col]
        if piece:
            newimgsize = int(self._cellsize * 0.91)
            img = pygame.transform.scale(
                self._images[piece.image], (newimgsize, newimgsize))
            x, y = self._coordsfromcell(row, col)
            # scale the surface if necessary:
            # print(self._cellsize, img.get_width(), int(self._cellsize*0.91))
            x += ((self._cellsize-img.get_width())/2)-1
            y += ((self._cellsize-img.get_height())/2)-1
            self._screen.blit(img, (x, y))

    def addpiece(self, row, col, piece):
        # put on board:
        self._chessboard[row, col] = piece
        # add to player's dict of pieces:
        self.pieces[piece.player][piece] = (row, col)
        # add sprite to board's sprite dict if necessary:
        if piece.image not in self._images.keys():
            self._images[piece.image] = pygame.image.load(
                piece.image).convert_alpha()

    def getpiecevalues(self):
        vals = {}
        for player in self.pieces.keys():
            vals[player] = 0
            for piece in self.pieces[player]:
                vals[player] += piece.piecevalue
        return vals

    def copy(self):
        boardcopy = Chessboard(self.rows, self.cols, setup='blank')
        boardcopy._chessboard = np.copy(self._chessboard)
        boardcopy.pieces = copy.deepcopy(self.pieces)
        return boardcopy

    def validmoves(self, row, col):
        # get moves for piece at row,col
        checkvalid = []
        piece = self._chessboard[row, col]
        if piece is not None:
            ourcolor = piece.player
            checkvalid = piece.getmoves(self._chessboard, row, col)
            for i in range(len(checkvalid)-1, -1, -1):
                tempboard = self.copy()
                tempboard.move(
                    row, col, checkvalid[i][1][0], checkvalid[i][1][1])
                # remove the move from list of options
                # if it would leave us in check (illegal):
                if tempboard.checkstatus(ourcolor):
                    checkvalid.pop(i)
        # print(checkvalid)
        return checkvalid

    def highlight(self, row, col):
        # TODO: put this in parent class
        x, y = self._coordsfromcell(row, col)
        pygame.draw.rect(self._bgimage, self._highlightcolor,
                         (x, y, self._cellsize, self._cellsize), width=0)

    def unhighlight(self, row, col):
        # TODO: put this in parent class
        x, y = self._coordsfromcell(row, col)
        pygame.draw.rect(self._bgimage, self._bgcolors[(
            row+col) % len(self._bgcolors)], (x, y, self._cellsize, self._cellsize), width=0)

    def checkstatus(self, player):
        # 1. find our king
        # 2. get each piece of opposite player
        # 3. see if they can move to our king. if so: check
        players = list(self.pieces.keys())
        otherplayer = players[0 if player == players[1] else 1]
        for piece in self.pieces[player]:
            if piece.pieceid == 'king':
                row, col = self.pieces[player][piece]
        # we have our king at row,col
        for otherpiece in self.pieces[otherplayer]:
            valid = otherpiece.getmoves(self._chessboard,
                                        *self.pieces[otherplayer][otherpiece])
            validdests = [(r, c) for ((a, b), (r, c)) in valid]
            if (row, col) in validdests:
                return True
        return False

    def checkmatestatus(self, player):
        # if we're not in check, we're not checkmated:
        if self.checkstatus(player):
            valid = []
            # if player doesn't have any valid moves, it's checkmate:
            for piece in self.pieces[player]:
                valid = valid+self.validmoves(*self.pieces[player][piece])
                if len(valid) > 0:
                    return False
            return True
        else:
            return False

    def getwinner(self):
        players = list(self.pieces.keys())
        for player in players:
            if self.checkmatestatus(player):
                otherplayer = players[0 if player == players[1] else 1]
                return otherplayer
        return None

    def redraw(self, message1="", message2=""):
        if self._screen:
            font = pygame.font.SysFont(None, 24)
            self._screen.blit(self._bgimage, (0, 0))

            # draw arrows if necessary
            if self._arrow:
                self._screen.blit(self._arrow, (0, 0))

            # draw the pieces
            for r in range(self.rows):
                for c in range(self.cols):
                    self.drawmark(r, c)
            # draw the letters/numbers
            for r in range(self.rows):
                textobj = font.render('87654321'[r], True, 'black')
                x, y = self._coordsfromcell(r, 0)
                x -= 18
                y += self._cellsize*0.4
                self._screen.blit(textobj, (x, y))
            for c in range(self.cols):
                textobj = font.render('abcdefgh'[c], True, 'black')
                x, y = self._coordsfromcell(7, c)
                x += self._cellsize*0.45
                y += self._cellsize+8
                self._screen.blit(textobj, (x, y))
            # draw the message
            textobj = font.render(message1, True, 'black')
            x, y = self._coordsfromcell(0, 4)
            x -= textobj.get_width()//2
            y -= 24
            self._screen.blit(textobj, (x, y))
            textobj = font.render(message2, True, 'black')
            x, y = self._coordsfromcell(0, 4)
            x -= textobj.get_width()//2
            y -= 48
            self._screen.blit(textobj, (x, y))

            pygame.display.flip()

    def move(self, row, col, torow, tocol):
        # move piece from row,col to torow,tocol (overwrites anything there)
        piecedest = self._chessboard[torow, tocol]
        if piecedest is not None:
            if piecedest in self.pieces[piecedest.player]:
                self.pieces[piecedest.player].pop(piecedest)
        self._chessboard[torow, tocol] = self._chessboard[row, col]
        # TODO: if the piece is a king and it moved 2 spaces, also move the rook (castling)
        # get the piece we just moved, register that it has moved
        piece = self._chessboard[torow, tocol]
        piece.hasmoved = True
        # change its location in dict of pieces:
        self.pieces[piece.player][piece] = (torow, tocol)
        self._chessboard[row, col] = None
        # if we have a screen, make our arrow:
        if self._screen is not None:
            arrowsurf = pygame.Surface(
                (self._pgwidth, self._pgheight)).convert_alpha()
            arrowsurf.fill((0, 0, 0, 0))
            arrowstart = self._coordsfromcell(row, col)
            arrowstart = (arrowstart[0]+self._cellsize/2,
                          arrowstart[1]+self._cellsize/2)
            arrowend = self._coordsfromcell(torow, tocol)
            arrowend = (arrowend[0]+self._cellsize/2,
                        arrowend[1]+self._cellsize/2)
            arrowlength = distance(*arrowstart, *arrowend)
            arrowangle = angle(*arrowstart, *arrowend)
            arrow = self._arrowpoly(arrowstart, arrowlength, 12, 36, 36)
            arrow = rotatepoints(arrow, arrowstart, arrowangle)
            pygame.draw.polygon(arrowsurf, (0, 0, 255, 128), arrow, width=0)
            pygame.draw.polygon(arrowsurf, 'black', arrow, width=2)
            self._arrow = arrowsurf

    def _arrowpoly(self, stpt: tuple, length, width, arrowlength, arrowwidth):
        points = [(stpt[0], stpt[1]+(width/2))]
        points.append((stpt[0]+(length-arrowlength), stpt[1]+(width/2)))
        points.append((stpt[0]+(length-arrowlength), stpt[1]+(arrowwidth/2)))
        points.append((stpt[0]+length, stpt[1]))
        points.append((stpt[0]+(length-arrowlength), stpt[1]-(arrowwidth/2)))
        points.append((stpt[0]+(length-arrowlength), stpt[1]-(width/2)))
        points.append((stpt[0], stpt[1]-(width/2)))
        points.append((stpt[0], stpt[1]+(width/2)))
        return points
