import lib


if __name__ == "__main__":
    deck = lib.Deck.create_deck(True)

    print(deck)
    print(len(deck))

    for card in deck:
        print(card)
