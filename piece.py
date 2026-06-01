from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color, position):
        self.color = color        # 0 = blanc, 1 = noir
        self.position = position  # objet Position

    @abstractmethod
    def isValidMove(self, newPosition, board):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Rook(Piece):
    def __str__(self):
        return 'R'

    def isValidMove(self, newPosition, board):
        # La tour se déplace en ligne droite (même colonne OU même ligne)
        sameCol = self.position.column == newPosition.column
        sameRow = self.position.row == newPosition.row

        if not sameCol and not sameRow:
            return False  # Pas en ligne droite

        # Vérifier qu'il n'y a pas de pièce sur le chemin
        if sameCol:
            minRow = min(self.position.row, newPosition.row) + 1
            maxRow = max(self.position.row, newPosition.row)
            for r in range(minRow, maxRow):
                from position import Position
                if board.getPiece(Position(self.position.column, r)) is not None:
                    return False
        else:
            cols = 'abcdefgh'
            c1 = cols.index(self.position.column)
            c2 = cols.index(newPosition.column)
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                from position import Position
                if board.getPiece(Position(cols[c], self.position.row)) is not None:
                    return False

        # Vérifier qu'on ne capture pas une pièce de même couleur
        target = board.getPiece(newPosition)
        if target is not None and target.color == self.color:
            return False

        return True


if __name__ == "__main__":
    from position import Position
    from board import Board
    b = Board()
    rook = b.getPiece(Position('a', 1))
    print(f"Tour en a1 : {rook}")
    print("Tests Piece/Rook OK !")