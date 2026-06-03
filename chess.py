import pygame
import sys
import json
import os
from board import Board
from position import Position
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from knight import Knight
from queen import Queen
from king import King


class GameGUI:
    def __init__(self):
        pygame.init()
        self.largeur = 640
        self.hauteur = 640
        self.taille_case = self.largeur // 8
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Jeu d'Echecs")

        self.board = Board()
        self.pos_selectionnee = None
        self.tour_joueur = 0

        self.images = {}
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
        couleurs = {0: 'w', 1: 'b'}

        for p in pieces:
            for c_val, c_lettre in couleurs.items():
                nom_fichier = os.path.join("image", f"{p}{c_lettre}.png")
                try:
                    img = pygame.image.load(nom_fichier)
                    img = pygame.transform.smoothscale(img, (self.taille_case, self.taille_case))
                    self.images[(p, c_val)] = img
                except FileNotFoundError:
                    pass

    def dessiner_plateau(self):
        couleurs = [(238, 238, 210), (118, 150, 86)]
        for ligne in range(8):
            for col in range(8):
                couleur = couleurs[(ligne + col) % 2]
                rect = pygame.Rect(col * self.taille_case, ligne * self.taille_case, self.taille_case, self.taille_case)
                pygame.draw.rect(self.ecran, couleur, rect)

                if self.pos_selectionnee:
                    scol = "abcdefgh".index(self.pos_selectionnee.column)
                    sligne = 8 - self.pos_selectionnee.row
                    if scol == col and sligne == ligne:
                        pygame.draw.rect(self.ecran, (255, 255, 50), rect, 5)

    def dessiner_pieces(self):
        cols = "abcdefgh"
        for ligne in range(8):
            for col in range(8):
                v_col = cols[col]
                v_ligne = 8 - ligne
                piece = self.board.getPiece(Position(v_col, v_ligne))

                if piece:
                    cle = (str(piece), piece.color)
                    if cle in self.images:
                        self.ecran.blit(self.images[cle], (col * self.taille_case, ligne * self.taille_case))

    def sauvegarder(self, fichier="sauvegarde.json"):
        data = {
            "currentPlayer": self.tour_joueur,
            "pieces": {}
        }
        for pos_str, piece in self.board.grid.items():
            data["pieces"][pos_str] = {
                "type": str(piece),
                "color": piece.color,
                "has_moved": getattr(piece, 'has_moved', False)
            }
        with open(fichier, 'w') as f:
            json.dump(data, f, indent=2)

    def charger(self, fichier="sauvegarde.json"):
        classes_pieces = {'P': Pawn, 'R': Rook, 'B': Bishop, 'N': Knight, 'Q': Queen, 'K': King}
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
            self.board.grid = {}
            for pos_str, info in data["pieces"].items():
                col = pos_str[0]
                row = int(pos_str[1])
                pos = Position(col, row)
                cls = classes_pieces.get(info["type"])
                if cls:
                    piece = cls(info["color"], pos)
                    if info["type"] == 'P':
                        piece.has_moved = info.get("has_moved", False)
                    self.board.grid[pos_str] = piece
            self.tour_joueur = data["currentPlayer"]
            self.pos_selectionnee = None
        except Exception:
            pass

    def jouer(self):
        cols = "abcdefgh"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.sauvegarder()
                    elif event.key == pygame.K_l:
                        self.charger()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // self.taille_case
                    ligne = y // self.taille_case
                    pos_clic = Position(cols[col], 8 - ligne)

                    if self.pos_selectionnee:
                        piece = self.board.getPiece(self.pos_selectionnee)
                        if piece and piece.isValidMove(pos_clic, self.board):
                            self.board.movePiece(self.pos_selectionnee, pos_clic)
                            if str(piece) == 'P':
                                piece.has_moved = True
                            self.tour_joueur = 1 - self.tour_joueur
                        self.pos_selectionnee = None
                    else:
                        piece = self.board.getPiece(pos_clic)
                        if piece and piece.color == self.tour_joueur:
                            self.pos_selectionnee = pos_clic

            self.dessiner_plateau()
            self.dessiner_pieces()
            pygame.display.flip()


if __name__ == "__main__":
    jeu = GameGUI()
    jeu.jouer()