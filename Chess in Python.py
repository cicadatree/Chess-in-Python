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
    colour: Colour
@dataclass
class RookPiece:
    colour: Colour
@dataclass
class KnightPiece: 
    colour: Colour
@dataclass
class BishopPiece: 
    colour: Colour
@dataclass
class KingPiece: 
    colour: Colour
@dataclass
class QueenPiece: 
    colour: Colour

while True:
    gameBoard = ChessBoard()

    whiteRook1 = RookPiece(Colour.WHITE)
    gameBoard.board[0][0] = whiteRook1
    whiteKnight1 = KnightPiece(Colour.WHITE)
    gameBoard.board[0][1] = whiteKnight1
    whiteBishop1 =  BishopPiece(Colour.WHITE)
    gameBoard.board[0][2] = whiteBishop1
    whiteQueen = QueenPiece(Colour.WHITE)
    gameBoard.board[0][3] = whiteQueen
    whiteKing = KingPiece(Colour.WHITE)
    gameBoard.board[0][4] = whiteKing
    whiteBishop2 = BishopPiece(Colour.WHITE)
    gameBoard.board[0][5] = whiteBishop2
    whiteKnight2 = KnightPiece(Colour.WHITE)
    gameBoard.board[0][6] = whiteKnight2
    whiteRook2 = RookPiece(Colour.WHITE)
    gameBoard.board[0][7] = whiteRook2

    # I need to figure out how to get pawn's assigned to discrete / distinct variables
    for i in range(8):
        gameBoard.board[1][i] = PawnPiece(Colour.WHITE)
        gameBoard.board[6][i] = PawnPiece(Colour.BLACK)

    blackRook1 = RookPiece(Colour.BLACK)
    gameBoard.board[7][0] = blackRook1
    blackKnight1 = KnightPiece(Colour.BLACK)
    gameBoard.board[7][1] = blackKnight1
    blackBishop1 = BishopPiece(Colour.BLACK)
    gameBoard.board[7][2] = blackBishop1
    blackQueen = QueenPiece(Colour.BLACK)
    gameBoard.board[7][3] = blackQueen
    blackKing = KingPiece(Colour.BLACK)
    gameBoard.board[7][4] = blackKing
    blackBishop2 = BishopPiece(Colour.BLACK)
    gameBoard.board[7][5] = blackBishop2
    blackKnight2 = KnightPiece(Colour.BLACK)
    gameBoard.board[7][6] = blackKnight2
    blackRook2 = RookPiece(Colour.BLACK)
    gameBoard.board[7][7] = blackRook2

    print(gameBoard.board)
    break