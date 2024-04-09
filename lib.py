import random


class Card:
    """Define a card"""
    RANKS = "2 3 4 5 6 7 8 9 10 J Q K".split()
    SUITS = "♥️ ♠️ ♦️ ♣️".split()

    def __init__(self, rank, suit):
        """Initialize the card attributes"""
        self.rank = rank
        self.suit = suit

    def get_card(self):
        """Return a card as a string"""
        return self.rank + self.suit

    @staticmethod
    def convert_card_to_points(card):
        """Convert a card into a points"""
        if card.get_card()[0] in "JQK" or "10" in card.get_card():
            return 10

        return int(card.get_card()[0])

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

    def get_cards(self):
        """Return deck of cards"""
        return self.cards

    def get_card_from_deck(self):
        """Take a card from the deck"""
        current_card = self.cards.pop()
        self.cards.insert(0, current_card)
        return current_card

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


class Croupier:
    """Define a croupier"""
    def __init__(self, name="Croupier"):
        """Initialize the player attributes"""
        self.name = name
        self.hand = []
        self.points = 0

    def add_card_to_hand(self, card):
        """Add a card to the hand and count points"""
        self.hand.append(card)
        self.points += Card.convert_card_to_points(card)

    def clear(self):
        self.points = 0
        self.hand = []

    def __str__(self):
        """Return a string representation of the player"""
        return f"Croupier {self.name}"


class Player(Croupier):
    """Define a player"""
    def __init__(self, name, balance):
        """Initialize the player attributes"""
        super().__init__(name)
        self.balance = balance

    def __str__(self):
        """Return a string representation of the player"""
        return f"Player - {self.name}, balance: {self.balance}"


class Game:
    """Define the game process"""
    def __init__(self, croupier, player, deck):
        """Initialize the game attributes"""
        self.croupier = croupier
        self.player = player
        self.deck = deck

    def round(self):
        """Describe the round of the game"""
        while True:
            bid = int(input("Take your bid: "))
            if bid > self.player.balance:
                print("Your bid was greater than your balance! Take bid again!")
            else:
                break

        self.player.add_card_to_hand(self.deck.get_card_from_deck())
        self.croupier.add_card_to_hand(self.deck.get_card_from_deck())

        self.player.add_card_to_hand(self.deck.get_card_from_deck())
        self.croupier.add_card_to_hand(self.deck.get_card_from_deck())

        while True:
            print("Your cards:\n\t", self.player.hand)
            choice = input("More cards? (y/n): ")
            if choice == "n":
                if self.player.points > self.croupier.points:
                    print("You win!")
                    print(f"Your points: {self.player.points}, Croupier: {self.croupier.points}")
                    self.player.balance += bid
                    self.player.clear()
                    self.croupier.clear()
                elif self.player.points < self.croupier.points:
                    print("You lose!")
                    print(f"Your points: {self.player.points}, Croupier: {self.croupier.points}")
                    self.player.balance -= bid
                    self.player.clear()
                    self.croupier.clear()
                else:
                    print("Draw! Your won!")
                    print(f"Your points: {self.player.points}, Croupier: {self.croupier.points}")
                    self.player.balance += bid
                    self.player.clear()
                    self.croupier.clear()
                break

            self.player.add_card_to_hand(self.deck.get_card_from_deck())
            if not self.croupier.points >= 17:
                self.croupier.add_card_to_hand(self.deck.get_card_from_deck())

            if self.player.points > 21:
                print("You lose!\n", self.player.hand)
                print("Your points:", self.player.points)
                self.player.balance -= bid
                self.player.clear()
                self.croupier.clear()
                break
            elif self.croupier.points > 21:
                print("You win!")
                print("Croupier points:", self.croupier.points)
                self.player.balance += bid
                self.player.clear()
                self.croupier.clear()
                break

    def play(self):
        """Play the game"""
        while self.player.balance:
            choice = input("Continue? (y/n): ")
            if choice == "n":
                break

            Game.round(self)

        print("Your final score is", self.player.balance)
