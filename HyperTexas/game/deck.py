from .poker import Poker, Poker_Colors, Poker_Numbers

class Deck:
    def __init__(self):
        self.cards = []
        for number in Poker_Numbers:
            for color in Poker_Colors:
                card = Poker()
                card.Number = number
                card.Color = color
                self.cards.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def Draw(self):
        return self.cards.pop(0)

    def Add(self, card: Poker):
        self.cards.append(card)
