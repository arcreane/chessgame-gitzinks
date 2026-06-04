from position import Position
from rook import Rook
from pawn import Pawn
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King


class Board:
    def __init__(self):
        # Dictionnaire : clé = "e4", valeur = objet Piece
        self.grid = {}
        self._initBoard()

    def _initBoard(self):
        cols = 'abcdefgh'
        # Pions
        for c in cols:
            self.grid[f"{c}2"] = Pawn(0, Position(c, 2))   # Blancs
            self.grid[f"{c}7"] = Pawn(1, Position(c, 7))   # Noirs

        # Pièces blanches
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, cls in enumerate(order):
            c = cols[i]
            self.grid[f"{c}1"] = cls(0, Position(c, 1))
            self.grid[f"{c}8"] = cls(1, Position(c, 8))

    def getPiece(self, position):
        return self.grid.get(str(position), None)

    def getPosition(self, piece):
        for key, p in self.grid.items():
            if p is piece:
                return p.position
        return None

    def movePiece(self, fromPos, toPos):
        key_from = str(fromPos)
        key_to = str(toPos)
        piece = self.grid.pop(key_from, None)
        if piece:
            piece.position = toPos
            self.grid[key_to] = piece

    def display(self):
        cols = 'abcdefgh'
        print("  a b c d e f g h")
        for row in range(8, 0, -1):
            line = f"{row} "
            for col in cols:
                piece = self.getPiece(Position(col, row))
                if piece:
                    symbol = str(piece)
                    # Minuscule = noir, majuscule = blanc
                    line += (symbol if piece.color == 0 else symbol.lower()) + " "
                else:
                    line += ". "
            print(line)
        print()


if __name__ == "__main__":
    b = Board()
    b.display()
    print("Tests Board OK !")