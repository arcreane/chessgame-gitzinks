class Bishop(Piece):
    
    def isValidMove(self, newPosition: Position, board) -> bool:
        return True

    def str(self):
        return "B"

class Queen(Piece):

    def isValidMove(self, newPosition: Position, board) -> bool:
        return True

    def str(self):
        return "Q"