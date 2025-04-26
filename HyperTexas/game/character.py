from HyperTexas.game.base_score import *

class Character:
    def __init__(self):
        self.desc = ""
        self.max_poker = 2      # 最大扑克手牌数
        self.pokers = []
        self.poker_play = []
        self.max_consume = 5    # 最多5个消耗牌
        self.consume = []
        self.effects = []
        self.gold = 0           # 初始筹码数    
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
        self.custom_tag = []
        self.poker_scored = []
        self.poker_unscored = []
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
