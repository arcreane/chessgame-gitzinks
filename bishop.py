from piece import Piece
from position import Position


class Bishop(Piece):
    """Classe pour le Fou."""

    def __init__(self, position: Position, color: int):
        super().__init__(position, color)

    def __str__(self):
        """Identifiant de la piece."""
        return "B"

    def isValidMove(self, newPosition: Position, board) -> bool:

        ecart_lig = abs(self.position.row - newPosition.row)
        ecart_col = abs(ord(self.position.column) - ord(newPosition.column))


        if ecart_lig == ecart_col and ecart_lig > 0:
            return True

        return False


# Tests de validation
if __name__ == "__main__":
    pos_dep = Position("e", 4)
    mon_fou = Bishop(pos_dep, 0)
    print("--- Test du Fou (Code Final) ---")

    # Test 1 : Diagonale haut-gauche
    print(f"Test 1 (Valide) -> {mon_fou.isValidMove(Position('c', 6), None)}")

    # Test 2 : Diagonale bas-droite
    print(f"Test 2 (Valide) -> {mon_fou.isValidMove(Position('g', 2), None)}")

    # Test 3 : Pas une diagonale
    print(f"Test 3 (Invalide) -> {mon_fou.isValidMove(Position('e', 6), None)}")