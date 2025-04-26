from .character import Character
from .poker import Poker


class Yuri(Character):
    def __init__(self):
        super().__init__()
        self.max_poker = 3
        self.desc = "扑克底牌数为3"


class PlayerInfo:
    def __init__(self):
        self.username = ""
        self.chip = 0   # 筹码
        self.pokers = []  # 底牌数量
        self.hand_cards = [] # 技能卡数量
        self.effects = []
        self.skill = None   # 技能

    def from_dict(self, info: dict):
        self.username = info.get('username')
        self.chip = info.get('chip')
        for poker_info in info.get('poker'):
            poker = Poker()
            poker.from_dict(poker_info)
            self.pokers.append(poker)
        self.hand_cards = info.get('hand_cards')
        self.effects = info.get('effects')
        self.skill = info.get('skill')

    def to_dict(self):
        return {
            'username': self.username,
            'chip': self.chip,
            'pokers': [i.to_dict() for i in self.pokers],
            'hand_cards': self.hand_cards,
            'effects': self.effects,
            'skill': self.skill
        }
