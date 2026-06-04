# move_hints.py
"""Calcule et affiche les cases accessibles pour une pièce sélectionnée."""
import pygame


def draw_hints(screen, piece, board, taille_case):
    """Dessine les cases valides directement sur l'écran."""
    from position import Position
    cols = 'abcdefgh'
    for r in range(1, 9):
        for c in cols:
            dest = Position(c, r)
            try:
                if piece.isValidMove(dest, board):
                    mc = cols.index(c)
                    ml = 8 - r
                    hint_surf = pygame.Surface((taille_case, taille_case), pygame.SRCALPHA)
                    hint_surf.fill((50, 200, 50, 110))
                    screen.blit(hint_surf, (mc * taille_case, ml * taille_case))
            except Exception:
                pass


if __name__ == "__main__":
    print("move_hints OK !")