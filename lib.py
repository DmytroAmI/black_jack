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

    def deal_card(self):
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


class Dealer:
    """Define a croupier"""

    def __init__(self, name="Dealer"):
        """Initialize the player attributes"""
        self.name = name
        self.hand = []
        self.points = 0

    def take_card(self, card):
        """Add a card to the hand and count points"""
        self.hand.append(card)
        self.points += Card.convert_card_to_points(card)

    def show_hand(self):
        return "".join(card.get_card() for card in self.hand)

    def clear(self):
        self.points = 0
        self.hand = []

    def __str__(self):
        """Return a string representation of the player"""
        return f"Dealer - {self.name}"


class Player(Dealer):
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
    MIN_BID = 10
    MAX_BID = 500

    def __init__(self, dealer, player, deck):
        """Initialize the game attributes"""
        self.dealer = dealer
        self.player = player
        self.deck = deck

    def take_bid(self):
        while True:
            bid = int(input("Take your bid: "))
            if bid > self.player.balance:
                print("Your bid was greater than your balance! Take bid again!")
            elif bid < self.MIN_BID or bid > self.MAX_BID:
                print("Your bid must be between 10 and 500! Take bid again!")
            else:
                return bid

    def end_round(self):
        print("Your hand:\n\t", self.player.show_hand(), "Your points:", {self.player.points})
        print("Dealer hand:\n\t", self.dealer.show_hand(), "Dealer points:", {self.dealer.points})
        self.player.clear()
        self.dealer.clear()

    def start_round(self):
        self.player.take_card(self.deck.deal_card())
        self.dealer.take_card(self.deck.deal_card())

        self.player.take_card(self.deck.deal_card())
        self.dealer.take_card(self.deck.deal_card())

        print("Your hand:\n\t", self.player.show_hand())
        print("Dealer hand:\n\t ??", self.dealer.hand[1])

    def win_round(self, bid):
        print("Your win!")
        self.player.balance += bid
        self.end_round()

    def lose_round(self, bid):
        print("Your lose!")
        self.player.balance -= bid
        self.end_round()

    def result_round(self, bid):
        if self.player.points > 21:
            self.lose_round(bid)
            return

        while self.dealer.points < 17:
            self.dealer.take_card(self.deck.deal_card())
            if self.dealer.points > 21:
                self.win_round(bid)
                return

        if self.player.points < self.dealer.points:
            self.lose_round(bid)
        elif self.player.points > self.dealer.points:
            self.win_round(bid)
        else:
            print("Push!")
            self.end_round()

    def round(self):
        """Round the game"""
        bid = self.take_bid()
        self.start_round()
        if self.player.points == 21 and self.dealer.points != 21:
            print("BlackJack!")
            self.win_round(bid * 1.5)
            return

        while True:
            print("1.Hit\n2.Stand\n3.Double Down\n4.Surrender\n")
            choice = input("Enter your choice: ").strip()
            match choice:
                case "1":
                    self.player.take_card(self.deck.deal_card())
                    print("Your hand:\n\t", self.player.show_hand())
                    if self.player.points > 21:
                        self.lose_round(bid)
                        break
                case "2":
                    self.result_round(bid)
                    break
                case "3":
                    if self.player.balance >= bid * 2:
                        double_bid = bid * 2
                        self.player.take_card(self.deck.deal_card())
                        print("Your hand:\n\t", self.player.show_hand())
                        self.result_round(double_bid)
                        break
                    else:
                        print("Not enough money to double")
                case "4":
                    if len(self.player.hand) == 2:
                        self.player.balance -= bid / 2
                        self.player.clear()
                        self.dealer.clear()
                        break
                    else:
                        print("This option is only available as the first decision.")
                case _:
                    print("Invalid input, please try again!")

    def play(self):
        """Play the game"""

        while self.player.balance:
            choice = input("Continue? (y/n): ")
            if choice == "n":
                break

            self.round()

        print("Your final score is", self.player.balance)
