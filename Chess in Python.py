from __future__ import annotations
from enum import Enum, auto

# Global Variables
emptyCell = ''

# global utility function for checking the validity of the move which a player wants to make
def askForValidMove(message: str, piece: Piece):
    print(message)
    userInputX = askFor1To8("What is the posX of the position you want to move to? ") - 1
    userInputY = askFor1To8("What is the posY of the position you want to move to? ") - 1
    if piece.isMoveValid(userInputX,userInputY):
        ##### TODO: if move is valid, do the move
        return True
    else:
        # try again (recursively)
        return askForValidMove("That's not a valid move, try again. ", piece)

# global utlity function to check if the user input is an int between 1 and 8.
# to be used when validating user inputs of board positions for selecting a piece they want to move.
def askFor1To8(message: str) -> int:  # get input from user with message
    # check if userInput is a string; pass if the ValueError is thrown
    userInput = input(message)
    try:
        userInput = int(userInput)
    except ValueError:
        userInput = -1
        pass
    if userInput <= 8 and userInput > 0:  # validate that the userInput is between 1 and 8
        return (userInput)
    # recursively return a call of the function if the user input is invalid
    return askFor1To8("Try again ")

# global utility function for checking if a piece move is valid
def askForValidPiece(message: str) -> Piece:
    # ask the user to input the X position for the piece they want to move
    print(message)
    # ask the user to input the Y position fro the piece they want to move
    userInputX = askFor1To8("What is the posX? ")-1
    # assign the piece corresponding to the user's X and Y inputs to a variable called userSelection
    userInputY = askFor1To8("What is the posY? ")-1
    # check if the userSelection piece is the same colour as the player making the selection
    userSelection = game.gameBoard.getPiece(userInputX, userInputY)
    if userSelection.colour == game.whichTurn:  # if the piece colour is correct, return the selected piece
        return userSelection
    # check if userSelection is a Piece (vs an empty board position):
    if userSelection == emptyCell:
        return askForValidPiece("There's are no pieces on this board position, try again. ")
    # if the colour is wrong, recursively call this function and tell the user they are an idiot for choosing the wrong-coloured piece. Because they are an idiot and it's important they know it.
    return askForValidPiece("Wrong colour, try again ")

class Colour(Enum):  # class used to enumerate white and black for inheritance in other objects (such as Piece objects)
    WHITE = auto()
    BLACK = auto()

    def __str__(self):  # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'

    __repr__ = __str__  # you have to explicitly tell python to reassign the new __str__ output as the the __repr__ output for the class, if you do not, it will continue to print the memory address of the given objecft

class ChessBoard:
    # define the initial board as a 2D array, where '' represents an empty square
    board = [[emptyCell for j in range(8)] for i in range(8)]

    def __init__(self):  # initialize the board with Pieces
        # assigns each white piece to it's initial position on the board
        self.board[0][0] = RookPiece(Colour.WHITE, 0, 0)
        self.board[0][1] = KnightPiece(Colour.WHITE, 0, 1)
        self.board[0][2] = BishopPiece(Colour.WHITE, 0, 2)
        self.board[0][3] = QueenPiece(Colour.WHITE, 0, 3)
        self.board[0][4] = KingPiece(Colour.WHITE, 0, 4)
        self.board[0][5] = BishopPiece(Colour.WHITE, 0, 5)
        self.board[0][6] = KnightPiece(Colour.WHITE, 0, 6)
        self.board[0][7] = RookPiece(Colour.WHITE, 0, 7)
        # assign each pawn to it's initial position on the board
        for i in range(8):
            self.board[1][i] = PawnPiece(Colour.WHITE, 1, i)
            self.board[6][i] = PawnPiece(Colour.BLACK, 6, i)
        # assign each black piece to it's initial position on the board
        self.board[7][0] = RookPiece(Colour.BLACK, 7, 0)
        self.board[7][1] = KnightPiece(Colour.BLACK, 7, 1)
        self.board[7][2] = BishopPiece(Colour.BLACK, 7, 2)
        self.board[7][3] = QueenPiece(Colour.BLACK, 7, 3)
        self.board[7][4] = KingPiece(Colour.BLACK, 7, 4)
        self.board[7][5] = BishopPiece(Colour.BLACK, 7, 5)
        self.board[7][6] = KnightPiece(Colour.BLACK, 7, 6)
        self.board[7][7] = RookPiece(Colour.BLACK, 7, 7)

    # method to find the piece on a specified position of the board
    def getPiece(self, x: int, y: int) -> Piece:
        return self.board[x][y]

    def __str__(self):  # redefine the __str__ special function to print the chess board out with new lines after every outer list element
        ret = ""
        for i in range(8):
            ret = ret + str(self.board[i]) + "\n"
        return ret


class Piece:  # defines the basic attributes of a Piece object
    posX: int
    posY: int
    colour: Colour
    fullName: str
    shortName: str

    def __init__(self, colour: Colour, posX: int, posY: int):
        self.posX = posX
        self.posY = posY
        self.colour = colour

    # this will not ever actually be called. It's just a placeholder for function
    def isMoveValid(self, x: int, y: int):
        return True

    # redefine the __str__ special function to print the piece to the terminal in format [colour][shortName]
    def __str__(self) -> str:
        return str(self.colour) + self.shortName

    __repr__ = __str__

# define objects for each chess piece (inherits from Piece)


class PawnPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "Pawn"
        self.shortName = "P"


class RookPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "Rook"
        self.shortName = "R"


class KnightPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "Knight"
        self.shortName = "N"


class BishopPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "Bishop"
        self.shortName = "B"


class KingPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "King"
        self.shortName = "K"


class QueenPiece(Piece):
    def __init__(self, colour: Colour, posX: int, posY: int):
        super().__init__(colour, posX, posY)
        self.fullName = "Queen" 
        self.shortName = "Q"


class GameState:  # GameState stores all relevant attributes of the given game's state.
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    turnCounter: int = 0
    # whichColour indicates whose turn it is (starting with White by default)
    whichTurn: Colour = Colour.WHITE


game = GameState()  # assign a new instance of the GameState object to the variable game

while True:  # Driver code
    print("\n")
    print("This game is called chess. There are two players; White (aka W) and Black (aka B). Each player starts with the same number and type of pieces.\n")
    print(f"It is {str(game.whichTurn)}'s turn.\n Here is the game board: \n")
    print(game.gameBoard)
    # ask the player for the x and y values of the piece which they'd like to move.
    userPieceChoice = askForValidPiece(f"It's {str(game.whichTurn)}'s turn")
    print(f"you selected this piece: {userPieceChoice}")
    # 
    userMoveChoice = askForValidMove("",userPieceChoice)



    break    # exit out of the Driver code
