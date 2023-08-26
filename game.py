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

class Piece:
    def __init__(self,type, x,y,size):
        self.type = type 
        self.x = x
        self.y = y
        self.size = size
    def move(self,piece):
        #TODO returns all possible squares for a given piece based on its type
        pass  

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.screen = p.display.set_mode((Width, Height))   
        self.Sq_sz = int(Width/self.size)
        self.board = self.create_board()        
        self.IMAGES = {}        
        self.load_images()
       
    def create_board(self):        
        #Building the board, building coordinates top left of each square 
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
    
    def create_positions(self):
        positions = {}
        square = 0
        x = 0
        y = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                positions[square] = Piece(self.board[i][j],x,y,self.Sq_sz)
                x += self.Sq_sz
                square +=1
            y +=self.Sq_sz
            x = 0
        return positions    

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
    def map(self):
        self.screen.fill(p.Color('white'))
        self.drawBoard()
        self.draw_pieces()

class Player:
    def __init__(self, color,size,positions):
        self.color = color
        self.size = size
        self.positions = positions
    
class Comp:
    def __init__(self,size,color,skill=None):
        self.size = size
        self.color = color  
        self.skill = skill
        self.pieces = Game(size).positions 

G = Game(16)
positions = G.create_positions()
P = Player('white',16,positions)
print(P.positions)
while True:        

    for e in p.event.get():
        if e.type == p.QUIT:
            sys.exit()
    G.map()    

    clock.tick(Max_FPS)
    p.display.flip()