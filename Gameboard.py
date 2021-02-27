import numpy as np
# from tkinter import *
from PIL import ImageTk, Image
import pygame


class Gameboard:
    SQRT2 = 1.414

    class Piece:
        def __init__(self, playernum=1):
            self.playernum = playernum

    def __init__(self, rows=8, cols=8, pygamescreen=None):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((2, self.rows, self.cols), dtype=np.int8)
        # self.highlighted = np.full((self.rows, self.cols), False, dtype=bool)
        # print(self.highlighted)
        self._images = {}
        if pygamescreen:
            self._screen = pygamescreen
            self._pgwidth = pygame.display.Info().current_w
            self._pgheight = pygame.display.Info().current_h
            self.config()  # load default layout (colors/grid/etc)
            # set cell size to integer:
            if (self._pgwidth/self._pgheight) > (self.cols/self.rows):
                # canvas is wider than it has to be: extra space on sides
                self._cellsize = (self._pgheight-(self._border*2) -
                                  (self._grid*(self.rows+1))) // self.rows
            else:
                # canvas is taller than it has to be (or equal): any extra space on top/bottom
                self._cellsize = (self._pgwidth-(self._border*2) -
                                  (self._grid*(self.cols+1))) // self.cols
            # print(f"self._cellsize = {self._cellsize}")
            # board size in pixels (x,y):
            self._boardsize = ((self._grid*(self.cols+1))+(self._cellsize*self.cols),
                               (self._grid*(self.rows+1))+(self._cellsize*self.rows))
            self._cellorigin = (
                (self._pgwidth-self._boardsize[0])//2, (self._pgheight-self._boardsize[1])//2)
            self._spacing = self._cellsize+self._grid
        else:
            self._screen = None

    def config(self, bgcolors=['gray', 'red'],
               playercolors=['', 'yellow', 'blue'],
               markstyles=[[''], ['x'], ['o']],
               grid=3,
               gridcolor='black',
               border=20,
               bordercolor='white',
               highlightcolor='green'):
        # list of bgcolors: e.g. ['red','black'] or just ['red']
        # first color is top-left (and bottom-right for square boards):
        self._bgcolors = bgcolors
        self._gridcolor = gridcolor
        # set cellstyless per number of players
        # usually, nothing (no mark/fill) for index 0:
        self._playercolors = playercolors
        self._markstyles = markstyles
        self._grid = grid
        self._border = border  # minimum border
        self._bordercolor = bordercolor
        self._highlightcolor = highlightcolor
        #
        # EXAMPLE of setting up mark styles from images:
        #
        #     # playerwin, aiwin, draw = 0, 0, 0
        #     # gameover = False
        #     gameboard = Gameboard(rows=8, cols=8, canvas=cv)
        #     # piecestyles = list of marks for each player (blank for player 0).
        #     # marks can be 'x', 'o', 'dot', or image filename
        #     piecestyles = [[''], [''], ['']]
        #     for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
        #         piecestyles[1].append(PATH + 'Chess_' + piece + 'lt60.png')
        #         piecestyles[2].append(PATH + 'Chess_' + piece + 'dt60.png')

        if self._screen:
            # TODO: redo the board sizing/etc. for new grid/border/etc.
            if (self._pgwidth/self._pgheight) > (self.cols/self.rows):
                # canvas is wider than it has to be: extra space on sides
                self._cellsize = (self._pgheight-(self._border*2) -
                                  (self._grid*(self.rows+1))) // self.rows
            else:
                # canvas is taller than it has to be (or equal): any extra space on top/bottom
                self._cellsize = (self._pgwidth-(self._border*2) -
                                  (self._grid*(self.cols+1))) // self.cols
            # board size in pixels (x,y):
            self._boardsize = ((self._grid*(self.cols+1))+(self._cellsize*self.cols),
                               (self._grid*(self.rows+1))+(self._cellsize*self.rows))
            self._cellorigin = (
                (self._pgwidth-self._boardsize[0])//2, (self._pgheight-self._boardsize[1])//2)
            self._spacing = self._cellsize+self._grid

        # load the images if there are any images in our marker styles:
        #
        # TODO: change this to pygame
        #
        # for p in self._markstyles:  # player
        #     for s in p:
        #         if '.' in s:        # assume it's a filename if there's a period
        #             self._images[s] = ImageTk.PhotoImage(Image.open(s))

    def copy(self):
        boardcopy = Gameboard(self.rows, self.cols)
        boardcopy.board[0] = np.copy(self.board[0])
        boardcopy.board[1] = np.copy(self.board[1])
        return boardcopy

    def _coordsfromcell(self, row, col):
        if self._screen:
            return (self._cellorigin[0]+(self._spacing*col), self._cellorigin[1]+(self._spacing*row))

    def cellfromcoords(self, x, y):
        if self._screen:
            col = int((x-self._cellorigin[0])/self._boardsize[0]*self.cols)
            row = int((y-self._cellorigin[1])/self._boardsize[1]*self.rows)
            if row not in range(self.rows):
                row = None
            if col not in range(self.cols):
                col = None
            return (row, col)
        return (None, None)

    def redraw(self):
        if self._screen:
            self._screen.create_rectangle(0, 0, self._pgwidth, self._pgheight,
                                          fill=self._bordercolor, outline=self._bordercolor)
            # first draw the grid (as filled rectangle to be 'cleared out' with cells):
            self._screen.create_rectangle(self._cellorigin[0]-self._grid, self._cellorigin[1]-self._grid,
                                          (self._cellorigin[0]-self._grid) +
                                          self._boardsize[0]-1,
                                          (self._cellorigin[1]-self._grid) +
                                          self._boardsize[1]-1,
                                          fill=self._gridcolor, outline=self._gridcolor, width=0)
            # now draw the cells
            for r in range(self.rows):
                for c in range(self.cols):
                    self.drawbackground(r, c)
                    self.drawmark(r, c)

    def highlight(self, row, col):
        x, y = self._coordsfromcell(row, col)
        # clear the cell with highlight color, then redraw mark (if any)
        self._screen.create_rectangle(x, y,
                                      x+self._cellsize-1,
                                      y+self._cellsize-1,
                                      fill=self._highlightcolor,
                                      outline=self._highlightcolor,
                                      width=0)
        self.drawmark(row, col)

    def unhighlight(self, row, col):
        # just redraw the cell
        self.drawbackground(row, col)
        self.drawmark(row, col)

    def drawbackground(self, row, col):
        x, y = self._coordsfromcell(row, col)
        # clear the cell with its bgcolor
        self._screen.create_rectangle(x, y,
                                      x+self._cellsize-1,
                                      y+self._cellsize-1,
                                      fill=self._bgcolors[(
                                          row+col) % len(self._bgcolors)],
                                      outline=self._bgcolors[(
                                          row+col) % len(self._bgcolors)],
                                      width=0)

    def drawmark(self, row, col):
        x, y = self._coordsfromcell(row, col)
        player = self.board[0][row, col]
        # draw colored mark (e.g. 'X') if cell is occupied
        if player > 0:
            clr = self._playercolors[player]
            cellstyle = self._markstyles[player][self.board[1][row, col]]
            if '.' in cellstyle:
                self._screen.create_image(
                    x+(self._cellsize/2)-2, y+(self._cellsize/2)-2, image=self._images[cellstyle])
            elif cellstyle == 'fill':
                self._screen.create_rectangle(x, y,
                                              x+self._cellsize-1,
                                              y+self._cellsize-1,
                                              fill=clr,
                                              outline=clr,
                                              width=0)
            elif cellstyle == 'x':
                # draw the x
                strokewidth = 10.0
                self._screen.create_line(x+(self._cellsize*.125)+(strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.125) +
                                         (strokewidth/(2*self.SQRT2)),
                                         x+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         width=strokewidth, fill=clr)
                self._screen.create_line(x+(self._cellsize*.125)+(strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         x+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.125) +
                                         (strokewidth/(2*self.SQRT2)),
                                         width=strokewidth, fill=clr)
            elif cellstyle == 'o':
                # draw the o
                strokewidth = 10.0
                self._screen.create_oval(x+(self._cellsize*.125)+(strokewidth/(2*self.SQRT2))-1,
                                         y+(self._cellsize*.125) +
                                         (strokewidth/(2*self.SQRT2))-1,
                                         x+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         width=strokewidth, outline=clr)
            elif cellstyle == 'dot':
                # draw the dot
                strokewidth = 10.0
                self._screen.create_oval(x+(self._cellsize*.125)+(strokewidth/(2*self.SQRT2))-1,
                                         y+(self._cellsize*.125) +
                                         (strokewidth/(2*self.SQRT2))-1,
                                         x+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         y+(self._cellsize*.875) -
                                         (strokewidth/(2*self.SQRT2)),
                                         width=strokewidth, outline=clr, fill=clr)

    def clearall(self):
        # clear the board (all zeros)
        self.board = np.zeros((2, self.rows, self.cols), dtype=np.int8)
        self.redraw()

    def clear(self, row, col):
        # clear a cell (i.e. set=0)
        if row in range(self.rows) and col in range(self.cols):
            self.board[0][row, col] = 0
            self.board[1][row, col] = 0
            self.redraw()

    def move(self, row, col, torow, tocol):
        # move piece from row,col to torow,tocol (overwrites anything there)
        self.board[0][torow, tocol] = self.board[0][row, col]
        self.board[1][torow, tocol] = self.board[1][row, col]
        self.board[0][row, col] = 0
        self.board[1][row, col] = 0
        self.redraw()

    def mark(self, row, col, playernum, piecetype):
        if row in range(self.rows) and col in range(self.cols):
            self.board[0][row, col] = playernum
            self.board[1][row, col] = piecetype
            self.redraw()

    def marklist(self, coordlist, playernum, piecetype):
        # coordlist = list of tuples
        # not sure if this actually works, maybe we should try it
        delta = False
        for c in coordlist:
            if c[0] in range(self.rows) and c[1] in range(self.cols):
                self.board[0][c] = playernum
                self.board[1][c] = piecetype
                delta = True
        if delta:
            self.redraw()

    def fill(self, row, col, torow, tocol, playernum, piecetype):
        for r in range(row, torow+1):
            for c in range(col, tocol+1):
                self.board[0][r, c] = playernum
                self.board[1][r, c] = piecetype
        self.redraw()

    def __getitem__(self, key):
        return self.board[key]

    def __str__(self):
        return "[Gameboard object]"
