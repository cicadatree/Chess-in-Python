## this is v1 of chess in python

from __future__ import annotations
from abc import ABC
from enum import Enum, auto
import re
import typing

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
def askForMove(message) -> typing.Tuple[Position, Position]:
    # ask the user to input the X position for the piece they want to move
    print(message)
    gotValidMove = False
    while not gotValidMove:
        userInput = input("Enter your move in Long Chess Notation (eg., b1-a3): ")
        # re.search() returns re.Match object which evaluates True if userInput matches the regular expression groups in longNotationPattern
        match = re.search(longNotationPattern, userInput)
        if not match:
            print("Incorrect syntax -- try again")
            continue

        # stores the match.group(1) and match.group(2) from the user's input as a Position object instance. These groups represent the rank and file of the source destination in the form of long algebraic notation.
        sourceLocation = Position().convertFromFileRanktoXY(match.group(1), match.group(2))
        # similary to sourceLocation's comment, destLocation stores the matching group(3) and group(4) from the user's input as a Position object instance.
        destLocation = Position().convertFromFileRanktoXY(match.group(3), match.group(4))

        # userSelection stores the return value for the getPieceFromBoard() method from the ChessBoard Class. 
        # The .getPieceFromBoard() method takes a Position as it's only argument, and returns the piece contained by the (x, y) board position: (_x property, _y property) of the Position argument
        userPieceSelection = game.gameBoard.getPieceFromBoard(sourceLocation)
        
        # check if the piece the user wants to move is their colour
        if userPieceSelection.colour == game.whichTurn:
            game.gameBoard
            # return the Positions of the user's sourceLocation and destLocation
            return (sourceLocation, destLocation)

        # check if the user is trying to select an EmptySquare Piece
        if userPieceSelection == EmptySquare:
            print("Source square does not contain a piece - try again")

        # if all conditions are not valid, it means the user is trying to move a Piece which isn't their own. repeat the loop.
        print(f"{str(userPieceSelection)} - Wrong colour - try again ")

# Position is the class which is designated as the coordinate-conversion class
# between the visual representation's coordinate sysetm and the in-memory
# representat's coordinate system. The only exception to this conversion being for Ranks/Y
# when the visual representation loop is reversed.
class Position: 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y 

    def convertFromRankToY(self, rank):
        self.y = 8 - int(rank)

    def convertFromFileToX(self, file):
        self.x = ord(file) - ord("a")

    def convertFromFileRanktoXY(self, file, rank):
        self.convertFromFileToX(file)
        self.convertFromRankToY(rank)
        return self

    def setByXY(self, x, y):
        self.file = x
        self.rank = y
        return self


# a Position represents the (File,Rank) of a particular square on the board, as converted to (Y,X)
class SquareLocation:
    file: int
    rank: int
    file_codes = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self, file="a", rank=0):
        self.file = ord(file) - ord("a") 
        self.rank = 8 - int(rank)

    def __str__(self):
        return f"{str(self.file_codes[self.file])}{str(self.rank + 1)}"

    def setByXY(self, x, y):
        self.file = x
        self.rank = y
        return self

    def get_x(self) -> int:
        return (self.file)
    
    def get_y(self) -> int:
        return (7 - self.rank)

    x = property(get_x)
    y = property(get_y)

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
    def __init__(self, colour : Colour, location : Position):
        self.colour = colour
        self.location = location

    def __str__(self) -> str:  # redefine the __str__ special function to print the
        return str(self.colour) + self.getPieceType()

    def getColour(self):
        return self.colour

    def getPieceType(self):
        if type(self) == PawnPiece:
            return "P"
        elif type(self) == KnightPiece:
            return "N"
        elif type(self) == RookPiece:
            return "R"
        elif type(self) == QueenPiece:
            return "Q"
        elif type(self) == KingPiece:
            return "K"
        elif type(self) == BishopPiece:
            return "B"
        else:
            return "''"

    __repr__ = __str__


class EmptySquare(Piece):
    def __init__(self):
        super().__init__(Colour.UNDEF, Position())


