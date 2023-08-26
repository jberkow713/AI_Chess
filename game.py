import pygame as p
import random
import sys
from pygame.constants import MOUSEBUTTONDOWN
import copy
'''
This is a customizable chess game. You can play against a computer on whatever size board you want,
and the pieces are randomized. The AI for computer logic is still being created, but the functionality
allows for human-comp gaming.
'''

p.init()
Width, Height = 1024, 1024
Max_FPS = 15
clock = p.time.Clock()

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.screen = p.display.set_mode((Width, Height))   
        self.board = self.create_board()
        self.Sq_sz = int(Width/self.size)
        self.IMAGES = {}
        self.load_images()
       
    def create_board(self):        
        Board = []
        top_row = []
        bottom_row = []        
        for _ in range(self.size):
            piece = self.pieces[random.randint(0,3)]
            top_row.append('w' + piece)
            bottom_row.append('b' + piece)
        top_row[int(self.size/2)] = 'wk'
        bottom_row[int(self.size/2)]='bk'
        
        white_pawns = ['wp' for _ in range(self.size)]
        black_pawns = ['bp' for _ in range(self.size)]
        
        Board.append(bottom_row)
        Board.append(black_pawns)
        for _ in range(self.size-4):
            Board.append(['-' for _ in range(self.size)])
        Board.append(white_pawns)
        Board.append(top_row)
        return Board
        
    def load_images(self):
        pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        for piece in pieces:
            self.IMAGES[piece]= p.transform.scale(p.image.load(piece+'.png'), (self.Sq_sz, self.Sq_sz))
    
    def drawBoard(self):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(self.size):
            for c in range(self.size):
                color = colors[((r+c)%2)]
                p.draw.rect(self.screen, color, p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))
        return self.screen

    def draw_pieces(self):    
        for r in range(self.size):
            for c in range(self.size):
                piece = self.board[r][c]
                if piece != '-':
                    self.screen.blit(self.IMAGES[piece], p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))

G = Game(16)
while True:        

    for e in p.event.get():
        if e.type == p.QUIT:
            sys.exit()

    G.screen.fill(p.Color('white'))
    G.drawBoard()
    G.draw_pieces()

    clock.tick(Max_FPS)
    p.display.flip()