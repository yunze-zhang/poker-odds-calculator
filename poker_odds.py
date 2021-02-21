import random

class PokerSimulator:

    def __init__(self, player_cards, board_state):
        self.player_cards = player_cards
        self.board_state = board_state
        self.deck = self.generate_new_deck()
        self.remove_player_cards_from_deck()
        self.shuffle_deck()
        
    def generate_new_deck(self):
        deck = []
        for suit in 'hdsc':
            for rank in 'A23456789TJQK':
                deck.append(rank+suit)
        return deck
    
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
    
    
    
    


