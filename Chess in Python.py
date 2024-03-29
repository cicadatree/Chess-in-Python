# TODO:
#       * create the ability to save the game (needed to learn how to write the ai according to alex)
#       * develop basic game ai to play against
#       * evaluate for win/loss condition on each turn
#       * evaluate for king-in-check condition during move validation
#       * evaluate for king-in-checkmate condition
#       * implement GUI for the board's visual representation (terminal sucks)

from __future__ import annotations
from abc import ABC
from enum import Enum, auto
import re
import typing
import copy

# Regular Expression for valid moves:
#   (letter-from-a-to-h) (number-from-1-to-8) hyphen (letter-from-a-to-h) (number-from-1-to-8)
# (the parentheses around each letter and number capture it in a capture group)
# So, if there's a match, the capture groups will be:
#   source_file = match.group(1)
#   source_rank = match.group(2)
#   dest_file = match.group(3)
#   dest_rank = match.group(4)
longNotationPattern = "^([a-h])([1-8])-([a-h])([1-8])$"

################################
####    Game AI Thoughts    ####
################################

# 1. AI makes move decisions for the opposite colour of the human player
#
# 2. AI makes move decisions using a for else loop that evaluates like this:
#
##   for (iterate over the current board):
###     i. iterating over the current board state. On each iteration, return False if the square is an EmptySquare or the opposite colour's piece (narrow in on the remaining subset of squares; only the ai colour's pieces)
###     ii. for each of the AI's own pieces in the iteration, evaluate all possible legal moves which the piece could make (run the pieces isValidMove method for the [i][j] board location which that piece is on)
###     iii. create an empty list. for each legal move of the given piece, score the move based on it's outcome (using the evaluateBoard global utility function). Add points to the given move if that move results in a capture; deduct points for moves that expose the AI's own king/queen.
###     iv. sort the list (appended with each legal move for the given piece) in descending order (from highest to lowest score)
##   else (in the final iteration, return the best of all possible moves)
###     i. take the first index from each piece's move score lists (which should be each pieces best move), add them to a new list 
###     ii. sort the new list in descending order and return the higesht-scoring move among all legal moves

# def aiMove() -> bool:
#     #i. iterate over the board
#     for i in range(8):
#         for j in range(8):
#             # if the colour of the piece being iterated is not the ai's (i.e. is the human's colour - opposite of the ai's, or UNDEF - the EmptySquare's colour), then continue
#             if mainGame.state.gameBoard.board[i][j].colour != mainGame.state.whichTurn:
#                 continue
#             # else the piece belongs to the ai
#             else:
#                 # match case is the same as switch case (just in python). Check each piece type on each iteration. W
#                 match mainGame.state.gameBoard.board[i][j]:
#                     case PawnPiece():
#                         print("It is a Pawn")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                         # do the move validation for all legal moves relative to the current board position ([i][j])
#                     case KingPiece():
#                         print("It is a King")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                     case QueenPiece():
#                         print("It is a Queen")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                     case RookPiece():
#                         print("It is a Rook")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                     case KnightPiece():
#                         print("It is a Knight")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                     case BishopPiece():
#                         print("It is a Bishop")
#                         mainGame.state.gameBoard.board[i][j].isValidMove(Position(i,j))
#                     case _:
#                         print("error - this should never happen")
#                         return False
#         else:
#             # TODO: after for loop has completed iterations, build a list of the 0th element from each pieces sorted list of legal move scores
#             return True


class Colour(Enum):  # Enum Class for Colour inheritance
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


class Position: # Position is oriented in the in-memory representation's coordinate system (x,y).
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y 

    # sets the (x,y) based on the (file,rank) passed in
    def setByFileRank(self, file, rank):
        self.x = ord(file) - ord("a")
        self.y = 8 - int(rank)
        return self

    # sets the (x,y) based on the (x,y) passed in
    def setByXY(self, x, y):
        self.x = x
        self.y = y
        return self


class Piece:
    colour: Colour
    location: Position
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

    # location is a placeholder required for the isKingCheck method
    def isValidMove(self, gameBoard : ChessBoard, location : Position):
        return False


class PawnPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, gameBoard : ChessBoard, location : Position):

        dx = abs(location.x - self.location.x)

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == self.colour:
            return False
        
        if self.location.x == location.x: 
            if self.colour == Colour.WHITE:
                if location.y == self.location.y - 1:
                    return True
                elif self.location.y == 6 and location.y == self.location.y - 2:
                    return True
                else:
                    return False
            else:
                if location.y == self.location.y + 1:
                    return True
                elif self.location.y == 1 and location.y == self.location.y + 2:
                    return True
                else:
                    return False
        elif dx == 1:
            if self.colour == Colour.WHITE:
                if location.y == self.location.y - 1 and type(gameBoard.getPieceFromBoard(Position((location.x),(location.y)))) is not EmptySquare:
                    return True
                else:
                    return False
            else:
                if location.y == self.location.y + 1 and type(gameBoard.getPieceFromBoard(Position((location.x),(location.y)))): 
                    return True
                else:
                    return False
        else:
            return False


class RookPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position, gameBoard : ChessBoard):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == self.colour:
            return False

        # Check if the move is on the cardinal
        if dx != 0 and dy != 0:
            return False

        # Check for pieces in the east direction
        if location.x > self.location.x:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y)))) is not EmptySquare:
                    return False
        # Check for pieces in the west direction
        elif location.x < self.location.x:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i), (self.location.y)))) is not EmptySquare:
                    return False
        # Check for pieces in the south direction
        elif location.y > self.location.y:
            for i in range(1, dy):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the north direction
        elif location.y < self.location.y:
            for i in range(1, dy):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y - i)))) is not EmptySquare:
                    return False
        return True


class BishopPiece(Piece):
    def __init__(self, colour, location: Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position, gameBoard : ChessBoard):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == self.colour:
            return False

        # Check if the move is on the diagonal
        if dx != dy:
            return False

        # Check for pieces in the northeast direction
        if location.x > self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the northwest direction
        elif location.x < self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the southeast direction
        elif location.x > self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y - i)))) is not EmptySquare:
                    return False
        # Check for pieces in the southwest direction
        elif location.x < self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y - i)))) is not EmptySquare:
                    return False
        return True


class KnightPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position, gameBoard : ChessBoard):
        x = self.location.x
        y = self.location.y

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == whichTurn:
            return False

        # list of all possible moves
        destinationSquares = [(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2),(x+2,y+1),(x-2,y+1),(x+2,y-1),(x-2,y-1)]

        # check if target valid for the knight
        if (location.x, location.y) not in destinationSquares:
            return False
        # check if target location is out of bounds
        if (location.x < 0 and location.x > 7) and (location.y < 0 and location.y > 7):
            return False
        if gameBoard.getPieceFromBoard(location).getColour() == self.colour:
            return False
        return True


class KingPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position, gameBoard : ChessBoard):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == self.colour:
            return False

        if dx > 1 or dy > 1:
            return False
        # Check for pieces in the southeast direction
        if location.x > self.location.x and location.y > self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the southwest direction
        elif location.x < self.location.x and location.y > self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the northeast direction
        elif location.x > self.location.x and location.y < self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y - i)))) is not EmptySquare:
                    return False
        # Check for pieces in the northwest direction
        elif location.x < self.location.x and location.y < self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y - i)))) is not EmptySquare:
                    return False
        # Check for pieces in the east direction
        elif location.x > self.location.x:
            for i in range(1):
                if (type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y)))) is not EmptySquare):
                    return False
        # Check for pieces in the west direction
        elif location.x < self.location.x:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((location.x - i), (location.y)))) is not EmptySquare:
                    return False
        # Check for pieces in the south direction
        elif location.y > self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the north direction
        elif location.y < self.location.y:
            for i in range(1):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y - i)))) is not EmptySquare:
                    return False
        return True


class QueenPiece(Piece):
    def __init__(self, colour, location : Position):
        super().__init__(colour, location)

    def isValidMove(self, location : Position, gameBoard : ChessBoard):
        dx = abs(location.x - self.location.x)
        dy = abs(location.y - self.location.y)

        #make sure you're not trying to validate a move that would land on one of your own pieces
        if gameBoard.board[location.x][location.y].colour == self.colour:
            return False

        # make sure that the destination location is on a cardinal (diagonal) line of sight
        if dx != dy and (dx != 0 and dy != 0):
            return False

        # Check for pieces in the southeast direction
        if location.x > self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the southwest direction
        elif location.x < self.location.x and location.y > self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the northeast direction
        elif location.x > self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y - i)))) is not EmptySquare:
                    return False
        # Check for pieces in the northwest direction
        elif location.x < self.location.x and location.y < self.location.y:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i),(self.location.y - i)))) is not EmptySquare:
                    return False
        # Check for pieces in the east direction
        elif location.x > self.location.x:
            for i in range(1, dx):
                if (type(gameBoard.getPieceFromBoard(Position((self.location.x + i),(self.location.y)))) is not EmptySquare):
                    return False
        # Check for pieces in the west direction
        elif location.x < self.location.x:
            for i in range(1, dx):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x - i), (self.location.y)))) is not EmptySquare:
                    return False
        # Check for pieces in the south direction
        elif location.y > self.location.y:
            for i in range(1, dy):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y + i)))) is not EmptySquare:
                    return False
        # Check for pieces in the north direction
        elif location.y < self.location.y:
            for i in range(1, dy):
                if type(gameBoard.getPieceFromBoard(Position((self.location.x), (self.location.y - i)))) is not EmptySquare:
                    return False
        return True


