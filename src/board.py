from const import *
from square import Square
from piece import *
from move import Move

class Board: 
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    # to calculate moves
    
    def calc_move(self, piece, row, col):
        """
        this is going to calculate all the possible valid moves of an specific
        piece on a specific position 
    
        """
        
        def pawn_moves():
            
            #steps
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        
                        #creating initial and final move squares
                        initial = Square(row,col)
                        final = Square(possible_move_row,col)
                        
                        #creating a new move
                        move = Move(initial, final)
                        
                        #append new move
                        piece.add_move(move)
                        
                    # if not then we are blocked so we broke the loop as no moves ahead
                    else: 
                        break
                #not in range
                else: 
                    break        
            
            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col -1, col+1]
            
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # creating initial and final squares
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)
                        
                        # creating new move
                        move = Move(initial, final)
                        
                        #append new move
                        piece.add_move(move)
                        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col-1),
                (row+1, col-2),
                (row+2, col+1),
                (row-1, col-2),
                (row-2, col-1)                
            ]
            
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create a square of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  #piece = piece
                        
                        # creating new move 
                        move = Move(initial, final)
                        
                        piece.add_move(move)
        
        
        
        def bishop_moves(): 
            pass
        
        
        
        def rook_moves():
            pass
        
        
        
        def queen_moves():
            pass
        
        
        
        def king_moves(): 
            pass
        
        
        
        
        if isinstance(piece, Pawn): pawn_moves()
        
        if isinstance(piece, Knight):knight_moves()
        
        if isinstance(piece, Bishop): pass
        
        if isinstance(piece, Rook): pass
        
        if isinstance(piece, Queen): pass
        
        if isinstance(piece, King): pass
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        
    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)
        
        
        for col in range(COLS):
            #pawns
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color) )
            
        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
            
        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
            
        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
            
        #Queen
        self.squares[row_other][3] = Square(row_other, 0, Queen(color))
            
        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))