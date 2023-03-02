from __future__ import annotations
from enum import Enum, auto
import re
import typing

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
def askForMove(message) -> typing.Tuple[SquareLocation, SquareLocation]:
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
        userSelection = game.gameBoard.getPiece(source_location)
        if userSelection.colour == game.whichTurn:
            game.gameBoard
            # if the piece colour is correct, return the move
            return (source_location, dest_location)

        # check if userSelection is a Piece (vs an empty board position):
        if userSelection == emptyCell:
            print("Source square does not contain a piece - try again")

        # if the colour is wrong - let the user know, but do not tell them they are an idiot!
        print(f"{str(userSelection)} - Wrong colour - try again ")


class SquareLocation:
    file: int
    rank: int
    file_codes = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self, file="a", rank=0):
        self.file = ord(file) - ord("a")
        self.rank = int(rank) - 1

    def __str__(self):
        return f"{str(self.file_codes[self.file])}{str(self.rank + 1)}"

    def setByXY(self, x, y):
        self.file = x
        self.rank = y
        return self
 
    def getXY(self) -> typing.Tuple[int, int]:
        return (7 - self.rank, self.file)

    def get_x(self) -> int:
        return (7 - self.rank)
    
    def get_y(self) -> int:
        return (self.file)

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
    def __init__(self, colour : Colour):
        self.colour = colour
        self.location = None

    def __str__(self) -> str:  # redefine the __str__ special function to print the
        return str(self.colour) + self.getPieceType()

    def getColour(self):
        return self.colour

    def set_location(self, location):
        self.location = location

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
        super().__init__(Colour.UNDEF)


class ChessBoard:
    def __init__(self):
        self.board = [[EmptySquare() for j in range(8)] for i in range(8)]

        # initialize the board with Pieces
        # assign each white piece to its initial position on the board
        for i, piece in enumerate([RookPiece(Colour.WHITE), KnightPiece(Colour.WHITE), BishopPiece(Colour.WHITE), 
                                   QueenPiece(Colour.WHITE), KingPiece(Colour.WHITE), BishopPiece(Colour.WHITE), 
                                   KnightPiece(Colour.WHITE), RookPiece(Colour.WHITE)]):
            self.board[7][i] = piece
            piece.set_location(SquareLocation().setByXY(7, i))

        # assign each White pawn pawn to its initial position on the board
        for i, piece in enumerate([PawnPiece(Colour.WHITE), PawnPiece(Colour.WHITE), PawnPiece(Colour.WHITE), 
                                   PawnPiece(Colour.WHITE), PawnPiece(Colour.WHITE), PawnPiece(Colour.WHITE), 
                                   PawnPiece(Colour.WHITE), PawnPiece(Colour.WHITE)]):
            self.board[6][i] = piece
            piece.set_location(SquareLocation().setByXY(6, i))

        # assign each black pawn pawn to its initial position on the board
        for i, piece in enumerate([PawnPiece(Colour.BLACK), PawnPiece(Colour.BLACK), PawnPiece(Colour.BLACK), 
                                   PawnPiece(Colour.BLACK), PawnPiece(Colour.BLACK), PawnPiece(Colour.BLACK), 
                                   PawnPiece(Colour.BLACK), PawnPiece(Colour.BLACK)]):
            self.board[1][i] = piece
            piece.set_location(SquareLocation().setByXY(1, i))

        # assign each black piece to its initial position on the board
        for i, piece in enumerate([RookPiece(Colour.BLACK), KnightPiece(Colour.BLACK), BishopPiece(Colour.BLACK), 
                            QueenPiece(Colour.BLACK), KingPiece(Colour.BLACK), BishopPiece(Colour.BLACK), 
                            KnightPiece(Colour.BLACK), RookPiece(Colour.BLACK)]):
            self.board[0][i] = piece
            piece.location = SquareLocation().setByXY(0, i)

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

    def getPiece(self, location : SquareLocation) -> Piece: # method to find the piece on a specified position of the board
        return self.board[location.x][location.y]

    def getAllowableMoves(self, location : SquareLocation):
        if type(self.getPiece(location)) == KnightPiece:
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

        for i in range(8):
            str_squares = (str(x) for x in self.board[i])
            fixed_str_squares = (y if y != "" else "''" for y in str_squares)
            line = " ".join(fixed_str_squares)
            ret = ret + str(8-i) + " " + line + "\n"

        ret = ret + "  " + \
            "  ".join(["a", "b", "c", "d", "e", "f", "g", "h"]) + "\n"
        return ret



class PawnPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def isValidMove(self):
        return True


class RookPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def isValidMove(self, location : SquareLocation):
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
    def __init__(self, colour):
        super().__init__(colour)

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

        if game.gameBoard.getPiece(targetLocation).getColour() == game.whichTurn:
            return False
       
        return True


class BishopPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def isValidMove(self, location : SquareLocation):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        # Check if the move is on the diagonal
        if dx != dy:
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
    def __init__(self, colour):
        super().__init__(colour)

    def isValidMove(self):
        return True


class QueenPiece(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def isValidMove(self):
        return True


class GameState:
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    turnCounter: int = 0
    # whichColour indicates whose turn it is (starting with White by default)
    whichTurn: Colour = Colour.WHITE

    # just move the piece; validation is done elsewhere
    def movePiece(self, sourcePiece : Piece, playerMove : typing.Tuple(SquareLocation, SquareLocation)):
        if game.gameBoard.getPiece(playerMove[0]).isValidMove(playerMove[1]):
            sourcePiece.location = playerMove[1]
            game.gameBoard.board[playerMove[1].x][playerMove[1].y] = sourcePiece
            game.gameBoard.board[playerMove[0].x][playerMove[0].y] = EmptySquare()

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
        # move stores the (SquareLocation, SquareLocation) representing the user's move
        move = askForMove(f"It's {str(game.whichTurn)}'s turn")
        game.movePiece(game.gameBoard.getPiece(move[0]), move)
        game.moveToNextTurn()
        continue

if __name__ == "__main__":
    main()