class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    board = [[EmptySquare() for j in range(8)] for i in range(8)]

    def getPieceFromBoard(self, location : Position) -> Piece: # method to find the piece on a specified position of the board
        return self.board[location.x][location.y]

    def __str__(self):  # redefine the __str__ special function to print the chess board out with new lines after every outer list element
        ret = ""

        # i is outside list (X)
        for i in range(8):
            ret = ret + str(8-i) + " "
            # j is inside lists (Y)
            for j in range(8):
                ret = ret + str(self.board[j][i]) + " "
                if j == 7:
                    ret = ret + "\n"

        ret = ret + "  " + \
            "  ".join(["a", "b", "c", "d", "e", "f", "g", "h"]) + "\n"
        return ret


class GameBoardFactory(ABC): # factory for providing new game instances. this is an abstract class. it is not real. there is no self to reference, because it will never be initialized.
    def getEmptyBoard() -> ChessBoard:
        board = ChessBoard()
        return board

    def getStandardBoard() -> ChessBoard:
        factoryBoard = ChessBoard()

        factoryBoard.board[0][0] = RookPiece        (Colour.BLACK, Position().setByXY(0,0))
        factoryBoard.board[1][0] = KnightPiece      (Colour.BLACK, Position().setByXY(1,0))
        factoryBoard.board[2][0] = BishopPiece      (Colour.BLACK, Position().setByXY(2,0))
        factoryBoard.board[3][0] = QueenPiece       (Colour.BLACK, Position().setByXY(3,0))
        factoryBoard.board[4][0] = KingPiece        (Colour.BLACK, Position().setByXY(4,0))
        factoryBoard.board[5][0] = BishopPiece      (Colour.BLACK, Position().setByXY(5,0))
        factoryBoard.board[6][0] = KnightPiece      (Colour.BLACK, Position().setByXY(6,0))
        factoryBoard.board[7][0] = RookPiece        (Colour.BLACK, Position().setByXY(7,0))
        
        # assign each pawn to it's initial position on the board
        for i in range(8):
            factoryBoard.board[i][1] = PawnPiece    (Colour.BLACK, Position().setByXY(i,1))
            factoryBoard.board[i][6] = PawnPiece    (Colour.WHITE, Position().setByXY(i,6))

        # assign each black piece to it's initial position on the board
        factoryBoard.board[0][7] = RookPiece        (Colour.WHITE, Position().setByXY(0,7))
        factoryBoard.board[1][7] = KnightPiece      (Colour.WHITE, Position().setByXY(1,7))
        factoryBoard.board[2][7] = BishopPiece      (Colour.WHITE, Position().setByXY(2,7))
        factoryBoard.board[3][7] = QueenPiece       (Colour.WHITE, Position().setByXY(3,7))
        factoryBoard.board[4][7] = KingPiece        (Colour.WHITE, Position().setByXY(4,7))
        factoryBoard.board[5][7] = BishopPiece      (Colour.WHITE, Position().setByXY(5,7))
        factoryBoard.board[6][7] = KnightPiece      (Colour.WHITE, Position().setByXY(6,7))
        factoryBoard.board[7][7] = RookPiece        (Colour.WHITE, Position().setByXY(7,7))

        return factoryBoard


