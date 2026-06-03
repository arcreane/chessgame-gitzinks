# knight.py
from piece import Piece


class Knight(Piece):
    """Cavalier : se déplace en L (2+1 cases), peut sauter par-dessus les pièces."""

    def __str__(self):
        return 'N'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour un cavalier."""
        cols = 'abcdefgh'
        dc = abs(cols.index(newPosition.column) - cols.index(self.position.column))
        dr = abs(newPosition.row - self.position.row)

        # Déplacement en L : (2,1) ou (1,2)
        if not ((dc == 2 and dr == 1) or (dc == 1 and dr == 2)):
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
    knight = b.getPiece(Position('b', 1))
    print(f"Cavalier en b1 : {knight}")
    print(f"b1->c3 valide ? {knight.isValidMove(Position('c', 3), b)}")   # True
    print(f"b1->b3 invalide ? {knight.isValidMove(Position('b', 3), b)}") # False
    print("Tests Knight OK !")