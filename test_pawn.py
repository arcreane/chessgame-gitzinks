import unittest
from position import Position
from pawn import Pawn
from board import Board


class TestPawn(unittest.TestCase):
    """
    Tests unitaires pour la classe Pawn.
    On teste chaque règle de déplacement du pion séparément.
    """

    def setUp(self):
        """
        Appelée avant chaque test.
        Crée un plateau vide et des pions pour les tests.
        """
        self.board = Board()

        # Pion blanc en e2 (position de départ classique)
        self.pion_blanc = Pawn(Position("e", 2), 0)
        self.board.pieces["e2"] = self.pion_blanc

        # Pion noir en e7 (position de départ classique)
        self.pion_noir = Pawn(Position("e", 7), 1)
        self.board.pieces["e7"] = self.pion_noir

    # ----------------------------------------------------------
    # Tests : avancer d'une case
    # ----------------------------------------------------------

    def test_blanc_avance_une_case(self):
        """Le pion blanc doit pouvoir avancer d'une case vers l'avant."""
        dest = Position("e", 3)
        self.assertTrue(self.pion_blanc.isValidMove(dest, self.board))

    def test_noir_avance_une_case(self):
        """Le pion noir doit pouvoir avancer d'une case vers l'avant (vers le bas)."""
        dest = Position("e", 6)
        self.assertTrue(self.pion_noir.isValidMove(dest, self.board))

    def test_blanc_ne_recule_pas(self):
        """Le pion blanc NE PEUT PAS reculer."""
        dest = Position("e", 1)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    def test_noir_ne_recule_pas(self):
        """Le pion noir NE PEUT PAS reculer."""
        dest = Position("e", 8)
        self.assertFalse(self.pion_noir.isValidMove(dest, self.board))

    # ----------------------------------------------------------
    # Tests : avancer de deux cases (premier coup)
    # ----------------------------------------------------------

    def test_blanc_avance_deux_cases_premier_coup(self):
        """Le pion blanc peut avancer de 2 cases au premier coup."""
        dest = Position("e", 4)
        self.assertTrue(self.pion_blanc.isValidMove(dest, self.board))

    def test_noir_avance_deux_cases_premier_coup(self):
        """Le pion noir peut avancer de 2 cases au premier coup."""
        dest = Position("e", 5)
        self.assertTrue(self.pion_noir.isValidMove(dest, self.board))

    def test_blanc_ne_peut_pas_deux_cases_apres_avoir_bouge(self):
        """Le pion blanc NE PEUT PAS avancer de 2 cases s'il a déjà bougé."""
        self.pion_blanc.has_moved = True
        dest = Position("e", 4)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    def test_bloque_si_case_intermediaire_occupee(self):
        """Le pion blanc ne peut pas sauter par-dessus une pièce."""
        # On place une pièce en e3 (case intermédiaire)
        obstacle = Pawn(Position("e", 3), 1)
        self.board.pieces["e3"] = obstacle
        dest = Position("e", 4)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    # ----------------------------------------------------------
    # Tests : avancer tout droit bloqué
    # ----------------------------------------------------------

    def test_blanc_bloque_si_case_devant_occupee(self):
        """Le pion blanc NE PEUT PAS avancer si la case devant est occupée."""
        obstacle = Pawn(Position("e", 3), 1)
        self.board.pieces["e3"] = obstacle
        dest = Position("e", 3)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    # ----------------------------------------------------------
    # Tests : capture en diagonale
    # ----------------------------------------------------------

    def test_blanc_capture_diagonale(self):
        """Le pion blanc peut capturer une pièce ennemie en diagonale."""
        ennemi = Pawn(Position("d", 3), 1)  # pion noir en d3
        self.board.pieces["d3"] = ennemi
        dest = Position("d", 3)
        self.assertTrue(self.pion_blanc.isValidMove(dest, self.board))

    def test_blanc_ne_capture_pas_allie(self):
        """Le pion blanc NE PEUT PAS capturer un allié en diagonale."""
        allie = Pawn(Position("d", 3), 0)  # pion blanc en d3
        self.board.pieces["d3"] = allie
        dest = Position("d", 3)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    def test_blanc_ne_capture_pas_case_vide_diagonale(self):
        """Le pion blanc NE PEUT PAS aller en diagonale si la case est vide."""
        dest = Position("d", 3)  # case vide
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    def test_noir_capture_diagonale(self):
        """Le pion noir peut capturer une pièce ennemie en diagonale."""
        ennemi = Pawn(Position("f", 6), 0)  # pion blanc en f6
        self.board.pieces["f6"] = ennemi
        dest = Position("f", 6)
        self.assertTrue(self.pion_noir.isValidMove(dest, self.board))

    # ----------------------------------------------------------
    # Tests : mouvements complètement invalides
    # ----------------------------------------------------------

    def test_mouvement_lateral_invalide(self):
        """Le pion ne peut pas se déplacer latéralement."""
        dest = Position("f", 2)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))

    def test_mouvement_trois_cases_invalide(self):
        """Le pion ne peut pas avancer de 3 cases."""
        dest = Position("e", 5)
        self.assertFalse(self.pion_blanc.isValidMove(dest, self.board))


if __name__ == "__main__":
    # Lance tous les tests et affiche le résultat
    unittest.main(verbosity=2)
