import unittest
from position import Position
from pawn import Pawn
from board import Board


class TestPawn(unittest.TestCase):

    def setUp(self):
        """Crée un plateau vide et un pion blanc en e2 avant chaque test."""
        self.board = Board()
        self.pion_blanc = self.board.getPiece(Position('e', 2))
        self.pion_noir = self.board.getPiece(Position('e', 7))

    def test_avance_une_case(self):
        """Le pion blanc avance d'une case."""
        self.assertTrue(self.pion_blanc.isValidMove(Position('e', 3), self.board))

    def test_avance_deux_cases_depart(self):
        """Le pion blanc peut avancer de 2 cases au départ."""
        self.assertTrue(self.pion_blanc.isValidMove(Position('e', 4), self.board))

    def test_ne_recule_pas(self):
        """Le pion blanc ne peut pas reculer."""
        self.assertFalse(self.pion_blanc.isValidMove(Position('e', 1), self.board))

    def test_bloque_si_piece_devant(self):
        """Le pion blanc ne peut pas avancer si une pièce bloque."""
        from pawn import Pawn
        self.board.grid['e3'] = Pawn(1, Position('e', 3))
        self.assertFalse(self.pion_blanc.isValidMove(Position('e', 3), self.board))

    def test_capture_diagonale(self):
        """Le pion blanc capture un ennemi en diagonale."""
        self.board.grid['d3'] = Pawn(1, Position('d', 3))
        self.assertTrue(self.pion_blanc.isValidMove(Position('d', 3), self.board))

    def test_pas_capture_allie(self):
        """Le pion blanc ne peut pas capturer un allié."""
        self.board.grid['d3'] = Pawn(0, Position('d', 3))
        self.assertFalse(self.pion_blanc.isValidMove(Position('d', 3), self.board))


if __name__ == "__main__":
    unittest.main(verbosity=2)