import lib


if __name__ == "__main__":
    deck = lib.Deck.create_deck(True)

    dealer = lib.Dealer("Albert")
    player = lib.Player("Dmytro")
    player.replenish()

    print(">>{}\n>>{}".format(dealer, player))
    print(f"\tMin bid is {lib.Game.MIN_BID}\n\tMax bid is {lib.Game.MAX_BID}")

    game = lib.Game(dealer, player, deck)
    game.play()
