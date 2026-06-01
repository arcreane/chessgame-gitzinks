# knight.py
from piece import Piece

class Knight(Piece):
    def __str__(self):
        return 'N'

    def isValidMove(self, newPosition, board):
        cols = 'abcdefgh'
        dc = abs(cols.index(newPosition.column) - cols.index(self.position.column))
        dr = abs(newPosition.row - self.position.row)

        # Le cavalier fait un L : (2,1) ou (1,2)
        if not ((dc == 2 and dr == 1) or (dc == 1 and dr == 2)):
            return False

        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False
        return True