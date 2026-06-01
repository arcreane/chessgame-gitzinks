# queen.py — combine Tour + Fou
from piece import Piece
from rook import Rook
from bishop import Bishop

class Queen(Piece):
    def __str__(self):
        return 'Q'

    def isValidMove(self, newPosition, board):
        # La reine = tour OU fou (même déplacement)
        fake_rook = Rook(self.color, self.position)
        fake_bishop = Bishop(self.color, self.position)
        return fake_rook.isValidMove(newPosition, board) or fake_bishop.isValidMove(newPosition, board)