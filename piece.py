from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color, position):
        self.color = color        # 0 = blanc, 1 = noir
        self.position = position  # objet Position

    @abstractmethod
    def isValidMove(self, newPosition, board):
        pass

    @abstractmethod
    def __str__(self):  #return lettre piece
        pass
if __name__ == "__main__":
    print("Piece est abstraite, pas de test direct.")
    print("Tests Piece OK ")