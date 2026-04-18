import unittest
from position import Position
from piece import Rook

class TestChess(unittest.TestCase):

    def test_position_str(self):
        p = Position("a", 1)
        self.assertEqual(str(p), "a1")

    def test_rook_str(self):
        p = Position("a", 1)
        r = Rook(p, 0)
        self.assertEqual(str(r), "R")

if name == 'main':
    unittest.main()
