from unittest import *
from game.HitoriGame import HitoriGame

class TestHitoriGame(TestCase):
    
    def setUp(self):
        
        self._w = 5
        self._h = 5
        
        self._game = HitoriGame((self._w, self._h), "./tables/5-easy.csv")
    
    
    def test_automateH(self):
        
        self._game.play(4, 4, "")    
        self._game.automateH()
        
        
        self.assertEqual(self._game._annots[4 + 3 * self._w], 2)
        self.assertEqual(self._game._annots[3 + 4 * self._w], 2)
        
        
        self._game.automateH()
        
        
        self.assertEqual(self._game._annots[3 + 3 * self._w], 1)
        self.assertEqual(self._game._annots[4 + 0 * self._w], 1)
        self.assertEqual(self._game._annots[0 + 4 * self._w], 1)
        
        
        
    def test_annotations(self):
        
        self._game.play(0, 0, "")
        self._game.play(0, 0, "flag")
        
        self.assertEqual(self._game.read(0, 0), "4#")
        self.assertEqual(self._game.read(1, 0), "5!")
        
                