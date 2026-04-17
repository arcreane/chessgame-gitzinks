from position import Position
from piece import Piece, Rook

class Board:
    def __init__(self):
        self.pieces = {}

    def getPosition(self, piece: Piece):
        for pos_str, p in self.pieces.items():
            if p == piece:
                return p.position
        return None

    def getPiece(self, position: Position):
        return self.pieces.get(str(position), None)

if __name__ == "__main__":
    plateau = Board()
    pos = Position("a", 1)
    tour = Rook(pos, 0)
    plateau.pieces[str(pos)] = tour
    print(f"Pièce en a1 : {plateau.getPiece(pos)}")