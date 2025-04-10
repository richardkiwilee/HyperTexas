from HyperTexas.game.character import Character


class Joker:
    def __init__(self):
        self.id = None
        self.price = 0
    
    def Trig(self, character: Character):
        pass

    def Score(self, character: Character, poker: Poker):
        pass

    def OnGetJoker(self, character: Character, joker: Joker):
        pass

    def OnSellJoker(self, character: Character, joker: Joker):
        pass
