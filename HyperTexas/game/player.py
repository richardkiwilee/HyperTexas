from .character import Character

class Yuri(Character):
    def __init__(self):
        super().__init__()
        self.max_poker = 3
        self.desc = "扑克底牌数为3"
