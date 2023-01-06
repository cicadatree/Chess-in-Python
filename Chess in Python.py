from dataclasses import dataclass
from typing import List
from enum import Enum, auto

@dataclass
class ChessBoard:
    board = [[None for j in range(8)] for i in range(8)]
    # define the initial board as a 2D array
    # board is a list of lists representing the state of the chessboard
    # None represents an empty square
    # the outer list represents the rows of the board (8 rows)
    # the inner list represents the columns of the board (8 columns)

class Colour(Enum):
    WHITE = auto()
    BLACK = auto()

@dataclass
class PawnPiece: 
    colour: Colour.WHITE or Colour.BLACK

@dataclass
class RookPiece: 
    colour: Colour.WHITE or Colour.BLACK

@dataclass
class KnightPiece: 
    colour: Colour.WHITE or Colour.BLACK

@dataclass
class BishopPiece: 
    colour: Colour.WHITE or Colour.BLACK

@dataclass
class KingPiece: 
    colour: Colour.WHITE or Colour.BLACK

@dataclass
class QueenPiece: 
    colour: Colour.WHITE or Colour.BLACK

  #### I need to fix this. remember: you're assigning instances of each piece to specific variables, and THEN assigning those variables to their starting positions on the gameBoard.board


while True:
    gameBoard = ChessBoard()

    whiteRook1 = RookPiece("WHITE")
    gameBoard.board[0][0] = whiteRook1
    whiteKnight1 = KnightPiece("WHITE")
    gameBoard.board[0][1] = whiteKnight1
    whiteBishop1 =  BishopPiece("WHITE")
    gameBoard.board[0][2] = whiteBishop1
    whiteQueen = QueenPiece("WHITE")
    gameBoard.board[0][3] = whiteQueen
    whiteKing = KingPiece("WHITE")
    gameBoard.board[0][4] = whiteKing
    whiteBishop2 = BishopPiece("WHITE")
    gameBoard.board[0][5] = whiteBishop2
    whiteKnight2 = KnightPiece("WHITE")
    gameBoard.board[0][6] = whiteKnight2
    whiteRook2 = RookPiece("WHITE")
    gameBoard.board[0][7] = whiteRook2
            
    for i in range(8):
        gameBoard.board[1][i] = PawnPiece("WHITE")
        gameBoard.board[6][i] = PawnPiece("BLACK")

    blackRook1 = RookPiece("BLACK")
    gameBoard.board[7][0] = blackRook1
    blackKnight1 = KnightPiece("BLACK")
    gameBoard.board[7][1] = blackKnight1
    blackBishop1 = BishopPiece("BLACK")
    gameBoard.board[7][2] = blackBishop1
    blackQueen = QueenPiece("BLACK")
    gameBoard.board[7][3] = blackQueen
    blackKing = KingPiece("BLACK")
    gameBoard.board[7][4] = blackKing
    blackBishop2 = BishopPiece("BLACK")
    gameBoard.board[7][5] = blackBishop2
    blackKnight2 = KnightPiece("BLACK")
    gameBoard.board[7][6] = blackKnight2
    blackRook2 = RookPiece("BLACK")
    gameBoard.board[7][7] = blackRook2

    print(gameBoard.board)
    break