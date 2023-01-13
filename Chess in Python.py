from __future__ import annotations
from enum import Enum, auto

# Global Variables
emptyCell = ''

# global utlity function to check if the user input is an int between 1 and 8. 
# to be used when validating user inputs of board positions for selecting a piece they want to move.
def askFor1To8(message) -> int:  # get input from user with message
    userInput = input(message) # check if userInput is a string; pass if the ValueError is thrown
    try:
        userInput = int(userInput)
    except ValueError:
        userInput = -1
        pass
    if userInput <= 8 and userInput > 0: # validate that the userInput is between 1 and 8
        return(userInput)
    return askFor1To8("Try again ") # recursively return a call of the function if the user input is invalid

# global utility function for checking if a piece move is valid
def askForValidPiece(message) -> Piece:
    print(message) # ask the user to input the X position for the piece they want to move
    userInputX = askFor1To8("What is the X? ")-1 # ask the user to input the Y position fro the piece they want to move
    userInputY = askFor1To8("What is the Y? ")-1 # assign the piece corresponding to the user's X and Y inputs to a variable called userSelection
    userSelection = game.gameBoard.getPiece(userInputX,userInputY) # check if the userSelection piece is the same colour as the player making the selection
    if userSelection.colour == game.whichTurn: # if the piece colour is correct, return the selected piece
        return userSelection
    if userSelection == emptyCell: # check if userSelection is a Piece (vs an empty board position):
        return askForValidPiece("")
    return askForValidPiece("Wrong colour, try again ") # if the colour is wrong, recursively call this function and tell the user they are an idiot for choosing the wrong-coloured piece. Because they are an idiot and it's important they know it.

class Colour(Enum):
    # enumerate white and black
    WHITE = auto()
    BLACK = auto()

    def __str__(self): # redefine the __str__ special function to print the Colour.WHITE as "W" and Colour.BLACK as "B" for legibility in the terminal
        if self.value == Colour.WHITE.value:
            return 'W'
        else:
            return 'B'

    __repr__ = __str__ # you have to explicitly tell python to reassign the new __str__ output as the the __repr__ output for the class, if you do not, it will continue to print the memory address of the given objecft

class ChessBoard:
    board = [[emptyCell for j in range(8)] for i in range(8)] # define the initial board as a 2D array, where '' represents an empty square
    
    def __init__(self): # initialize the board with Pieces
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
    
    def getPiece(self,x,y) -> Piece: # method to find the piece on a specified position of the board
        return self.board[x][y]
    
    def __str__(self): # redefine the __str__ special function to print the chess board out with new lines after every outer list element
        ret = ""
        for i in range(8):
            ret = ret + str(self.board[i]) + "\n"
        return ret

class Piece: # defines the basic attributes of a Piece object
    colour: Colour
    fullName: str
    shortName: str

    def __str__(self) -> str: # redefine the __str__ special function to print the 
        return str(self.colour) + self.shortName

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

class GameState: # GameState stores all relevant attributes of the given game's state.
    gameBoard: ChessBoard = ChessBoard()    # gameBoard is a ChessBoard-like object
    turnCounter: int = 0    # turnCounter starts on 0 and should increment by 1 at the end of each turn.
    whichTurn: Colour = Colour.WHITE    # whichColour indicates whose turn it is (starting with White by default)

game = GameState()  # assign a new instance of the GameState object to the variable game

while True: # Driver code
    print("\n")
    print("This game is called chess. There are two players; White (aka W) and Black (aka B). Each player starts with the same number and type of pieces.\n")
    print(f"It is {str(game.whichTurn)}'s turn.\n Here is the game board: \n")
    print(game.gameBoard)
    userPieceChoice = askForValidPiece(f"It's {str(game.whichTurn)}'s turn") # ask the player for the x and y values of the piece which they'd like to move.
    print(f"you selected this piece: {userPieceChoice}")

    break    # exit out of the Driver code