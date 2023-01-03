class ChessBoard:
    def __init__(self):
        # define the initial board as a 2D array
        self.board = [[None for j in range(8)] for i in range(8)]
        # board is a list of lists representing the state of the chessboard
        # None represents an empty square
        # the outer list represents the rows of the board (8 rows)
        # the inner list represents the columns of the board (8 columns)

        # next we initialize the position of the pieces on the board
        self.board[0][0] = 'R'  # place a rook at the top-left corner
        self.board[0][1] = 'N'  # place a knight next to the rook
        self.board[0][2] = 'B'  # place a bishop next to the knight
        self.board[0][3] = 'Q'  # place the queen on the d-file
        self.board[0][4] = 'K'  # place the king on the e-file
        self.board[0][5] = 'B'  # place a bishop next to the king
        self.board[0][6] = 'N'  # place a knight next to the bishop
        self.board[0][7] = 'R'  # place a rook at the top-right corner
        
        for i in range(8):
            self.board[1][i] = 'P'  # place pawns on the second row
            self.board[6][i] = 'p'  # place pawns on the seventh row
        
        self.board[7][0] = 'r'  # place a rook at the bottom-left corner
        self.board[7][1] = 'n'  # place a knight next to the rook
        self.board[7][2] = 'b'  # place a bishop next to the knight
        self.board[7][3] = 'q'  # place the queen on the d-file
        self.board[7][4] = 'k'  # place the king on the e-file
        self.board[7][5] = 'b'  # place a bishop next to the king
        self.board[7][6] = 'n'  # place a knight next to the bishop
        self.board[7][7] = 'r'  # place a rook at the bottom-right corner

    # define the method to add a piece
    def addPiece(self,piece,row,column):
        self.board[row][column] = piece
    
    # define the method to remove a piece
    def removePiece(self,row,column):
        self.board[row][column] = None

class PawnPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'p'
        self.blackSymbol = 'P'

class RookPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'r'
        self.blackSymbol = 'R'

class KnightPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'n'
        self.blackSymbol = 'N'

class BishopPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'b'
        self.blackSymbol = 'B'

class KingPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'k'
        self.blackSymbol = 'K'

class QueenPiece: 
    def __init__(self,colour):
        self.colour = colour
        self.whiteSymbol = 'q'
        self.blackSymbol = 'Q'

# initialize and print the chessboard
print(ChessBoard.board)