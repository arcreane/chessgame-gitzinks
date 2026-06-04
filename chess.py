import pygame
import sys
import json
import os
import random
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
        self.joue_contre_ia = False

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

    def choisir_mode_jeu(self):
        menu_actif = True
        font_titre = pygame.font.SysFont("arial", 60, bold=True)
        font_bouton = pygame.font.SysFont("arial", 35, bold=True)

        titre = font_titre.render("JEU D'ÉCHECS", True, (255, 255, 255))
        bouton_ia = font_bouton.render("1 Joueur (vs IA)", True, (40, 40, 40))
        bouton_humain = font_bouton.render("2 Joueurs (Local)", True, (40, 40, 40))

        rect_ia = pygame.Rect(self.largeur // 2 - 175, 250, 350, 70)
        rect_humain = pygame.Rect(self.largeur // 2 - 175, 360, 350, 70)

        while menu_actif:
            self.ecran.fill((60, 65, 70))

            self.ecran.blit(titre, (self.largeur // 2 - titre.get_width() // 2, 80))

            pygame.draw.rect(self.ecran, (200, 200, 200), rect_ia, border_radius=10)
            pygame.draw.rect(self.ecran, (200, 200, 200), rect_humain, border_radius=10)

            self.ecran.blit(bouton_ia, (rect_ia.centerx - bouton_ia.get_width() // 2,
                                        rect_ia.centery - bouton_ia.get_height() // 2))
            self.ecran.blit(bouton_humain, (rect_humain.centerx - bouton_humain.get_width() // 2,
                                            rect_humain.centery - bouton_humain.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_ia.collidepoint(event.pos):
                        self.joue_contre_ia = True
                        menu_actif = False
                    elif rect_humain.collidepoint(event.pos):
                        self.joue_contre_ia = False
                        menu_actif = False

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

    def faire_coup_ia(self):
        pieces_ia = [p for p in self.board.grid.values() if p.color == 1]
        coups_possibles = []
        cols = "abcdefgh"

        for piece in pieces_ia:
            for ligne in range(1, 9):
                for col in cols:
                    dest = Position(col, ligne)
                    if piece.isValidMove(dest, self.board):
                        coups_possibles.append((piece.position, dest, piece))

        if coups_possibles:
            depart, arrivee, piece = random.choice(coups_possibles)
            self.board.movePiece(depart, arrivee)
            if str(piece) == 'P':
                piece.has_moved = True
            self.tour_joueur = 0

    def jouer(self):
        cols = "abcdefgh"
        while True:
            if self.joue_contre_ia and self.tour_joueur == 1:
                pygame.time.delay(400)
                self.faire_coup_ia()

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
                    if not self.joue_contre_ia or self.tour_joueur == 0:
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
    jeu.choisir_mode_jeu()
    jeu.jouer()