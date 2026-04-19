from piece import Piece
from position import Position


class Pawn(Piece):
    """
    Représente un Pion sur l'échiquier.
    
    Règles de déplacement du Pion :
    - Avance d'une case vers l'avant (jamais en arrière)
    - Peut avancer de 2 cases si c'est son premier mouvement
    - Capture en diagonale (1 case en avant à gauche ou droite)
    - Blanc (color=0) avance vers les lignes croissantes (row +1)
    - Noir  (color=1) avance vers les lignes décroissantes (row -1)
    """

    def __init__(self, position: Position, color: int):
        super().__init__(position, color)
        # On mémorise si la pièce a déjà bougé (pour le coup à 2 cases)
        self.has_moved = False

    def isValidMove(self, newPosition: Position, board) -> bool:
        """
        Vérifie si le déplacement vers newPosition est valide pour ce pion.
        
        Paramètres :
            newPosition : la case de destination
            board       : l'état actuel du plateau (instance de Board)
        
        Retourne True si le mouvement est valide, False sinon.
        """

        col_actuelle  = self.position.column  # ex: 'e'
        row_actuelle  = self.position.row     # ex: 2
        col_dest      = newPosition.column    # ex: 'e'
        row_dest      = newPosition.row       # ex: 3

        # Direction selon la couleur : blanc monte (+1), noir descend (-1)
        direction = 1 if self.color == 0 else -1

        # --- Différences de colonne et de ligne ---
        diff_col = ord(col_dest) - ord(col_actuelle)  # 0 si même colonne
        diff_row = row_dest - row_actuelle             # positif = vers l'avant (blanc)

        # On ne peut jamais rester sur place
        if diff_col == 0 and diff_row == 0:
            return False

        # ---- CAS 1 : Avancer d'une case tout droit ----
        if diff_col == 0 and diff_row == direction:
            # La case de destination doit être VIDE
            if board.getPiece(newPosition) is None:
                return True

        # ---- CAS 2 : Avancer de deux cases (premier coup uniquement) ----
        if diff_col == 0 and diff_row == 2 * direction and not self.has_moved:
            # Les deux cases devant doivent être libres
            case_intermediaire = Position(col_actuelle, row_actuelle + direction)
            if (board.getPiece(case_intermediaire) is None and
                    board.getPiece(newPosition) is None):
                return True

        # ---- CAS 3 : Capture en diagonale ----
        if abs(diff_col) == 1 and diff_row == direction:
            piece_en_dest = board.getPiece(newPosition)
            # Il doit y avoir une pièce ENNEMIE sur la case de destination
            if piece_en_dest is not None and piece_en_dest.color != self.color:
                return True

        # Tout autre mouvement est invalide
        return False

    def __str__(self) -> str:
        # Identifiant du pion selon le cahier des charges
        return "P"
