from .base_score import *

class Character:
    def __init__(self):
        self.max_poker = 2      # 最大扑克手牌数
        self.poker = []
        self.poker_play = []
        self.max_joker = 5      # 最大小丑牌数
        self.joker = []
        self.max_consume = 3    # 最多3个消耗牌
        self.consume = []
        self.gold = 4           # 初始金币数    
        self.per_interest = 5   # 每5金币获得利息
        self.max_interest = 5   # 最多5个金币利息
        self.skill = None
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
        self.chip = 0
        self.mag = 0
        self.played_type = None

    def OnGameStart(self):
        pass

    def OnTurnStart(self):
        pass

    def OnTurnEnd(self):
        pass

    def OnRoundStart(self):
        pass

    def OnRoundEnd(self):
        pass
