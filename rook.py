from piece import Piece


class Rook(Piece):
    """Tour : se déplace en ligne droite."""

    def __str__(self):
        return 'R'

    def isValidMove(self, newPosition, board):
        return True