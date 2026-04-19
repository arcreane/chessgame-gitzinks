import random
import json
from board import Board
from position import Position
from pawn import Pawn
from piece import Rook
from bishop import Bishop


# ============================================================
#  CLASSE PLAYER  —  un joueur humain
# ============================================================

class Player:
    """
    Représente un joueur humain.
    
    Attributs :
        name  (str) : le prénom du joueur
        color (int) : 0 = blanc, 1 = noir
    """

    def __init__(self, name: str, color: int):
        self.name  = name
        self.color = color

    def askMove(self) -> str:
        """
        Demande au joueur de saisir son coup dans le terminal.
        Format attendu : "Pe2 e4"  (identifiant + case départ + case arrivée)
        Exemple valides : "Pe2 e4", "Ra1 a4", "Bc1 f4"
        """
        coup = input(f"{self.name} ({'Blanc' if self.color == 0 else 'Noir'}), entrez votre coup (ex: Pe2 e4) : ")
        return coup.strip()


# ============================================================
#  CLASSE AIPLAYER  —  un joueur IA (coup aléatoire)
# ============================================================

class AIPlayer(Player):
    """
    Joueur IA qui génère un coup aléatoire valide.
    Hérite de Player et redéfinit askMove().
    """

    def askMove(self) -> str:
        """
        Génère automatiquement un coup aléatoire parmi les coups valides.
        Si aucun coup valide, retourne une chaîne vide.
        """
        # On a besoin du plateau pour chercher les coups valides
        # (board est passé via chess, voir play())
        return ""  # sera complété dans Chess.play() avec accès au board


# ============================================================
#  CLASSE CHESS  —  moteur principal du jeu
# ============================================================

