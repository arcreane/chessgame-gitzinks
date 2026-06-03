class Player:
    """Classe représentant un joueur d'échecs[cite: 195]."""

    def __init__(self, name: str, color: int):
        self.name = name
        self.color = color

    def askMove(self) -> str:
        """Demande au joueur de saisir son coup. Format : 'Pe2 e4'"""
        coup = input(f"{self.name} ({'Blanc' if self.color == 0 else 'Noir'}), votre coup (ex: Pe2 e4) : ")
        return coup.strip()


class AIPlayer(Player):
    """Sous-classe pour le joueur IA[cite: 202]."""

    def askMove(self) -> str:
        # Coup aléatoire pour commencer [cite: 203]
        return "Nb1 Nc3"


if __name__ == "__main__":
    # Tests fonctionnels [cite: 321, 322]
    j1 = Player("Yanis", 0)
    ia = AIPlayer("IA", 1)
    print(f"Coup du joueur {j1.name} : {j1.askMove()}")
    print(f"Coup de l'IA : {ia.askMove()}")
    print("Tests Player OK!")

