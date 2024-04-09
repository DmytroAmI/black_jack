import random


class Card:
    """Define a card"""
    RANKS = "2 3 4 5 6 7 8 9 10 J Q K A ".split()
    SUITS = "♥️ ♠️ ♦️ ♣️".split()

    def __init__(self, rank, suit):
        """Initialize the card attributes"""
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """Return a string representation of the card"""
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return self.__str__()


class Deck:
    """Define a deck of cards"""
    def __init__(self, cards):
        """Initialize the attributes deck of cards"""
        self.cards = cards
        self.index = 0

    @classmethod
    def create_deck(cls, shuffle=False):
        """Create a deck of 52 cards and return"""
        cards = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]
        if shuffle:
            random.shuffle(cards)
        return cls(cards)

    def __len__(self):
        """Return the number of cards in the deck"""
        return len(self.cards)

    def __iter__(self):
        """Return an iterator"""
        return iter(self.cards)

    def __next__(self):
        """Return the next card from the deck"""
        if self.index >= len(self.cards):
            raise StopIteration

        result = self.cards[self.index]
        self.index += 1
        return result

    def __str__(self):
        """Return a string representation of the deck"""
        return str(self.cards)


class Player:
    pass


class Game:
    pass
