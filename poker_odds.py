import random
from enum import Enum

class StrengthIndex(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

class PokerSimulator:

    def __init__(self, player_cards, board_state):
        self.player_cards = player_cards
        self.board_state = board_state if board_state else []
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
        player_strengths = []
        for player_hand in self.player_cards:
            board = self.board_state + player_hand
            player_strengths.append(get_hand_strength(self, board))
    
    def get_hand_strength(self, board):
        """
        Returns in a tuple of (StrengthIndex, strength_index_value) hand strength
        """
        rank_counts = self.get_rank_counts(board)
        suit_counts = self.get_suit_counts(board)

        sf_rank = self.get_largest_straight_flush(board, suit_counts)
        if sf_rank:
            return StrengthIndex.STRAIGHT_FLUSH, sf_rank
        quads_rank = self.get_largest_duplicate_rank(rank_counts, 4)
        if quads_rank:
            kicker = self.get_largest_kicker_sum(board, [quads_rank], 1)
            return StrengthIndex.FOUR_OF_A_KIND, quads_rank, kicker
        fh_ranks = self.get_largest_full_house(rank_counts)
        if fh_ranks:
            return StrengthIndex.FULL_HOUSE, fh_ranks[0], fh_ranks[1]
        flush_suit = self.get_flush_suit(suit_counts)
        if flush_suit:
            return StrengthIndex.FLUSH, self.get_flush_rank_sum(board, flush_suit)
        straight_rank = self.get_largest_straight(board)
        if straight_rank:
            return StrengthIndex.STRAIGHT, straight_rank
        trips_rank = self.get_largest_duplicate_rank(rank_counts, 3)
        if trips_rank:
            kicker_sum = self.get_largest_kicker_sum(board, [trips_rank], 2)
            return StrengthIndex.THREE_OF_A_KIND, trips_rank, kicker_sum
        tp_ranks = self.get_largest_two_pair(rank_counts)
        if tp_ranks:
            kicker = self.get_largest_kicker_sum(board, [tp_ranks[0], tp_ranks[1]], 1)
            return StrengthIndex.TWO_PAIR, tp_ranks[0], tp_ranks[1], kicker
        pair_rank = self.get_largest_duplicate_rank(rank_counts, 2)
        if pair_rank:
            kicker_sum = self.get_largest_kicker_sum(board, [pair_rank], 3)
            return StrengthIndex.ONE_PAIR, pair_rank, kicker_sum
        else:
            kicker_sum = self.get_largest_kicker_sum(board, [], 5)
            return StrengthIndex.HIGH_CARD, kicker_sum
    
    def get_rank_counts(self, board):
        board_ranks = [card[0] for card in board]
        rank_counts = {rank : 0 for rank in 'AKQJT98765432'}
        for rank in board_ranks:
            rank_counts[rank] += 1
        return rank_counts
    
    def get_suit_counts(self, board):
        board_suits = [card[1] for card in board]
        suit_counts = {suit : 0 for suit in 'hdsc'}
        for suit in board_suits:
            suit_counts[suit] += 1
        return suit_counts
            
    def get_largest_duplicate_rank(self, rank_counts, num_duplicates):
        for rank in rank_counts:
            if rank_counts[rank] == num_duplicates:
                return self.rank_values[rank]
        return None
    
    def get_flush_suit(self, suit_counts):
        for suit in suit_counts:
            if suit_counts[suit] >= 5:
                return suit
        return None
    
    def get_flush_rank_sum(self, board, suit):
        """
        Returns the rank sum of a suit that was determined to be a flush
        """
        flush_ranks = sorted([card[0] for card in board if card[1] == suit])
        rank_sum = 0
        for i in range(1, 6):
            rank_sum += self.rank_values[flush_ranks[-i]]
        return rank_sum
    
    def get_largest_straight(self, board):
        """
        Returns largest rank in 5-card straight if straight is found
        If no straight, returns None
        """
        board_rank_values = sorted([self.rank_values[card[0]] for card in board])
        consecutive_count = 0
        current_head = board_rank_values[-1]
        possible_straight_ranks = []
        for i in reversed(range(len(board))):
            if board_rank_values[i] == board_rank_values[i-1] + 1:
                consecutive_count += 1
            elif board_rank_values[i] != board_rank_values[i-1]:
                consecutive_count = 0
                current_head = board_rank_values[i-1]
            if consecutive_count >= 4:
                return current_head

        # A to 5 straight
        for rank in 'A2345':
            if self.rank_values[rank] not in board_rank_values:
                return None
        return 5
    
    def get_largest_straight_flush(self, board, suit_counts):
        """
        Returns largest rank in 5-card straight flush if possible
        If no straight flush, returns None
        """
        suit = self.get_flush_suit(suit_counts)
        if suit:
            suit_ranks = [card[0] for card in board if card[1] == suit]
            straight_rank = self.get_largest_straight(suit_ranks)
            if straight_rank:
                return straight_rank
        return None
    
    def get_largest_full_house(self, rank_counts):
        """
        Returns weighted value of full house if possible
            (10*trips rank + pair rank)
        If no full house, returns None
        """
        trips_rank = self.get_largest_duplicate_rank(rank_counts, 3)
        if trips_rank:
            pair_rank = self.get_largest_duplicate_rank(rank_counts, 2)
            if pair_rank:
                return trips_rank, pair_rank
        return None
    
    def get_largest_kicker_sum(self, board, excluded_ranks, n):
        """
        Returns sum of n largest ranks not in excluded_ranks
        """
        board_rank_values = sorted([self.rank_values[card[0]] for card in board])
        rank_sum = 0
        rank_count = 0
        for i in range(1, len(board_rank_values)):
            if board_rank_values[-i] not in excluded_ranks:
                rank_sum += board_rank_values[-i]
                rank_count += 1
            if rank_count == n:
                return rank_sum
        raise Exception('Too many ranks were added in largest excluded rank sum')
    
    def get_largest_two_pair(self, rank_counts):
        pairs = []
        for rank in rank_counts:
            if rank_counts[rank] == 2:
                pairs.append(rank)
            if len(pairs) == 2:
                return self.rank_values[pairs[0]], self.rank_values[pairs[1]]
        return None
        