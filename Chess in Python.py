# Useful resource: https://www.chessprogramming.org/Main_Page

# large-scale tasks to be completed (as of Jan 8, 2023):
## 1. Figure out the actual game engine
## 2. Figure out how to draw the game in a window (GUI)
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

# global utlity function to check if the user input is 
def validateInput(message) -> int:
    # get input from user with message
    userInput = input(message)
    # check if userInput is a string
    if isinstance(userInput, str):
        try:
            int(userInput)
        except ValueError:
            userInput = -1
            pass
        userInput = int(userInput)
    # validate that the userInput is between 1 and 8
    if userInput < 8 and userInput > 0:
        return(userInput)

    validateInput("TRY AGAIN IDIOT ")

class Colour(Enum):
    # enumerate white and black
    # when inheriting from Enum, the auto() method automatically assigns the appropriate enum to each listed value
    WHITE = auto()
    BLACK = auto()

    # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
    def __str__(self):
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'
    # you have to explicitly tell python to reassign the new __str__ output as the the __repr__ output for the class
    # if you do not, it will continue to print the memory address of the given objecft
    __repr__ = __str__

class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    # the outer list represents the rows of the board (8 rows)
    # the inner list represents the columns of the board (8 columns)
    board = [['' for j in range(8)] for i in range(8)] 

    def __init__(self):
        #assigns each white piece to it's initial position on the board
        self.board[0][0] = RookPiece(Colour.WHITE)
        self.board[0][1] = KnightPiece(Colour.WHITE)
        self.board[0][2] = BishopPiece(Colour.WHITE)
        self.board[0][3] = QueenPiece(Colour.WHITE)
        self.board[0][4] = KingPiece(Colour.WHITE)
        self.board[0][5] = BishopPiece(Colour.WHITE)
        self.board[0][6] = KnightPiece(Colour.WHITE)
        self.board[0][7] = RookPiece(Colour.WHITE)

        # assign each pawn to it's initial position on the board
        for i in range(8):
            self.board[1][i] = PawnPiece(Colour.WHITE)
            self.board[6][i] = PawnPiece(Colour.BLACK)

        # assign each black piece to it's initial position on the board
        self.board[7][0] = RookPiece(Colour.BLACK)
        self.board[7][1] = KnightPiece(Colour.BLACK)
        self.board[7][2] = BishopPiece(Colour.BLACK)
        self.board[7][3] = QueenPiece(Colour.BLACK)
        self.board[7][4] = KingPiece(Colour.BLACK)
        self.board[7][5] = BishopPiece(Colour.BLACK)
        self.board[7][6] = KnightPiece(Colour.BLACK)
        self.board[7][7] = RookPiece(Colour.BLACK)

    def getPiece(self,x,y) -> Piece:
        return print(self.board[x][y])

    # redefine the __str__ special function to print the chess board out with new lines after every outer list element
    def __str__(self):
        ret = ""
        for i in range(8):
            ret = ret + str(self.board[i]) + "\n"
        return ret

# defines the basic concept of a "piece"
# has a colour (e.g. WHITE), a fullName (e.g. "Rook"), and shortName (e.g. "R")
'''general question: can the Piece class be an abstract base class??'''
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

# this set of classes define all piece types in chess (inheriting colour, fullName, and shortName attributes from the Piece object)
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
class GameState:
    gameBoard: ChessBoard = ChessBoard()
    turnCounter: int = 0
    whichTurn: Colour = Colour.WHITE
    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    # whichColour indicates whose turn it is (starting with White by default)

# assign game to a new instance of the GameState object, and then assign the ChessBoard() object as it's gameBoard
game = GameState()

# main loop
while True:
    print("\n")
    print("This game is called chess. There are two players; White (aka W) and Black (aka B). Each player starts with the same number and type of pieces.\n")
    print("It is " + str(game.whichTurn) + "'s turn \n" + "Here is the game board: \n")

    userInputX = validateInput("What is the X value for your piece? ")
    userInputY = validateInput("What is the Y value for your piece? ")

    game.gameBoard.getPiece(userInputX,userInputY)

    break