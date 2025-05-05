try:
    from .poker import Poker
    from .base_score import *
except:
    from poker import Poker
    from base_score import *


class PlayerInfo:
    def __init__(self):
        self.username = ""
        self.chip = 0   # 筹码
        self.pokers = []  # 底牌数量
        self.hand_cards = [] # 技能卡数量
        self.effects = []
        self.skill = None   # 技能
        self.level = {
            Score_Name_No_Pair : 0,
            Score_Name_One_Pair : 0,
            Score_Name_Two_Pair : 0,
            Score_Name_Three : 0,    # 三条
            Score_Name_Straight : 0, # 顺子
            Score_Name_Flush : 0,    # 同花
            Score_Name_Full_House : 0,    # 葫芦 
            Score_Name_Four : 0,    # 四条
            Score_Name_Straight_Flush : 0, # 同花顺
            Score_Name_Five : 0,  # 五条
            Score_Name_House_Flush : 0,   # 同花葫芦
            Score_Name_Five_Flush : 0    # 同花五条
        }


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
        self.level = info.get('level')

    def to_dict(self):
        return {
            'username': self.username,
            'chip': self.chip,
            'pokers': [i.to_dict() for i in self.pokers],
            'hand_cards': [i.to_dict() for i in self.hand_cards],
            'effects': self.effects,
            'skill': self.skill,
            'level': self.level
        }
