# sound_manager.py
"""Gestion du son : musique de fond et effets sonores."""
import pygame
import os


class SoundManager:
    """Gère la musique de fond et les effets sonores."""

    def __init__(self):
        pygame.mixer.init()
        self._music_on = True
        self._sfx_on = True
        self._move_sound = None
        self._capture_sound = None
        self._load_sounds()

    def _load_sounds(self):
        """Charge les sons si les fichiers existent."""
        try:
            if os.path.exists("sounds/background.mp3"):
                pygame.mixer.music.load("sounds/background.mp3")
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)  # boucle infinie
        except Exception:
            pass
        try:
            if os.path.exists("sounds/move.wav"):
                self._move_sound = pygame.mixer.Sound("sounds/move.wav")
                self._move_sound.set_volume(0.6)
        except Exception:
            pass
        try:
            if os.path.exists("sounds/capture.wav"):
                self._capture_sound = pygame.mixer.Sound("sounds/capture.wav")
                self._capture_sound.set_volume(0.8)
        except Exception:
            pass

    def play_move(self):
        if self._sfx_on and self._move_sound:
            self._move_sound.play()

    def play_capture(self):
        if self._sfx_on and self._capture_sound:
            self._capture_sound.play()

    def toggle_music(self):
        self._music_on = not self._music_on
        if self._music_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def toggle_sfx(self):
        self._sfx_on = not self._sfx_on


if __name__ == "__main__":
    print("SoundManager OK !")