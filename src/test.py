import unittest

from round import Round
from game import Game
from player import Player
from card import Card

class Test(unittest.TestCase):
    
    def test_methods(self):
        
        game = Game()
        game.initialize_cards()
        game.players = [Player("Mike"), Player("Tim"), Player("Jack"), Player("Nick")]
        
        # Points for Mike
        game.players[0].cards_deck = game.cards[0:26]
        # Points for Tim
        game.players[1].cards_deck = game.cards[26:37]
        # Points for Jack
        game.players[2].cards_deck = game.cards[37:49]
        # Points for Nick
        game.players[3].cards_deck = game.cards[49:52]
        
        rnd = Round(game.players[0])
        game.players[1].mokki = 2
        rnd.calculate_points(game.players)
        
        # Check that the points of each player is correct
        self.assertEqual(4, game.players[0].points, "Wrong amount of points!")
        self.assertEqual(3, game.players[1].points, "Wrong amount of points!")
        self.assertEqual(1, game.players[2].points, "Wrong amount of points!")
        self.assertEqual(3, game.players[3].points, "Wrong amount of points!")
        
        
        # Check that the validation algorithm works properly
        self.assertEqual(True, Round.check_validity(self, Card("Pata-7", 7, 7), [Card("Ruutu-3", 3, 3), Card("Hertta-4", 4, 4)]), "Validation failed")
        self.assertNotEqual(True, Round.check_validity(self, Card("Pata-8", 8, 8), [Card("Ruutu-3", 3, 3), Card("Hertta-4", 4, 4)]), "Validation failed")
        self.assertEqual(True, Round.check_validity(self, Card("Pata-2", 2, 15), [Card("Pata-8", 8, 8), Card("Hertta-7", 7, 7)]), "Validation failed")
        self.assertNotEqual(True, Round.check_validity(self, Card("Pata-10", 10, 10), [Card("Ruutu-5", 5, 5), Card("Hertta-5", 5, 5), Card("Pata-5", 5, 5)]), "Validation failed")
        
        # Check that the dealer changes correctly after each round
        game.set_dealer()
        self.assertEqual(game.players[0], game.dealer, "Wrong dealer!")
        game.set_dealer()
        self.assertEqual(game.players[1], game.dealer, "Wrong dealer!")
        game.set_dealer()
        game.set_dealer()
        game.set_dealer()
        self.assertEqual(game.players[0], game.dealer, "Wrong dealer!")
        
        
if __name__ == '__main__':
    unittest.main()