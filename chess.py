# chess.py
import random
import json
from board import Board
from position import Position
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King


class Player:
    """Joueur humain."""

    def __init__(self, name: str, color: int):
        """
        :param name: nom du joueur
        :param color: 0 = blanc, 1 = noir
        """
        self.name = name
        self.color = color

    def askMove(self) -> str:
        """Demande au joueur de saisir son coup. Format : 'Pe2 e4'"""
        coup = input(f"{self.name} ({'Blanc' if self.color == 0 else 'Noir'}), entrez votre coup (ex: Pe2 e4) : ")
        return coup.strip()


class AIPlayer(Player):
    """Joueur IA — le coup est calculé dans Chess._getAIMove()."""

    def askMove(self) -> str:
        """Retourne une string vide, le coup est généré par Chess."""
        return ""


class Chess:
    """Moteur principal du jeu d'échecs."""

    def __init__(self):
        self.board = Board()          # Le plateau avec toutes les pièces
        self.players = []             # Liste des 2 joueurs
        self.currentPlayer = None     # Joueur qui a la main

    def initPlayers(self):
        """Crée les deux joueurs. Instancie AIPlayer si le nom saisi est 'AI'."""
        self.players = []
        for color, label in [(0, 'Blanc'), (1, 'Noir')]:
            nom = input(f"Nom du joueur {label} (ou 'AI') : ").strip()
            if nom.upper() == "AI":
                self.players.append(AIPlayer(nom, color))
            else:
                self.players.append(Player(nom, color))
        self.currentPlayer = self.players[0]  # Les blancs commencent

    def displayBoard(self):
        """Affiche le plateau 8x8 en mode texte. Majuscules=blancs, minuscules=noirs."""
        print("\n    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for row in range(8, 0, -1):
            ligne = f"{row} |"
            for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                piece = self.board.getPiece(Position(col, row))
                if piece is None:
                    ligne += "   |"
                elif piece.color == 0:
                    ligne += f" {str(piece).upper()} |"
                else:
                    ligne += f" {str(piece).lower()} |"
            print(ligne)
            print("  +---+---+---+---+---+---+---+---+")
        print()

    def isValidMove(self, move: str) -> bool:
        """
        Vérifie si la string move correspond à un coup légal.
        Format attendu : 'Pe2 e4' (type + case départ + espace + case arrivée)
        """
        try:
            pos_dep  = Position(move[1], int(move[2]))
            pos_dest = Position(move[4], int(move[5]))
            piece    = self.board.getPiece(pos_dep)
            if piece is None:
                print("Aucune pièce à cet emplacement.")
                return False
            if str(piece).upper() != move[0].upper():
                print(f"La pièce en {pos_dep} n'est pas '{move[0]}'.")
                return False
            if piece.color != self.currentPlayer.color:
                print("Cette pièce ne vous appartient pas.")
                return False
            return piece.isValidMove(pos_dest, self.board)
        except (IndexError, ValueError):
            print("Format invalide. Exemple : Pe2 e4")
            return False

    def updateBoard(self, move: str):
        """Déplace la pièce sur le plateau selon la string move."""
        pos_dep  = Position(move[1], int(move[2]))
        pos_dest = Position(move[4], int(move[5]))
        piece    = self.board.getPiece(pos_dep)
        del self.board.pieces[str(pos_dep)]
        piece.position = pos_dest
        if str(piece) == 'P':
            piece.has_moved = True
        self.board.pieces[str(pos_dest)] = piece

    def isCheckMate(self) -> bool:
        """Détecte l'échec et mat. TODO : implémenter la vraie détection."""
        return False

    def switchPlayer(self):
        """Passe la main à l'autre joueur."""
        self.currentPlayer = (
            self.players[1] if self.currentPlayer == self.players[0]
            else self.players[0]
        )

    def saveGame(self, filename: str = "sauvegarde.json"):
        """Sauvegarde l'état complet de la partie dans un fichier JSON."""
        data = {
            "currentPlayer": self.currentPlayer.color,
            "pieces": {
                pos: {"type": str(p), "color": p.color, "has_moved": getattr(p, 'has_moved', False)}
                for pos, p in self.board.pieces.items()
            }
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Partie sauvegardée dans '{filename}'.")

    def loadGame(self, filename: str = "sauvegarde.json"):
        """Restaure une partie depuis un fichier JSON."""
        piece_classes = {'P': Pawn, 'R': Rook, 'B': Bishop, 'N': Knight, 'Q': Queen, 'K': King}
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.board.pieces = {}
            for pos_str, info in data["pieces"].items():
                col = pos_str[0]
                row = int(pos_str[1])
                pos = Position(col, row)
                cls = piece_classes.get(info["type"])
                if cls:
                    piece = cls(info["color"], pos)
                    if info["type"] == 'P':
                        piece.has_moved = info["has_moved"]
                    self.board.pieces[pos_str] = piece
            for player in self.players:
                if player.color == data["currentPlayer"]:
                    self.currentPlayer = player
                    break
            print(f"Partie restaurée depuis '{filename}'.")
        except FileNotFoundError:
            print(f"Fichier '{filename}' introuvable.")
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")

    def _getAIMove(self) -> str:
        """Génère un coup aléatoire valide pour l'IA."""
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        pieces_ia = [p for p in self.board.pieces.values()
                     if p.color == self.currentPlayer.color]
        random.shuffle(pieces_ia)
        for piece in pieces_ia:
            cases = [Position(c, r) for c in cols for r in range(1, 9)]
            random.shuffle(cases)
            for dest in cases:
                if piece.isValidMove(dest, self.board):
                    return f"{str(piece)}{piece.position.column}{piece.position.row} {dest.column}{dest.row}"
        return ""

    def play(self):
        """Boucle principale de la partie d'échecs."""
        print("=== JEU D'ÉCHECS ===\n")
        self.initPlayers()
        if input("Charger une partie sauvegardée ? (o/n) : ").strip().lower() == 'o':
            self.loadGame()
        while not self.isCheckMate():
            self.displayBoard()
            print(f"Tour de : {self.currentPlayer.name} ({'Blanc' if self.currentPlayer.color == 0 else 'Noir'})")
            if isinstance(self.currentPlayer, AIPlayer):
                move = self._getAIMove()
                if not move:
                    print("L'IA n'a aucun coup valide. Fin de partie.")
                    break
                print(f"L'IA joue : {move}")
            else:
                move = ""
                while not self.isValidMove(move):
                    move = self.currentPlayer.askMove()
            self.updateBoard(move)
            if input("Sauvegarder la partie ? (o/n) : ").strip().lower() == 'o':
                self.saveGame()
            self.switchPlayer()
        print("Fin de la partie !")


if __name__ == "__main__":
    Chess().play()