# bishop.py
from piece import Piece


class Bishop(Piece):
    """Fou : se déplace en diagonale."""

    def __str__(self):
        return 'B'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour un fou."""
        from position import Position
        cols = 'abcdefgh'
        c1 = cols.index(self.position.column)
        c2 = cols.index(newPosition.column)
        r1 = self.position.row
        r2 = newPosition.row

        # Mouvement diagonal : différence colonne == différence ligne
        if abs(c2 - c1) != abs(r2 - r1):
            return False

        # Chemin libre
        dc = 1 if c2 > c1 else -1
        dr = 1 if r2 > r1 else -1
        c, r = c1 + dc, r1 + dr
        while c != c2:
            if board.getPiece(Position(cols[c], r)) is not None:
                return False
            c += dc
            r += dr

        # Pas de capture d'allié
        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False

        return True