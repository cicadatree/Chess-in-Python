class ChessBoard:
    def __init__(self):
        # define the initial board as a 2D array
        self.board = [[None for j in range(8)] for i in range(8)]
        # board is a list of lists representing the state of the chessboard
        # None represents an empty square
        # the outer list represents the rows of the board (8 rows)
        # the inner list represents the columns of the board (8 columns)

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

gameBoard = ChessBoard()

gameBoard.board[0][0] = RookPiece("WHITE")  # place a rook at the top-left corner
gameBoard.board[0][1] = KnightPiece("WHITE")  # place a knight next to the rook
gameBoard.board[0][2] = BishopPiece("WHITE")  # place a bishop next to the knight
gameBoard.board[0][3] = QueenPiece("WHITE")  # place the queen on the d-tile
gameBoard.board[0][4] = KingPiece("WHITE")  # place the king on the e-tile
gameBoard.board[0][5] = BishopPiece("WHITE")  # place a bishop next to the king
gameBoard.board[0][6] = KnightPiece("WHITE")  # place a knight next to the bishop
gameBoard.board[0][7] = RookPiece("WHITE")  # place a rook at the top-right corner
        
for i in range(8):
    gameBoard.board[1][i] = PawnPiece("WHITE")  # place pawns on the second row
    gameBoard.board[6][i] = PawnPiece("BLACK")  # place pawns on the seventh row

gameBoard.board[7][0] = RookPiece("BLACK")  # place a rook at the bottom-left corner
gameBoard.board[7][1] = KnightPiece("BLACK")  # place a knight next to the rook
gameBoard.board[7][2] = BishopPiece("BLACK")  # place a bishop next to the knight
gameBoard.board[7][3] = QueenPiece("BLACK")  # place the queen on the d-tile
gameBoard.board[7][4] = KingPiece("BLACK")  # place the king on the e-tile
gameBoard.board[7][5] = BishopPiece("BLACK")  # place a bishop next to the king
gameBoard.board[7][6] = KnightPiece("BLACK")  # place a knight next to the bishop
gameBoard.board[7][7] = RookPiece("BLACK")  # place a rook at the bottom-right corner

print(gameBoard.board)