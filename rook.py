# rook.py
from piece import Piece


class Rook(Piece):
    """Tour : se déplace en ligne droite (même colonne ou même ligne)."""

    def __str__(self):
        return 'R'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour une tour."""
        from position import Position
        cols = 'abcdefgh'
        sameCol = self.position.column == newPosition.column
        sameRow = self.position.row == newPosition.row

        if not sameCol and not sameRow:
            return False

        # Vérifier chemin dispo colonne
        if sameCol:
            minRow = min(self.position.row, newPosition.row) + 1
            maxRow = max(self.position.row, newPosition.row)
            for r in range(minRow, maxRow):
                if board.getPiece(Position(self.position.column, r)) is not None:
                    return False
        # Vérifier chemin dispo ligne
        else:
            c1 = cols.index(self.position.column)
            c2 = cols.index(newPosition.column)
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                if board.getPiece(Position(cols[c], self.position.row)) is not None:
                    return False

        # Pas  capture d'allié
        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False

        return True


if __name__ == "__main__":
    from position import Position
    from board import Board
    b = Board()
    rook = b.getPiece(Position('a', 1))
    print(f"Tour en a1 : {rook}")
    print(f"a1->a3 valide ? {rook.isValidMove(Position('a', 3), b)}")  # False (pion bloque)
    print("Tests Rook OK !")