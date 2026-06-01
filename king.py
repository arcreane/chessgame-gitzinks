# king.py
from piece import Piece

class King(Piece):
    def __str__(self):
        return 'K'

    def isValidMove(self, newPosition, board):
        cols = 'abcdefgh'
        dc = abs(cols.index(newPosition.column) - cols.index(self.position.column))
        dr = abs(newPosition.row - self.position.row)

        # Le roi avance d'une case dans toutes les directions
        if dc > 1 or dr > 1:
            return False

        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False
        return True