class Chess:
    """
    Gère la partie d'échecs entre deux joueurs.
    
    Attributs :
        board         (Board)  : l'état du plateau
        players       (list)   : liste des 2 joueurs [blanc, noir]
        currentPlayer (Player) : le joueur qui doit jouer
    """

    def __init__(self):
        self.board         = Board()
        self.players       = []
        self.currentPlayer = None
        # On initialise le plateau avec toutes les pièces
        self._initBoard()

    # ----------------------------------------------------------
    #  Initialisation du plateau
    # ----------------------------------------------------------

    def _initBoard(self):
        """
        Place toutes les pièces à leur position de départ.
        Blancs en lignes 1 et 2, Noirs en lignes 7 et 8.
        """
        colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # --- Pions (ligne 2 pour blancs, ligne 7 pour noirs) ---
        for col in colonnes:
            # Pion blanc
            pos_b = Position(col, 2)
            self.board.pieces[str(pos_b)] = Pawn(pos_b, 0)
            # Pion noir
            pos_n = Position(col, 7)
            self.board.pieces[str(pos_n)] = Pawn(pos_n, 1)

        # --- Tours ---
        for col, color, row in [('a', 0, 1), ('h', 0, 1), ('a', 1, 8), ('h', 1, 8)]:
            pos = Position(col, row)
            self.board.pieces[str(pos)] = Rook(pos, color)

        # --- Fous (Bishop) ---
        for col, color, row in [('c', 0, 1), ('f', 0, 1), ('c', 1, 8), ('f', 1, 8)]:
            pos = Position(col, row)
            self.board.pieces[str(pos)] = Bishop(pos, color)

        # Note : Cavaliers, Reines, Rois seront ajoutés quand leurs fichiers seront prêts

    # ----------------------------------------------------------
    #  Initialisation des joueurs
    # ----------------------------------------------------------

    def initPlayers(self):
        """
        Demande les noms des joueurs.
        Si le nom saisi est 'AI', crée un AIPlayer à la place.
        """
        self.players = []

        for color, label in [(0, 'Blanc'), (1, 'Noir')]:
            nom = input(f"Entrez le nom du joueur {label} (tapez 'AI' pour l'IA) : ").strip()
            if nom.upper() == "AI":
                self.players.append(AIPlayer(nom, color))
            else:
                self.players.append(Player(nom, color))

        # Le joueur blanc commence toujours
        self.currentPlayer = self.players[0]

    # ----------------------------------------------------------
    #  Affichage du plateau
    # ----------------------------------------------------------

    def displayBoard(self):
        """
        Affiche le plateau dans le terminal sous forme de grille 8x8.
        Les pièces blanches sont en minuscules, les noires en MAJUSCULES.
        """
        print("\n    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")

        for row in range(8, 0, -1):  # de 8 à 1
            ligne = f"{row} |"
            for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                pos   = Position(col, row)
                piece = self.board.getPiece(pos)
                if piece is None:
                    ligne += "   |"
                elif piece.color == 0:  # blanc → minuscule
                    ligne += f" {str(piece).lower()} |"
                else:                   # noir → majuscule
                    ligne += f" {str(piece).upper()} |"
            print(ligne)
            print("  +---+---+---+---+---+---+---+---+")
        print()

    # ----------------------------------------------------------
    #  Validation d'un coup
    # ----------------------------------------------------------

    def isValidMove(self, move: str) -> bool:
        """
        Analyse la chaîne 'move' et vérifie si le coup est valide.
        
        Format attendu : "Pe2 e4"
          - move[0]    = identifiant de la pièce ('P', 'R', 'B', etc.)
          - move[1]    = colonne de départ ('a'–'h')
          - move[2]    = ligne de départ ('1'–'8')
          - move[4]    = colonne de destination
          - move[5]    = ligne de destination
        
        Retourne True si le coup est légal, False sinon.
        """
        try:
            # Découpage de la chaîne
            id_piece  = move[0]          # ex: 'P'
            col_dep   = move[1]          # ex: 'e'
            row_dep   = int(move[2])     # ex: 2
            col_dest  = move[4]          # ex: 'e'
            row_dest  = int(move[5])     # ex: 4

            pos_dep  = Position(col_dep,  row_dep)
            pos_dest = Position(col_dest, row_dest)

            # Récupérer la pièce à la position de départ
            piece = self.board.getPiece(pos_dep)

            # Vérifications de base
            if piece is None:
                print("Aucune pièce à cet emplacement.")
                return False
            if str(piece) != id_piece:
                print(f"La pièce en {pos_dep} n'est pas un(e) '{id_piece}'.")
                return False
            if piece.color != self.currentPlayer.color:
                print("Cette pièce ne vous appartient pas.")
                return False

            # Déléguer la vérification à la pièce elle-même
            return piece.isValidMove(pos_dest, self.board)

        except (IndexError, ValueError):
            print("Format invalide. Exemple correct : Pe2 e4")
            return False

    # ----------------------------------------------------------
    #  Mise à jour du plateau
    # ----------------------------------------------------------

    def updateBoard(self, move: str):
        """
        Déplace la pièce sur le plateau après validation du coup.
        Supprime la pièce capturée si la case de destination était occupée.
        """
        col_dep  = move[1]
        row_dep  = int(move[2])
        col_dest = move[4]
        row_dest = int(move[5])

        pos_dep  = Position(col_dep,  row_dep)
        pos_dest = Position(col_dest, row_dest)

        # Récupérer la pièce
        piece = self.board.getPiece(pos_dep)

        # Supprimer l'ancienne case
        del self.board.pieces[str(pos_dep)]

        # Mettre à jour la position de la pièce
        piece.position = pos_dest

        # Si c'est un pion, marquer qu'il a bougé
        if str(piece) == 'P':
            piece.has_moved = True

        # Placer la pièce sur la nouvelle case (écrase la pièce capturée si besoin)
        self.board.pieces[str(pos_dest)] = piece

    # ----------------------------------------------------------
    #  Échec et mat (version simplifiée)
    # ----------------------------------------------------------

    def isCheckMate(self) -> bool:
        """
        Vérifie si le joueur courant est en échec et mat.
        Version simplifiée : retourne toujours False pour l'instant.
        La version complète sera implémentée en séance 5 en groupe.
        """
        return False

    # ----------------------------------------------------------
    #  Changer de joueur
    # ----------------------------------------------------------

    def switchPlayer(self):
        """
        Passe la main à l'autre joueur.
        Si currentPlayer est players[0], on passe à players[1], et vice versa.
        """
        if self.currentPlayer == self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]

    # ----------------------------------------------------------
    #  Sauvegarde / Restauration JSON
    # ----------------------------------------------------------

    def saveGame(self, filename: str = "sauvegarde.json"):
        """
        Sauvegarde l'état actuel de la partie dans un fichier JSON.
        """
        data = {
            "currentPlayer": self.currentPlayer.color,
            "pieces": {}
        }
        for pos_str, piece in self.board.pieces.items():
            data["pieces"][pos_str] = {
                "type":      str(piece),
                "color":     piece.color,
                "has_moved": getattr(piece, 'has_moved', False)
            }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Partie sauvegardée dans '{filename}'.")

    # ----------------------------------------------------------
    #  Boucle principale du jeu
    # ----------------------------------------------------------

    def play(self):
        """
        Démarre et gère la boucle principale de la partie.
        
        Pseudo-code selon le cahier des charges :
            Initialiser les joueurs
            Tant qu'il n'y a pas d'échec et mat :
                Afficher le plateau
                Tant que le mouvement n'est pas valide :
                    Demander un coup au joueur courant
                Mettre à jour le plateau
                Passer au joueur suivant
        """
        print("=== JEU D'ÉCHECS ===\n")
        self.initPlayers()

        while not self.isCheckMate():

            # Afficher le plateau
            self.displayBoard()
            print(f"Tour de : {self.currentPlayer.name} ({'Blanc' if self.currentPlayer.color == 0 else 'Noir'})")

            # Gérer le coup de l'IA
            if isinstance(self.currentPlayer, AIPlayer):
                move = self._getAIMove()
                if move == "":
                    print("L'IA n'a aucun coup valide. Fin de partie.")
                    break
                print(f"L'IA joue : {move}")
            else:
                # Demander un coup valide au joueur humain
                move = ""
                while not self.isValidMove(move):
                    move = self.currentPlayer.askMove()

            # Mettre à jour le plateau
            self.updateBoard(move)

            # Proposer de sauvegarder
            reponse = input("Sauvegarder la partie ? (o/n) : ").strip().lower()
            if reponse == 'o':
                self.saveGame()

            # Passer au joueur suivant
            self.switchPlayer()

        print("Fin de la partie !")

    # ----------------------------------------------------------
    #  Coup aléatoire pour l'IA
    # ----------------------------------------------------------

    def _getAIMove(self) -> str:
        """
        Génère un coup aléatoire valide pour l'IA.
        Parcourt toutes les pièces de l'IA et toutes les cases possibles
        jusqu'à en trouver un valide.
        """
        colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Récupérer toutes les pièces de l'IA
        pieces_ia = [
            p for p in self.board.pieces.values()
            if p.color == self.currentPlayer.color
        ]
        random.shuffle(pieces_ia)

        for piece in pieces_ia:
            # Essayer toutes les cases du plateau dans un ordre aléatoire
            cases = [Position(c, r) for c in colonnes for r in range(1, 9)]
            random.shuffle(cases)

            for dest in cases:
                if piece.isValidMove(dest, self.board):
                    move = f"{str(piece)}{piece.position.column}{piece.position.row} {dest.column}{dest.row}"
                    return move

        return ""  # Aucun coup valide trouvé


# ============================================================
#  Point d'entrée
# ============================================================

if __name__ == "__main__":
    partie = Chess()
    partie.play()
