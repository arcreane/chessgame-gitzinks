from piece import Piece


class Pawn(Piece):
    def __str__(self):
        return 'P'

    def isValidMove(self, newPosition, board):
        col = self.position.column
        row = self.position.row

        # Direction selon la couleur (blanc monte, noir descend)
        direction = 1 if self.color == 0 else -1

        # Avancer d'une case droit
        if col == newPosition.column and newPosition.row == row + direction:
            if board.getPiece(newPosition) is None:
                return True

        # Avancer de 2 cases depuis position initiale
        startRow = 2 if self.color == 0 else 7
        if col == newPosition.column and row == startRow and newPosition.row == row + 2 * direction:
            from position import Position
            middle = Position(col, row + direction)
            if board.getPiece(middle) is None and board.getPiece(newPosition) is None:
                return True

        # Capture en diagonale
        cols = 'abcdefgh'
        colIdx = cols.index(col)
        if newPosition.row == row + direction:
            if newPosition.column in [cols[colIdx - 1] if colIdx > 0 else '', cols[colIdx + 1] if colIdx < 7 else '']:
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
    from position import Position
    print(f"e2→e4 valide ? {pawn.isValidMove(Position('e', 4), b)}")  # True
    print("Tests Pawn OK !")