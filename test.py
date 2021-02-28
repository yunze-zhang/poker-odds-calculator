import unittest
from poker_odds import PokerSimulator
from poker_odds import StrengthIndex

class TestPokerSimulator(unittest.TestCase):

    def test_player_hands(self):
        simulator = PokerSimulator(None, None)
        self.assertEqual(simulator.player_hands, None)
        simulator = PokerSimulator([['Ah', 'Kd'], ['Qh','Qd']], None)
        self.assertEqual(simulator.player_hands, [['Ah', 'Kd'], ['Qh', 'Qd']])
    
    def test_deck_generation(self):
        simulator = PokerSimulator(None, None)
        deck = simulator.generate_new_deck()
        self.assertEqual(len(deck), 52)
    
    def test_player_card_removal(self):
        simulator = PokerSimulator([['Ah','Kd'], ['Qh', 'Qd']], None)
        deck = simulator.generate_new_deck()
        simulator.remove_player_cards(deck)
        self.assertEqual(len(deck), 48)
    
    def test_board_state(self):
        simulator = PokerSimulator(None, ['Ah', 'Ad', 'Ah'])
        self.assertEqual(len(simulator.board_state), 3)
    
    def test_simulate_full_board(self):
        simulator = PokerSimulator([['Ah','Kd'], ['Qh', 'Qd']], None)
        deck = simulator.generate_new_deck()
        simulator.remove_player_cards(deck)
        simulated_board_state = simulator.deal_full_board(deck)
        self.assertEqual(len(simulated_board_state), 5)
    
    def test_rank_values(self):
        simulator = PokerSimulator([['Ah','Kd'], ['Qh', 'Qd']], None)
        self.assertEqual(simulator.rank_values['A'], 14)

    def test_high_card(self):
        simulator = PokerSimulator([['Ah','Kd']], ['2d', '3h', '7s', '9c', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.HIGH_CARD.value, 53))
    
    def test_one_pair(self):
        simulator = PokerSimulator([['Ah','Kd']], ['Ad', '3h', '7s', '9c', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.ONE_PAIR.value, 14, 32))
    
    def test_two_pair(self):
        simulator = PokerSimulator([['Ah','Kd']], ['Ad', 'Kh', '7s', '9c', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.TWO_PAIR.value, 14, 13, 10))
    
    def test_two_pair_multiple(self):
        simulator = PokerSimulator([['Th','9d']], ['Ad', 'Kh', 'As', 'Kc', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.TWO_PAIR.value, 14, 13, 10))
    
    def test_trips(self):
        simulator = PokerSimulator([['Th','9d']], ['Ad', 'Kh', 'Qs', 'Tc', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.THREE_OF_A_KIND.value, 10, 27))
    
    def test_straight(self):
        simulator = PokerSimulator([['Th','9d']], ['2d', 'Kh', 'Qs', 'Tc', 'Jd'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        board_rank_values = sorted([simulator.rank_values[card[0]] for card in board])
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT.value, 13))
    
    def test_straight_multiple(self):
        simulator = PokerSimulator([['Th','9d']], ['Ad', 'Kh', 'Qs', 'Tc', 'Jd'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT.value, 14))
    
    def test_straight_ace_to_5(self):
        simulator = PokerSimulator([['Ah','2d']], ['3d', '4h', '5s', 'Tc', 'Jd'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT.value, 5))
    
    def test_flush(self):
        simulator = PokerSimulator([['Ah','2h']], ['3d', '4h', '5s', 'Th', 'Jh'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.FLUSH.value, 15.4))
    
    def test_flush_multiple(self):
        simulator = PokerSimulator([['Ah','2h']], ['Qh', '4h', '5s', 'Th', 'Jh'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.FLUSH.value, 17.5))
    
    def test_full_house(self):
        simulator = PokerSimulator([['Ad','2h']], ['Ah', '2d', 'As', 'Th', 'Jh'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.FULL_HOUSE.value, 14, 2))
    
    def test_full_house_multiple(self):
        simulator = PokerSimulator([['Ad','2h']], ['Ah', '2d', 'As', 'Th', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.FULL_HOUSE.value, 14, 10))
    
    def test_quads(self):
        simulator = PokerSimulator([['Ad','2h']], ['Ah', '2d', 'As', 'Ac', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.FOUR_OF_A_KIND.value, 14, 10))
    
    def test_straight_flush(self):
        simulator = PokerSimulator([['Ad','Kd']], ['Ah', '2d', 'Qd', 'Jd', 'Td'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT_FLUSH.value, 14))
    
    def test_straight_flush_a_to_5(self):
        simulator = PokerSimulator([['Ad','Kd']], ['Ah', '2d', '3d', '5d', '4d'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT_FLUSH.value, 5))
    
    def test_straight_flush_multiple(self):
        simulator = PokerSimulator([['8d','9d']], ['Td', '2d', 'Jd', 'Qd', 'Kd'])
        board = simulator.board_state + simulator.player_hands[0]
        hand_strength = simulator.get_hand_strength(board)
        self.assertEqual(hand_strength, (StrengthIndex.STRAIGHT_FLUSH.value, 13))

    def test_simulate_winner(self):
        simulator = PokerSimulator([['8d','9d'], ['Ah', 'Kd']], None)
        winner = simulator.simulate_winner()
    
    def test_get_winner_odds_pre_flop(self):
        simulator = PokerSimulator([['8d','9d'], ['Ah', 'Kd']], None)
        print(simulator.get_winner_odds(10000))
    
    def test_get_winner_odds_post_flop(self):
        simulator = PokerSimulator([['8d','9d'], ['Ah', 'Kd']], ['6d', '7d', 'As'])
        print(simulator.get_winner_odds(10000))

    def test_get_winner_odds_full_board(self):
        simulator = PokerSimulator([['8d','9d'], ['Ah', 'Kd']], ['6d', '7d', 'As', 'Jd', '4d'])
        print(simulator.get_winner_odds(10000))

if __name__ == '__main__':
    unittest.main()
