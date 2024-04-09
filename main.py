import lib


if __name__ == "__main__":
    deck = lib.Deck.create_deck(True)

    croupier = lib.Croupier("Robert")
    player = lib.Player("John", 1000)

    print(croupier)
    print(player)

    game = lib.Game(croupier, player, deck)
    game.play()
