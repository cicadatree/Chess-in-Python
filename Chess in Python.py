# large-scale tasks to be completed (as of Jan 8, 2023):
## 1. Figure out the actual game engine
## 2. Figure out how to draw the game in a window

from dataclasses import dataclass
from enum import Enum, auto

class Colour(Enum):
    # enumerate white and black
    # when inheriting from Enum, the auto() method automatically assigns the appropriate enum to each listed value
    WHITE = auto()
    BLACK = auto()

    # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
    def __str__(self) -> str:
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'

    # you have to explicitly tell python to reassign the new __str__ output as the the __repr__ output for the class
    # if you do not, it will continue to print the memory address of the given instance of the object
    __repr__ = __str__

@dataclass
class Player:
    colour: Colour

class ChessBoard:
    # define the initial board as a 2D array
    # board is a list of lists representing the chessboard
    # '' represents an empty square
    # the outer list represents the rows of the board (8 rows)
    # the inner list represents the columns of the board (8 columns)
    board = [['' for j in range(8)] for i in range(8)]

   # redefine the __str__ special function to print the chess board out with new lines after every outer list element
    def __str__(self) -> str:
        ret = ""
        for i in range(8):
            ret = ret + str(self.board[i]) + "\n"
        return ret

# defines the basic concept of a "piece"
# has a colour (e.g. WHITE), a fullName (e.g. "Rook"), and shortName (e.g. "R")
class Piece:
    colour: Colour
    fullName: str
    shortName: str

    # redefine the __str__ special function to print the 
    def __str__(self):
        return str(self.colour) + self.shortName

    # you have to explicitly tell python to reassign the new __str__ output as the the __repr__ output for the class
    # if you do not, it will continue to print the memory address of the given instance of the object
    __repr__ = __str__

# this set of classes defines all possible pieces (inheriting attributes from the Piece object)
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

# assign game to a new instance of the GameState object, and then assign the ChessBoard() object as it's gameBoard
game = GameState()
game.gameBoard = ChessBoard()

#assigns each piece to a position on the board
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

# main loop
while True:
    print("\n")
    print("This game is called chess. There are two players; White (aka W) and Black (aka B). Each player starts with the same number and type of pieces.\n")
    print("It is " + str(game.whichTurn) + "'s turn" + "\n" + "Here is the game board: \n")
    print(game.gameBoard)
    break