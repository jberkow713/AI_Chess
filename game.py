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
Width, Height = 900,900
Max_FPS = 15
clock = p.time.Clock()
L_BLUE = (0,255,255)

def collision(coords_1,coords_2):
    # collision function
    if coords_1[0]>=coords_2[0] and coords_1[0]<=coords_2[1]:
        if coords_1[1]>=coords_2[2] and coords_1[1]<=coords_2[3]:
            return True 
    return False

def click_check():
    clicked = p.mouse.get_pressed()    
    if clicked[0] == True or clicked[2]==True:
        return True
    return False


class Piece:
    def __init__(self,type, x,y,size):
        self.type = type 
        self.x = x
        self.y = y
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
    def move(self,piece):

        #TODO returns all possible squares for a given piece based on its type
        pass  

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.screen = p.display.set_mode((Width, Height))   
        self.Sq_sz = int(Width/self.size)
        self.highlighted = None 
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
        # Creating coordinate position for each piece on the board
        # Run on every move to update 
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
        if self.highlighted!=None:
            p.draw.rect(self.screen,L_BLUE,self.highlighted)    
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
    def __init__(self, color,game):        
        self.color = color        
        self.game = game
        self.positions = self.game.create_positions()
        self.sq_size = self.game.Sq_sz        
        self.pieces = self.find_usable()
        self.clicked = None
        self.timer_on = False 
        self.highlight_timer = 0               
            
    def find_usable(self):
        usable = {}
        if self.color =='white':
            pieces = ['wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        else:
            pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp']    
        for idx,piece in self.positions.items():
            if piece.type in pieces:
                usable[idx]=piece
        return usable

    def play(self):        
        pos = p.mouse.get_pos()
               
        # player commands to interact with pieces
        # Piece(self.board[i][j],x,y,self.Sq_sz)
        if self.timer_on ==True:
            self.highlight_timer -=1
            if self.highlight_timer <=0:
                self.timer_on = False 
        for piece in self.pieces.values():
            x_1,x_2  = piece.x,piece.x + self.sq_size 
            y_1,y_2 = piece.y, piece.y + self.sq_size
            coords = (x_1,x_2,y_1,y_2)
            
            if self.clicked != None and self.timer_on==False and collision(pos,self.clicked)==True:             
                if click_check()==True:                    
                    self.game.highlighted = None
                    self.clicked = None
                    self.timer_on = True 
                    self.highlight_timer =5
                    return   
            if self.timer_on == False:
                if collision(pos,coords)==True:
                    if click_check() == True:
                        self.game.highlighted = (x_1,y_1,self.sq_size,self.sq_size)
                        self.clicked = coords
                        self.highlight_timer = 5
                        self.timer_on = True
                    


    def click_piece(self):
        # TODO
        # find position mouse clicked on board
        # access self.positions to determine which piece was clicked
        # highlight square
        # on clicking new square, determine if piece can move to that square
        pass 
    def conquered(self,From,To):
        # TODO
        # determine if from piece is conquering the to piece, 
        # has to be piece of opposite color, on square where piece is moving to
        pass   

class Comp:
    def __init__(self,size,color,skill=None):
        self.size = size
        self.color = color  
        self.skill = skill
        self.pieces = Game(size).positions
    def calc_moves_square(self):
        #TODO 
        # calc all moves for given square
        pass   
G = Game(25)
P = Player('white',G)
P2 = Player('black',G)
while True:
    for e in p.event.get():
        if e.type == p.QUIT:
            sys.exit()
    G.map()
    P.play()
    P2.play()
    clock.tick(Max_FPS)
    p.display.flip()