class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    board = [[EmptySquare() for j in range(8)] for i in range(8)]

    def __init__(self):  # initialize the board with Pieces
        # assigns each white piece to it's initial position on the board
        self.board[0][0] = RookPiece        (Colour.WHITE, Position().setByXY(0,0))
        self.board[1][0] = KnightPiece      (Colour.WHITE, Position().setByXY(1,0))
        self.board[2][0] = BishopPiece      (Colour.WHITE, Position().setByXY(2,0))
        self.board[3][0] = QueenPiece       (Colour.WHITE, Position().setByXY(3,0))
        self.board[4][0] = KingPiece        (Colour.WHITE, Position().setByXY(4,0))
        self.board[5][0] = BishopPiece      (Colour.WHITE, Position().setByXY(5,0))
        self.board[6][0] = KnightPiece      (Colour.WHITE, Position().setByXY(6,0))
        self.board[7][0] = RookPiece        (Colour.WHITE, Position().setByXY(7,0))
        # assign each pawn to it's initial position on the board
        for i in range(8):
            self.board[i][1] = PawnPiece    (Colour.WHITE, Position().setByXY(i,1))
            self.board[i][6] = PawnPiece    (Colour.BLACK, Position().setByXY(i,6))

        # assign each black piece to it's initial position on the board
        self.board[0][7] = RookPiece        (Colour.BLACK, Position().setByXY(0,7))
        self.board[1][7] = KnightPiece      (Colour.BLACK, Position().setByXY(1,7))
        self.board[2][7] = BishopPiece      (Colour.BLACK, Position().setByXY(2,7))
        self.board[3][7] = QueenPiece       (Colour.BLACK, Position().setByXY(3,7))
        self.board[4][7] = KingPiece        (Colour.BLACK, Position().setByXY(4,7))
        self.board[5][7] = BishopPiece      (Colour.BLACK, Position().setByXY(5,7))
        self.board[6][7] = KnightPiece      (Colour.BLACK, Position().setByXY(6,7))
        self.board[7][7] = RookPiece        (Colour.BLACK, Position().setByXY(7,7))

    def getPieceFromBoard(self, location : Position) -> Piece: # method to find the piece on a specified position of the board
        return self.board[location.x][location.y]

    def getAllowableMoves(self, location : Position):
        if type(self.getPieceFromBoard(location)) == KnightPiece:
            x = location.x
            y = location.y
            # list of all possible moves
            destinationSquares = [(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2),(x+2,y+1),(x-2,y+1),(x+2,y-1),(x-2,y-1)]
            # list of all moves that are legal inside the board
            inBoundsDestinationSquares = filter(lambda i : (i[0] >= 0 and i[0] <= 7) and (i[1] >= 0 and i[1] <= 7), destinationSquares)
            # list of all in-bounds moves that are moving into an EmptySquare not already occupied by another piece of the same colour
            validInBoundsDestinationSquares = filter(lambda i : (isinstance(self.board[i[0]][i[1]], EmptySquare)) and (self.board[i[0]][i[1]].getColour() != game.whichTurn), inBoundsDestinationSquares)
            return validInBoundsDestinationSquares

    def __str__(self):  # redefine the __str__ special function to print the chess board out with new lines after every outer list element
        ret = ""
 
        for i in reversed(range(8)):
            str_squares = (str(x) for x in self.board[i])
            fixed_str_squares = (y if y != "" else "''" for y in str_squares)
            line = " ".join(fixed_str_squares)
            ret = ret + str(i+1) + " " + line + "\n"

        ret = ret + "  " + \
            "  ".join(["a", "b", "c", "d", "e", "f", "g", "h"]) + "\n"
        return ret


class PawnPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self):
        return True


class RookPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        # Check if the move is on the cardinal
        if dx != 0 and dy != 0:
            return False

        # Check the northeast direction
        if location.x > self.location.x:
            for i in range(1, dx):
                if ((self.location.x + i),(self.location.y)) is not None:
                    return False
        # Check the northwest direction
        elif location.x < self.location.x:
            for i in range(1, dx):
                if (self.location.x - i, self.location.y + i) is not None:
                    return False
        # Check the southeast direction
        elif location.y < self.location.y:
            for i in range(1, dx):
                if (self.location.x, self.location.y - i) is not None:
                    return False
        # Check the southwest direction
        elif location.y < self.location.y:
            for i in range(1, dx):
                if (self.location.x, self.location.y - i) is not None:
                    return False

        return True


class KnightPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, targetLocation):
        x = (7-self.location.x)
        y = self.location.y

        # list of all possible moves
        destinationSquares = [(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2),(x+2,y+1),(x-2,y+1),(x+2,y-1),(x-2,y-1)]

        # check if target valid for the knight
        if (targetLocation.y, targetLocation.x) not in destinationSquares:
            return False

        # check if target location is out of bounds
        if (targetLocation.x < 0 and targetLocation.x > 7) and (targetLocation.y < 0 and targetLocation.y > 7):
            return False

        if game.gameBoard.getPieceFromBoard(targetLocation).getColour() == game.whichTurn:
            return False
       
        return True


class BishopPiece(Piece):
    def __init__(self, colour, location: Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        # Check if the move is on the diagonal
        if (7- dx) != dy:
            return False

        # Check the northeast direction
        if location.x > self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if ((self.location.x + i),(self.location.y + i)) is not None:
                    return False
        # Check the northwest direction
        elif location.x < self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if (self.location.x - i,self.location.y + i) is not None:
                    return False
        # Check the southeast direction
        elif location.x > self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if (self.location.x + i,self.location.y - i) is not None:
                    return False
        # Check the southwest direction
        elif location.x < self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if (self.location.x - i,self.location.y - i) is not None:
                    return False

        return True


class KingPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self):
        return True


class QueenPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self):
        return True


class GameBoardFactory(ABC): # factory for providing new game instances. this is an abstract class. it is not real. there is no self to reference, because it will never be initialized.
    def getEmptyBoard() -> ChessBoard:
        board = ChessBoard()
        return board
    
    def getStandardBoard() -> ChessBoard:
        factoryBoard = ChessBoard()

        factoryBoard.board[0][0] = RookPiece        (Colour.BLACK, Position().setByXY(0,0))
        factoryBoard.board[0][1] = KnightPiece      (Colour.BLACK, Position().setByXY(0,1))
        factoryBoard.board[0][2] = BishopPiece      (Colour.BLACK, Position().setByXY(0,2))
        factoryBoard.board[0][3] = QueenPiece       (Colour.BLACK, Position().setByXY(0,3))
        factoryBoard.board[0][4] = KingPiece        (Colour.BLACK, Position().setByXY(0,4))
        factoryBoard.board[0][5] = BishopPiece      (Colour.BLACK, Position().setByXY(0,5))
        factoryBoard.board[0][6] = KnightPiece      (Colour.BLACK, Position().setByXY(0,6))
        factoryBoard.board[0][7] = RookPiece        (Colour.BLACK, Position().setByXY(0,7))
        # assign each pawn to it's initial position on the board
        for i in range(8):
            factoryBoard.board[1][i] = PawnPiece    (Colour.BLACK, Position().setByXY(1,i))
            factoryBoard.board[6][i] = PawnPiece    (Colour.WHITE, Position().setByXY(6,i))
        # assign each black piece to it's initial position on the board
        factoryBoard.board[7][0] = RookPiece        (Colour.WHITE, Position().setByXY(7,0))
        factoryBoard.board[7][1] = KnightPiece      (Colour.WHITE, Position().setByXY(7,1))
        factoryBoard.board[7][2] = BishopPiece      (Colour.WHITE, Position().setByXY(7,2))
        factoryBoard.board[7][3] = QueenPiece       (Colour.WHITE, Position().setByXY(7,3))
        factoryBoard.board[7][4] = KingPiece        (Colour.WHITE, Position().setByXY(7,4))
        factoryBoard.board[7][5] = BishopPiece      (Colour.WHITE, Position().setByXY(7,5))
        factoryBoard.board[7][6] = KnightPiece      (Colour.WHITE, Position().setByXY(7,6))
        factoryBoard.board[7][7] = RookPiece        (Colour.WHITE, Position().setByXY(7,7))

        return factoryBoard

    def getKnightsOnlyBoard() -> ChessBoard:
        factoryBoard = ChessBoard()

        factoryBoard.board[0][1] = KnightPiece      (Colour.BLACK, Position().setByXY(0,1))
        factoryBoard.board[0][6] = KnightPiece      (Colour.BLACK, Position().setByXY(0,6))
        factoryBoard.board[7][1] = KnightPiece      (Colour.WHITE, Position().setByXY(7,1))
        factoryBoard.board[7][6] = KnightPiece      (Colour.WHITE, Position().setByXY(7,6))

        return factoryBoard

class GameState:
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    turnCounter: int = 0
    # whichColour indicates whose turn it is (starting with White by default)
    whichTurn: Colour = Colour.WHITE

    # just move the piece; valibdation is done elsewhere
    def movePiece(self, sourcePiece : Piece, playerMove : typing.Tuple(Position, Position)):
        if game.gameBoard.getPieceFromBoard(playerMove[0]).isValidMove(playerMove[1]):
            sourcePiece.location = playerMove[1]
            game.gameBoard.board[playerMove[1].x][playerMove[1].y] = sourcePiece
            game.gameBoard.board[playerMove[0].x][playerMove[0].y] = EmptySquare()

    def moveToNextTurn(self):
        self.turnCounter += 1
        if self.turnCounter % 2 == 0:
            self.whichTurn = Colour.WHITE
        else:
            self.whichTurn = Colour.BLACK

game = GameState()

def main():

    while True:
        print("\n")
        print("Here is the game board: \n")
        print(game.gameBoard)
        # move stores the tuple (sourceLocation : Position, DestLocation : Position) representing the user's desired move
        move = askForMove(f"It's {str(game.whichTurn)}'s turn")
        
        
        # movePiece(sourcePiece : Piece, playerMove : typing.Tuple(Position, Position))
        game.movePiece(game.gameBoard.getPieceFromBoard(move[0]), move)
        game.moveToNextTurn()
        continue

if __name__ == "__main__":
    main()