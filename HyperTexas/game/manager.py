from .level import Level
from .deck import Deck
from .character import Character

class Manager:
    def __init__(self):
        self.level = Level()
        self.character_dict = dict()
        self.public_cards = []
        self.deck = Deck()
        self.deck.shuffle()
