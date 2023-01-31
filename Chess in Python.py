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
            game.gameBoard
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
    UNDEF = auto()

    def __str__(self):  # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
        if self.value == Colour.WHITE.value:
            return 'W'
        elif self.value == Colour.BLACK.value:
            return 'B'
        else:
            return ''
        

    __repr__ = __str__


class Piece:
    def __init__(self, colour, pieceType):
        self.colour = colour
        self.pieceType = pieceType

    def getColour(self):
        return self.colour

    def __str__(self) -> str:  # redefine the __str__ special function to print the
        return str(self.colour) + self.pieceType
    __repr__ = __str__

class EmptySquare(Piece):
    def __init__(self):
        super().__init__(Colour.UNDEF,"''")

class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    board = [[EmptySquare() for j in range(8)] for i in range(8)]

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

    def getAllowableMoves(self, x, y):
        if type(self.getPiece(x,y)) == KnightPiece:
            # list of all possible moves
            destinationSquares = [(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2),(x+2,y+1),(x-2,y+1),(x+2,y-1),(x-2,y-1)]
            # list of all moves that are legal inside the board
            inBoundsDestinationSquares = filter(lambda i : (i[0] >= 0 and i[0] <= 7) and (i[1] >= 0 and i[1] <= 7), destinationSquares)
    
            validDestinationSquares = []
            # list of all valid moves for the piece itself
            for i in list(inBoundsDestinationSquares):
                w = self.board[i[0]][i[1]]
                z = w.getColour()
                y = game.whichTurn
                print(str(type(w)))
                if isinstance(w,EmptySquare):
                    validDestinationSquares.append(i)
                elif z != y:
                    validDestinationSquares.append(i)
            return validDestinationSquares

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


class PawnPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "P")


class RookPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "R")


class KnightPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "N")


class BishopPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "B")


class KingPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "K")


class QueenPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour, "Q")


class GameState:
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    turnCounter: int = 0
    # whichColour indicates whose turn it is (starting with White by default)
    whichTurn: Colour = Colour.WHITE

    def moveToNextTurn(self):
        self.turnCounter += 1
        if game.turnCounter % 2 == 0:
            game.whichTurn = Colour.WHITE
        else:
            game.whichTurn = Colour.BLACK


game = GameState()

def main():
    while True:
        print("\n")
        print("Here is the game board: \n")
        print(game.gameBoard)
        # ask the player for the x and y values of the piece which they'd like to move from and to.
        move = askForMove(f"It's {str(game.whichTurn)}'s turn")
        # userSelection gives you the piece at the user's selected source square
        userSelection = game.gameBoard.getPiece(*(move[0].getXY()))
        print(f"you selected this move: {str(userSelection)} {str(move[0])}-{str(move[1])}")
        validSquares = game.gameBoard.getAllowableMoves(*(move[0].getXY()))
        print(str(validSquares))


        game.moveToNextTurn()
        continue

if __name__ == "__main__":
    main()
