import unittest
from poker_odds import PokerSimulator

class TestPokerSimulator(unittest.TestCase):

    def test_player_cards(self):
        simulator = PokerSimulator(None, None)
        self.assertEqual(simulator.player_cards, None)
        simulator = PokerSimulator([['Ah', 'Kd'], ['Qh','Qd']], None)
        self.assertEqual(simulator.player_cards, [['Ah', 'Kd'], ['Qh', 'Qd']])
    
    def test_deck_generation(self):
        simulator = PokerSimulator(None, None)
        self.assertEqual(len(simulator.deck), 52)
    
    def test_player_card_removal(self):
        simulator = PokerSimulator([['Ah','Kd'], ['Qh', 'Qd']], None)
        self.assertEqual(len(simulator.deck), 48)
    
    def test_board_state(self):
        simulator = PokerSimulator(None, ['Ah', 'Ad', 'Ah'])
        self.assertEqual(len(simulator.board_state), 3)
    
    def test_simulate_full_board(self):
        simulator = PokerSimulator([['Ah','Kd'], ['Qh', 'Qd']], None)
        simulator.simulate_full_board()
        self.assertEqual(len(simulator.board_state), 5)

if __name__ == '__main__':
    unittest.main()
