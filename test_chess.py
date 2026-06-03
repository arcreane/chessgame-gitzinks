# test_chess.py
import unittest
from position import Position
from rook import Rook
from pawn import Pawn
from board import Board


class TestPosition(unittest.TestCase):
    """Tests unitaires pour Position."""

    def test_position_str(self):
        """Position doit retourner 'e4' pour column='e', row=4."""
        p = Position("e", 4)
        self.assertEqual(str(p), "e4")

    def test_position_egalite(self):
        """Deux positions identiques doivent être égales."""
        self.assertEqual(Position("a", 1), Position("a", 1))

    def test_position_inegalite(self):
        """Deux positions différentes ne doivent pas être égales."""
        self.assertNotEqual(Position("a", 1), Position("b", 2))


class TestRook(unittest.TestCase):
    """Tests unitaires pour la Tour."""

    def setUp(self):
        """Plateau vide avec une tour blanche en a1."""
        self.board = Board()
        self.board.pieces = {}
        self.rook = Rook(0, Position('a', 1))
        self.board.pieces['a1'] = self.rook

    def test_rook_str(self):
        """La tour doit retourner 'R'."""
        self.assertEqual(str(self.rook), 'R')

    def test_deplacement_colonne_valide(self):
        """La tour peut avancer sur la même colonne si chemin libre."""
        self.assertTrue(self.rook.isValidMove(Position('a', 5), self.board))

    def test_deplacement_ligne_valide(self):
        """La tour peut avancer sur la même ligne si chemin libre."""
        self.assertTrue(self.rook.isValidMove(Position('h', 1), self.board))

    def test_mouvement_diagonal_invalide(self):
        """La tour ne peut pas se déplacer en diagonale."""
        self.assertFalse(self.rook.isValidMove(Position('c', 3), self.board))

    def test_bloque_par_piece(self):
        """La tour ne peut pas sauter par-dessus une pièce."""
        self.board.pieces['a3'] = Pawn(0, Position('a', 3))
        self.assertFalse(self.rook.isValidMove(Position('a', 5), self.board))

    def test_capture_ennemi(self):
        """La tour peut capturer une pièce ennemie."""
        self.board.pieces['a5'] = Pawn(1, Position('a', 5))
        self.assertTrue(self.rook.isValidMove(Position('a', 5), self.board))

    def test_ne_capture_pas_allie(self):
        """La tour ne peut pas capturer un allié."""
        self.board.pieces['a5'] = Pawn(0, Position('a', 5))
        self.assertFalse(self.rook.isValidMove(Position('a', 5), self.board))


if __name__ == '__main__':
    unittest.main(verbosity=2)