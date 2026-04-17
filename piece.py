from abc import ABC, abstractmethod
from position import Position


class Piece(ABC):
    def __init__(self, position: Position, color: int):
        self.position = position
        self.color = color  # 0 pour blanc, 1 pour noir

    @abstractmethod
    def isValidMove(self, newPosition: Position, board) -> bool:
        pass


class Rook(Piece):
    def isValidMove(self, newPosition: Position, board) -> bool:
        return True

    def __str__(self):
        return "R"


if __name__ == "__main__":
    pos = Position("a", 1)
    tour = Rook(pos, 0)
    print(f"Tour créée en {tour.position}")