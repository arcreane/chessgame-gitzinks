# timer.py
"""Chronomètre par joueur pour le jeu d'échecs."""
import time


class ChessTimer:
    """Gère le temps de jeu pour chaque joueur."""

    def __init__(self):
        self.times = [0.0, 0.0]
        self._start = None
        self._current_player = 0

    def start(self, player: int):
        self._current_player = player
        self._start = time.time()

    def switch(self, new_player: int):
        if self._start is not None:
            self.times[self._current_player] += time.time() - self._start
        self.start(new_player)

    def elapsed(self, player: int) -> str:
        total = self.times[player]
        if self._current_player == player and self._start is not None:
            total += time.time() - self._start
        m, s = divmod(int(total), 60)
        return f"{m:02d}:{s:02d}"


if __name__ == "__main__":
    t = ChessTimer()
    t.start(0)
    time.sleep(1)
    print(f"Blanc : {t.elapsed(0)}")
    print("ChessTimer OK !")