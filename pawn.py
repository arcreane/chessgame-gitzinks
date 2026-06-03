# pawn.py
from piece import Piece


class Pawn(Piece):
    """Pion : avance d'une case, deux au premier coup, capture en diagonale."""

    def __init__(self, color: int, position):
        """
        :param color: 0 = blanc, 1 = noir
        :param position: objet Position
        """
        super().__init__(color, position)
        self.has_moved = False  # True après le premier déplacement

    def __str__(self):
        return 'P'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour un pion."""
        from position import Position
        col = self.position.column
        row = self.position.row
        direction = 1 if self.color == 0 else -1  # blanc monte, noir descend

        # Avancer d'une case tout droit
        if col == newPosition.column and newPosition.row == row + direction:
            if board.getPiece(newPosition) is None:
                return True

        # Avancer de 2 cases au premier coup
        startRow = 2 if self.color == 0 else 7
        if (col == newPosition.column
                and row == startRow
                and not self.has_moved
                and newPosition.row == row + 2 * direction):
            middle = Position(col, row + direction)
            if board.getPiece(middle) is None and board.getPiece(newPosition) is None:
                return True

        # Capture en diagonale
        cols = 'abcdefgh'
        colIdx = cols.index(col)
        diag_cols = []
        if colIdx > 0:
            diag_cols.append(cols[colIdx - 1])
        if colIdx < 7:
            diag_cols.append(cols[colIdx + 1])

        if newPosition.row == row + direction and newPosition.column in diag_cols:
            target = board.getPiece(newPosition)
            if target is not None and target.color != self.color:
                return True

        return False


if __name__ == "__main__":
    from position import Position
    from board import Board
    b = Board()
    pawn = b.getPiece(Position('e', 2))
    print(f"Pion en e2 : {pawn}")
    print(f"e2->e3 valide ? {pawn.isValidMove(Position('e', 3), b)}")   # True
    print(f"e2->e4 valide ? {pawn.isValidMove(Position('e', 4), b)}")   # True
    print(f"e2->e5 invalide ? {pawn.isValidMove(Position('e', 5), b)}") # False
    print("Tests Pawn OK !")