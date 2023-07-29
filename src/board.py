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
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        #creating new move 
                        move = Move(initial, final)
                        
                        #empty then continue
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append a new move
                            piece.add_move(move)
                        
                        # has enemy piece the move plus break
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # append a new move
                            piece.add_move(move)
                            break
                        
                        # has our own piece then break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    # not in range
                    else:
                        break
                    #incrementing incrs    
                    possible_move_row = possible_move_row + row_incr 
                    possible_move_col = possible_move_col + col_incr
                        
        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row+1, col+0), # down
                (row-1, col+1), # digonally right up
                (row-1, col-1), # diagonally left up
                (row+1, col+1), # digonally right down
                (row+1, col-1), # diagonally left down
                (row+0, col+1), # right
                (row+0, col-1)  # left
            ]   
            
            #normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move 
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)
                        
                        #create new move 
                        move = Move(initial, final)
                        
                        #append move
                        piece.add_move(move)
            #castling moves
            
            #queen side castle
            
            # king side castle
        
        
        
        if isinstance(piece, Pawn): 
            pawn_moves()
        
        elif isinstance(piece, Knight):
            knight_moves()
        
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1,1),  # up-right
                (-1,-1),  # up-left
                (1,1),  # down-right
                (1,-1)  # down-left
            ])
        
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1,0), #up
                (0,-1), #left
                (1,0), #down
                (0,1) # right
            ])
        
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1,0), #up
                (0,-1), #left
                (1,0), #down 
                (0,1), # right
                (-1,1),  # up-right
                (-1,-1),  # up-left
                (1,1),  # down-right
                (1,-1)  # down-left
            ])
        
        elif isinstance(piece, King):
            king_moves()
    
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
        self.squares[4][4] = Square(row_other, 4, King(color))