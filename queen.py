# queen.py
from piece import Piece


class Queen(Piece):
    """Reine : combine les mouvements de la tour et du fou."""

    def __str__(self):
        return 'Q'

    def isValidMove(self, newPosition, board):
        """Retourne True si le déplacement est valide pour une reine."""
        from rook import Rook
        from bishop import Bishop
        # La reine se déplace comme une tour OU comme un fou
        fake_rook = Rook(self.color, self.position)
        fake_bishop = Bishop(self.color, self.position)
        return (fake_rook.isValidMove(newPosition, board)
                or fake_bishop.isValidMove(newPosition, board))