class GameState:
    gameBoard: ChessBoard = GameBoardFactory.getStandardBoard()   # gameBoard is a ChessBoard-like object
    

    # kingDict stores key:value pair of Colour:kingPosition, which is updated each turn. Designed to keep track of each colour's king position for reference in the isKingCheck function
    kingDict = {}
    # these two lists should store the list of pieces (for each respective colour) which are still on the board. By default, all pieces are on the board. When a piece captures another piece, new behaviour has to be written to remove them from this list.
    whitePiecesOnBoard = []
    blackPiecesOnBoard = []

    # just move the piece; valibdation is done elsewhere
    def movePiece(self, sourcePiece : Piece, destinationPosition : Position):
        if sourcePiece.isValidMove(self.gameBoard, destinationPosition):
            # first, take the sourcePiece off the board (by replacing it with an EmptySquare)
            self.gameBoard.board[sourcePiece.location.x][sourcePiece.location.y] = EmptySquare()
            # next, assign the location of the source piece to the destination position (this is in the in-memory representation of the source piece)
            sourcePiece.location = destinationPosition
            # finally, update the in-memory representation of the board by putting the source piece on the destination position.
            # note that this will also destroy any underlying piece on the destination square. 
            self.gameBoard.board[destinationPosition.x][destinationPosition.y] = sourcePiece
            # TODO: based on the note above, I will need to update the gamestate with the lost pieces which are captured (when they are on the destination square). 
            # I'll need to do a test on whether the destination square is occupied during this method.
            return True
        else:
            # TODO: handle cases when the move is not valid (i.e)
            print("this is not a valid move, try again. \n")
            return False



class NewGame:

    def __init__(self):
        self.state = GameState()
        self.whichTurn = Colour.WHITE
        self.turnCounter = 0 

    def moveToNextTurn(self):
        self.turnCounter += 1
        if self.turnCounter % 2 == 0:
            self.whichTurn = Colour.WHITE
        else:
            self.whichTurn = Colour.BLACK

    def askForMove(self, message : str) -> typing.Tuple[Position, Position]: # global utility function for checking if a piece move is valid
        # ask the user to input the X position for the piece they want to move
        print(message)
        print(f"{str(self.whichTurn)}'s score is: {self.evaluateBoard()}\n")
        gotValidMove = False
        while not gotValidMove:
            userInput = input("Enter your move in Long Chess Notation (eg., b1-a3): ")
            # re.search() returns re.Match object which evaluates True if userInput matches the regular expression groups in longNotationPattern
            match = re.search(longNotationPattern, userInput)
            if not match:
                print("Incorrect syntax -- try again")
                continue

            # stores the match.group(1) and match.group(2) from the user's input as a Position object instance. These groups represent the rank and file of the source destination in the form of long algebraic notation.
            sourceLocation = Position().setByFileRank(match.group(1), match.group(2))
            # similary to sourceLocation's comment, destLocation stores the matching group(3) and group(4) from the user's input as a Position object instance.
            destLocation = Position().setByFileRank(match.group(3), match.group(4))

            # userSelection stores the return value for the getPieceFromBoard() method from the ChessBoard Class. 
            # The .getPieceFromBoard() method takes a Position as it's only argument, and returns the piece contained by the (x, y) board position: (_x property, _y property) of the Position argument
            userPieceSelection = self.state.gameBoard.getPieceFromBoard(sourceLocation)
            
            # check if the piece the user wants to move is their colour
            if userPieceSelection.colour == self.whichTurn:
                self.state.gameBoard
                # return the Positions of the user's sourceLocation and destLocation
                return (sourceLocation, destLocation)

            # check if the user is trying to select an EmptySquare Piece
            if userPieceSelection == EmptySquare:
                print("Source square does not contain a piece - try again")

            # if all conditions are not valid, it means the user is trying to move a Piece which isn't their own. repeat the loop.
            print(f"{str(userPieceSelection)} - Wrong colour - try again ")

    def doTurn(self):
        # move stores the tuple (sourceLocation : Position, DestLocation : Position) representing the user's desired move
        move = self.askForMove(f"It's {str(self.whichTurn)}'s turn")
        # movePiece(sourcePiece : Piece, destinationPosition : typing.Tuple(Position, Position))
        if not self.state.movePiece(self.state.gameBoard.getPieceFromBoard(move[0]), move[1]):
            self.doTurn()

    def evaluateBoard(self): # basic evaluation function which iterates over the board and calculates the given player's score
        whiteScore = 0
        blackScore = 0

        for i in range(8):
            for j in range(8):
                if self.whichTurn == Colour.WHITE:
                    piece = self.state.gameBoard.board[i][j]
                    if str(piece) == 'WP':
                        whiteScore += 1
                    elif str(piece)  == 'WN' or str(piece) == 'WB':
                        whiteScore += 3
                    elif str(piece)  == 'WR':
                        whiteScore += 5
                    elif str(piece)  == 'WQ':
                        whiteScore += 9
                    elif str(piece)  == 'BP':
                        whiteScore -= 1
                    elif str(piece)  == 'BN' or str(piece) == 'BB':
                        whiteScore -= 3
                    elif str(piece)  == 'BR':
                        whiteScore -= 5
                    elif str(piece)  == 'BQ':
                        whiteScore -= 9
                    elif str(piece) == "''":
                        whiteScore += 0
                    else:
                        return whiteScore
                else:
                    piece = self.state.gameBoard.board[i][j]
                    if str(piece) == 'WP':
                        blackScore -= 1
                    elif str(piece) == 'WN' or str(piece) == 'WB':
                        blackScore -= 3
                    elif str(piece) == 'WR':
                        blackScore -= 5
                    elif str(piece) == 'WQ':
                        blackScore -= 9
                    elif str(piece) == 'BP':
                        blackScore += 1
                    elif str(piece) == 'BN' or str(piece) == 'BB':
                        blackScore += 3
                    elif str(piece) == 'BR':
                        blackScore += 5
                    elif str(piece) == 'BQ':
                        blackScore += 9
                    elif str(piece) == "''":
                        blackScore += 0
                    else:
                        return blackScore

    # global utility function that can be called whenever you need to check if a King is in check. 
    def isKingCheck(self, colour : Colour): 
        # Get the colour's king Position
        for i in range(8):
            for j in range(8):
                if type(self.state.gameBoard.board[i][j]) is KingPiece and colour == self.state.gameBoard.board[i][j].colour:
                    correctKingPos = self.state.gameBoard.board[i][j].location

        # Iterate over the current board, and for each Piece use the isValidMove method (passing the King's position in as the destinationLocation for the method). 
        for i in range(8):
            for j in range(8):
                # If the piece being evaluated puts the king in check, then isKingCheck returns True
                if type(self.state.gameBoard.board[i][j]) is not EmptySquare and self.state.gameBoard.board[i][j].isValidMove(self.state.gameBoard, correctKingPos) == True:
                    return True
        return False

    def gameLoop(self):
        print("\n")
        print("-----------")
        print("Here is the game board: \n")
        print(self.state.gameBoard)
        self.doTurn()
        self.moveToNextTurn()
