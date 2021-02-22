import random
from enum import Enum

class Hand(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRIGHT_FLUSH = 8

class PokerSimulator:

    def __init__(self, player_cards, board_state):
        self.player_cards = player_cards
        if not board_state:
            self.board_state = []
        else:
            self.board_state = board_state
        self.rank_values = self.create_rank_dictionary()
        self.deck = self.generate_new_deck()
        self.remove_player_cards_from_deck()
        
    def generate_new_deck(self):
        deck = []
        for suit in 'hdsc':
            for rank in 'A23456789TJQK':
                deck.append(rank+suit)
        return deck
    
    def create_rank_dictionary(self):
        value = 2
        rank_values = {}
        for rank in '23456789TJQKA':
            rank_values[rank] = value
            value += 1
        return rank_values
    
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def remove_player_cards_from_deck(self):
        if self.player_cards:
            for hand in self.player_cards:
                for card in hand:
                    if card in self.deck:
                        self.deck.remove(card)
                    else:
                        raise Exception("Invalid Player Card")
    
    def deal_card(self):
        return self.deck.pop()

    def simulate_full_board(self):
        self.shuffle_deck()
        while len(self.board_state) < 5:
            next_card = self.deal_card()
            self.board_state.append(next_card)
    
    def determine_winner(self):
        for player_hand in self.player_cards:
            board = self.board_state + player_hand
            board_ranks = [card[0] for card in board]
            board_suits = [card[1] for card in board]
            hand_strength = []
            
    def check_high_card(self):
        pass

    def check_one_pair(self):
        pass