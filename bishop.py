# bishop.py
from piece import Piece

class Bishop(Piece):
    def __str__(self):
        return 'B'

    def isValidMove(self, newPosition, board):
        cols = 'abcdefgh'
        c1 = cols.index(self.position.column)
        c2 = cols.index(newPosition.column)
        r1 = self.position.row
        r2 = newPosition.row

        # Diagonale = différence colonne == différence ligne
        if abs(c2 - c1) != abs(r2 - r1):
            return False

        # Vérifier le chemin libre
        dc = 1 if c2 > c1 else -1
        dr = 1 if r2 > r1 else -1
        c, r = c1 + dc, r1 + dr
        while c != c2:
            from position import Position
            if board.getPiece(Position(cols[c], r)) is not None:
                return False
            c += dc
            r += dr

        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False
        return True