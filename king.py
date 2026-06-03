# king.py
from piece import Piece


class King(Piece):
    """Roi : se déplace d'une case dans toutes les directions."""

    def __str__(self):
        return 'K'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour un roi."""
        cols = 'abcdefgh'
        dc = abs(cols.index(newPosition.column) - cols.index(self.position.column))
        dr = abs(newPosition.row - self.position.row)

        # Maximum 1 case dans n'importe quelle direction
        if dc > 1 or dr > 1:
            return False

        # Pas de capture d'allié
        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False

        return True


if __name__ == "__main__":
    from position import Position
    from board import Board
    b = Board()
    king = b.getPiece(Position('e', 1))
    print(f"Roi en e1 : {king}")
    print("Tests King OK !")