##### NOTE - Apr 8, 2023
## I HAVE A GAMESTATE. APPARENTLY I WILL HAVE A SPECIAL KEYWORD IN MY APPLICATION LOOP.
## APPARENTLY I WILL NOW HOW A LOOP FOR MY GAMESTATE, AND A LOOP FOR MY APPLICATION.
## THE LOOP FOR MY GAMESTATE HOLDS ALL THE LOGIC FOR THE GAME (I.E. main())
## THE APPLICATION LOOP EXISTS AS A HIGHER ORDER LOOP TO THE GAMESTATE LOOP. IT WILL RUN THE GAMESTATE LOOP (WHICH IS ACTUALLY JUST A FUNCTION IN THE APPLICATION LOOP).
## IN THE APPLCIATION LOOP, WHAT IT WILL DO IS CHECK FOR SPECIAL KEYWORDS INPUT BY THE USER TO CONTROL THE APPLICATION (LIKE "QUIT" TO EXIT THE APPLICATION).
## ANOTHER KEYWORD MAY BE "SAVE" (WHICH WILL SAVE THE CURRENT GAMESTATE TO A NEW VARIABLE, AND EXIT TO MENU)
## ANOTHER KEYWORD MAY BE "NEW GAME" (WHICH WILL START A NEW GAME IN A FRESH INSTANCE)

#### NOTE - Apr 10, 2023
# check if game is running (if running, the game can be saved)
# the application is the executive layer. my code needs to be updated so that the application layer receives the user input before the game does. 
# if the user input is an application keyword (such as "SAVE" or "QUIT"), then execute those functions. 
# Otherwise, pass whatever the user's input was (presumably their move in long algebraic notation) to the game loop for processing in the game.
class ChessApp():
    def __init__(self):
        self.exit = False
        self.isGameRunning = False
        while not self.exit:
            match self.isGameRunning:
                case True: # this is the "game" case (the game is running, so go to the game)
                    self.mainGame.gameLoop()
                case False: # this is the "menu" case (the game is not running, so go to the menu)
                    self.userInput = input("Welcome to Chess in Python. To start a new game, type: NEW. ")
                    match self.userInput:
                        case "NEW":
                            self.mainGame = NewGame()
                            self.isGameRunning = True

if __name__ == "__main__":
    main = ChessApp()

