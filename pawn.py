# pawn.py
from piece import Piece


class Pawn(Piece):
    """Pion : avance d'une case, deux au premier coup, capture en diagonale."""

    def __init__(self, color: int, position):
        super().__init__(color, position)
        self.has_moved = False

    def __str__(self):
        return 'P'

    def isValidMove(self, newPosition, board):
        return True