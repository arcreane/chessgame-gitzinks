# end_screen.py
"""Affiche l'écran de fin de partie."""
import pygame
import sys


def show_end_screen(screen, width, height, winner_color: int):
    """
    Affiche un écran de victoire.
    :param winner_color: 0 = Blancs gagnent, 1 = Noirs gagnent
    """
    winner = "Blancs"      if winner_color == 0 else "Noirs"
    font_big = pygame.font.SysFont("arial", 64, bold=True)
    font_small = pygame.font.SysFont("arial", 32)

    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    txt_win = font_big.render(f"Les {winner} gagnent !", True, (255, 215, 0))
    txt_restart = font_small.render("R = Rejouer  |  Q = Quitter", True, (220, 220, 220))

    screen.blit(txt_win, (width // 2 - txt_win.get_width() // 2, height // 2 - 80))
    screen.blit(txt_restart, (width // 2 - txt_restart.get_width() // 2, height // 2 + 20))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return


if __name__ == "__main__":
    print("end_screen OK !")