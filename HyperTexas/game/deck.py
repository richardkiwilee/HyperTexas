from HyperTexas.game.poker import Poker, Poker_Colors, Poker_Numbers
from HyperTexas.game.card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.id = 1
        for number in Poker_Numbers:
            for color in Poker_Colors:
                card = Poker()
                card.id = self.id
                self.id += 1
                card.Number = number
                card.Color = color
                self.cards.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def Draw(self):
        return self.cards.pop(0)

    def Add(self, card: Poker):
        self.cards.append(card)
        card.id = self.id
        self.id += 1

    def Get(self, id):
        for poker in self.cards:
            if poker.id == id:
                return poker
        return None

    def dump(self):
        return [poker.to_dict() for poker in self.cards]


class ConsumeDeck:
    def __init__(self):
        self.cards = []
        
        
    def shuffle(self):
        random.shuffle(self.cards)

    def Draw(self):
        return self.cards.pop(0)

    def Add(self, card: Card):
        self.cards.append(card)

    def Pop(self):
        return self.cards.pop()
