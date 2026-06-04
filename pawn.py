from piece import Piece
from position import Position


class Pawn(Piece):
    """Pion : avance tout droit, capture en diagonale."""

    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False  # Pour autoriser le coup de 2 cases au départ

    def __str__(self):
        return "P"

    def isValidMove(self, newPosition, board):
        # Direction : blanc monte (+1), noir descend (-1)
        direction = 1 if self.color == 0 else -1

        diff_col = ord(newPosition.column) - ord(self.position.column)
        diff_row = newPosition.row - self.position.row

        # Cas 1 : avancer d'une case tout droit (case vide)
        if diff_col == 0 and diff_row == direction:
            return board.getPiece(newPosition) is None

        # Cas 2 : avancer de 2 cases au premier coup (les 2 cases vides)
        if diff_col == 0 and diff_row == 2 * direction and not self.has_moved:
            case_du_milieu = Position(self.position.column, self.position.row + direction)
            return (board.getPiece(case_du_milieu) is None and
                    board.getPiece(newPosition) is None)

        # Cas 3 : capture en diagonale (1 case, ennemi présent)
        if abs(diff_col) == 1 and diff_row == direction:
            cible = board.getPiece(newPosition)
            return cible is not None and cible.color != self.color

        return False


if __name__ == "__main__":
    from board import Board
    b = Board()
    pion = b.getPiece(Position('e', 2))
    print(f"Pion en e2 : {pion}")
    print("Avance e3 :", pion.isValidMove(Position('e', 3), b))   # True
    print("Avance e4 :", pion.isValidMove(Position('e', 4), b))   # True
    print("Recule e1 :", pion.isValidMove(Position('e', 1), b))   # False
    print("Tests Pawn OK !")