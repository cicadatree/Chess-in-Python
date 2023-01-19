from __future__ import annotations
from enum import Enum, auto
import re

emptyCell = ''  # represents an empty board position
# Regular Expression for valid moves:
#   (letter-from-a-to-h) (number-from-1-to-8) hyphen (letter-from-a-to-h) (number-from-1-to-8)
# (the parentheses around each letter and number capture it in a capture group)
# So, if there's a match, the capture groups will be:
#   source_file = match.group(1)
#   source_rank = match.group(2)
#   dest_file = match.group(3)
#   dest_rank = match.group(4)
longNotationPattern = "^([a-h])([1-8])-([a-h])([1-8])$"

# global utility function for checking if a piece move is valid
def askForMove(message) -> (SquareLocation, SquareLocation):
    # ask the user to input the X position for the piece they want to move
    print(message)
    gotValidMove = False
    while not gotValidMove:
        userInput = input("Enter desired move in Long Chess Notation (eg., b4-c5): ")
        # Validate and parse the user input
        match = re.search(longNotationPattern, userInput)
        if not match:
            print("Incorrect syntax -- try again")
            continue

        # Get the X/Y of the source and destination
        source_location = SquareLocation(match.group(1), match.group(2))
        dest_location = SquareLocation(match.group(3), match.group(4))

        # Check if the userSelection piece is the same colour as the player making the selection
        userSelection = game.gameBoard.getPiece(*(source_location.getXY()))
        if userSelection.colour == game.whichTurn:
            # if the piece colour is correct, return the move
            return (source_location, dest_location)

        # check if userSelection is a Piece (vs an empty board position):
        if userSelection == emptyCell:
            print("Source square does not contain a piece - try again")

        # if the colour is wrong - let the user know, but do not tell them they are an idiot!
        print(f"{str(userSelection)} - Wrong colour - try again ")


class Colour(Enum):  # enumerate white and black
    WHITE = auto()
    BLACK = auto()

    def __str__(self):  # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'

    __repr__ = __str__


class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    board = [[emptyCell for j in range(8)] for i in range(8)]

    def __init__(self):  # initialize the board with Pieces
        # assigns each white piece to it's initial position on the board
        self.board[0][0] = RookPiece(Colour.BLACK)
        self.board[0][1] = KnightPiece(Colour.BLACK)
        self.board[0][2] = BishopPiece(Colour.BLACK)
        self.board[0][3] = QueenPiece(Colour.BLACK)
        self.board[0][4] = KingPiece(Colour.BLACK)
        self.board[0][5] = BishopPiece(Colour.BLACK)
        self.board[0][6] = KnightPiece(Colour.BLACK)
        self.board[0][7] = RookPiece(Colour.BLACK)
        # assign each pawn to it's initial position on the board
        for i in range(8):
            self.board[1][i] = PawnPiece(Colour.BLACK)
            self.board[6][i] = PawnPiece(Colour.WHITE)
        # assign each black piece to it's initial position on the board
        self.board[7][0] = RookPiece(Colour.WHITE)
        self.board[7][1] = KnightPiece(Colour.WHITE)
        self.board[7][2] = BishopPiece(Colour.WHITE)
        self.board[7][3] = QueenPiece(Colour.WHITE)
        self.board[7][4] = KingPiece(Colour.WHITE)
        self.board[7][5] = BishopPiece(Colour.WHITE)
        self.board[7][6] = KnightPiece(Colour.WHITE)
        self.board[7][7] = RookPiece(Colour.WHITE)

    # method to find the piece on a specified position of the board
    def getPiece(self, x, y) -> Piece:
        return self.board[x][y]

    def __str__(self):  # redefine the __str__ special function to print the chess board out with new lines after every outer list element
        ret = ""

        for i in range(8):
            str_squares = (str(x) for x in self.board[i])
            fixed_str_squares = (y if y != "" else "''" for y in str_squares)
            line = " ".join(fixed_str_squares)
            ret = ret + str(8-i) + " " + line + "\n"

        ret = ret + "  " + \
            "  ".join(["a", "b", "c", "d", "e", "f", "g", "h"]) + "\n"
        return ret


class SquareLocation:
    file: int
    rank: int
    file_codes = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self, file, rank):
        self.file = ord(file) - ord("a")
        self.rank = int(rank) - 1

    def __str__(self):
        return f"{str(self.file_codes[self.file])}{str(self.rank + 1)}"

    def getXY(self) -> (int,int):
        return (7 - self.rank, self.file)


class Piece:
    colour: Colour
    pieceType: str

    def getAllowableSquares(self) -> bool:
        return True

    def getAllowableDirectionalSquares(self) -> bool:
        return True

    def __str__(self) -> str:  # redefine the __str__ special function to print the
        return str(self.colour) + self.pieceType
    __repr__ = __str__


class PawnPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "P"


class RookPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "R"


class KnightPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "N"


class BishopPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "B"


class KingPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "K"


class QueenPiece(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.pieceType = "Q"


class GameState:
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    turnCounter: int = 0
    # whichColour indicates whose turn it is (starting with White by default)
    whichTurn: Colour = Colour.WHITE


game = GameState()

while True:
    print("\n")
    print("This game is called chess. There are two players; White (aka W) and Black (aka B). Each player starts with the same number and type of pieces.\n")
    print(f"It is {str(game.whichTurn)}'s turn.\n Here is the game board: \n")
    print(game.gameBoard)
    # ask the player for the x and y values of the piece which they'd like to move from and to.
    move = askForMove(f"It's {str(game.whichTurn)}'s turn")
    userSelection = game.gameBoard.getPiece(*(move[0].getXY()))
    print(f"you selected this move: {str(userSelection)} {str(move[0])}-{str(move[1])}")

    break    # exit out of the Driver code
