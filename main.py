import lib


if __name__ == "__main__":
    deck = lib.Deck.create_deck(True)

    dealer = lib.Dealer("Albert")
    player = lib.Player("Dmytro", 500)

    print(dealer)
    print(player)
    print(f"Min bid is {lib.Game.MIN_BID}, Max bid is {lib.Game.MAX_BID}")

    game = lib.Game(dealer, player, deck)
    game.play()
