from dataclasses import dataclass
from enum import Enum, auto

class Colour(Enum):
    WHITE = auto()
    BLACK = auto()
    def __str__(self) -> str:
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'
    __repr__ = __str__



@dataclass
class Player:
    colour: Colour

class ChessBoard:
    board = [['' for j in range(8)] for i in range(8)]
    # define the initial board as a 2D array
    # board is a list of lists representing the state of the chessboard
    # None represents an empty square
    # the outer list represents the rows of the board (8 rows)
    # the inner list represents the columns of the board (8 columns)
    def __str__(self) -> str:
        ret = ""
        for i in range(8):
            ret = ret + str(self.board[i]) + "\n"
        return ret

    def getPiece(self,userInput):
        if len(userInput) > 2:
            return "Invalid input - must be exactly 2 characters"

        for i in userInput:
            for 

class Piece:
    colour: Colour
    fullName: str
    shortName: str
    def __str__(self):
        return str(self.colour) + self.shortName
    __repr__ = __str__

class PawnPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "Pawn"
        self.shortName = "P"

class RookPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "Rook"
        self.shortName = "R"

class KnightPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "Knight"
        self.shortName = "N"
    
class BishopPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "Bishop"
        self.shortName = "B"

class KingPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "King"
        self.shortName = "K"

class QueenPiece(Piece):
    def __init__(self,colour):
        self.colour = colour
        self.fullName = "Queen"
        self.shortName = "Q"

# GameState stores all relevant attributes of the given game's state.
# Can even consider adding an attribute that saves the game's current state as an FEN string (https://www.chess.com/terms/fen-chess)

class GameState:
    gameBoard: ChessBoard
    turnCounter: int = 0
    whichTurn: Colour = Colour.WHITE

game = GameState()
game.gameBoard = ChessBoard()

game.gameBoard.board[0][0] = RookPiece(Colour.WHITE)
game.gameBoard.board[0][1] = KnightPiece(Colour.WHITE)
game.gameBoard.board[0][2] = BishopPiece(Colour.WHITE)
game.gameBoard.board[0][3] = QueenPiece(Colour.WHITE)
game.gameBoard.board[0][4] = KingPiece(Colour.WHITE)
game.gameBoard.board[0][5] = BishopPiece(Colour.WHITE)
game.gameBoard.board[0][6] = KnightPiece(Colour.WHITE)
game.gameBoard.board[0][7] = RookPiece(Colour.WHITE)

for i in range(8):
    game.gameBoard.board[1][i] = PawnPiece(Colour.WHITE)
    game.gameBoard.board[6][i] = PawnPiece(Colour.BLACK)

game.gameBoard.board[7][0] = RookPiece(Colour.BLACK)
game.gameBoard.board[7][1] = KnightPiece(Colour.BLACK)
game.gameBoard.board[7][2] = BishopPiece(Colour.BLACK)
game.gameBoard.board[7][3] = QueenPiece(Colour.BLACK)
game.gameBoard.board[7][4] = KingPiece(Colour.BLACK)
game.gameBoard.board[7][5] = BishopPiece(Colour.BLACK)
game.gameBoard.board[7][6] = KnightPiece(Colour.BLACK)
game.gameBoard.board[7][7] = RookPiece(Colour.BLACK)
    
while True:
    print("This game is chess. You are playing this game of chess. It is " + str(game.whichTurn) + "'s turn" + "\n")
    print(game.gameBoard)
    pieceSelect = input("What piece do you want to move? ")
    if pieceSelect == 

    break