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
            'No_Pair' : 0,
            'One_Pair' : 0,
            'Two_Pair' : 0,
            'Three' : 0,    # 三条
            'Straight' : 0, # 顺子
            'Flush' : 0,    # 同花
            'Full_House' : 0,    # 葫芦 
            'Four' : 0,    # 四条
            'Straight_Flush' : 0, # 同花顺
            'Five' : 0,  # 五条
            'House_Flush' : 0,   # 同花葫芦
            'Five_Flush' : 0    # 同花五条
        }
        self.chip = 0
        self.mag = 0

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

    def OnPlayerAct(self):
        pass

    def CalInterest(self):
        # 计算利息
        return min(self.max_interest, self.gold//self.per_interest)

    def FindPlayType(self):
        # 根据self.poker_play找到类型
        _type = Score_Name_No_Pair
        return _type

    def GetScorablePokers(self) -> list:
        # 获取可计算得分的扑克
        return []

    def ScoreCard(self, poker):
        if poker.Material == Poker_Material_Universal:
            pass
        if poker.Material == Poker_Material_Gold:
            self.gold += 3
        if poker.Material == Poker_Material_Glass:
            pass
        if poker.Material == Poker_Material_Iron:
            pass
        if poker.Material == Poker_Material_Stone:
            self.chip += 50
        if poker.Material == Poker_Material_Lucky:
            r = random.random(0, 100)
            if r < 20:
                self.mag += 20
            r = random.random(0, 100)
            if r < 7:
                self.gold += 20
        if poker.Material == Poker_Material_Chip:
            self.chip += 30
        if poker.Material == Poker_Material_Magnification:
            self.mag += 4
        if poker.Number == Poker_Number_A:
            self.chip += 11
        if poker.Number == Poker_Number_2:
            self.chip += 2
        if poker.Number == Poker_Number_3:
            self.chip += 3
        if poker.Number == Poker_Number_4:
            self.chip += 4
        if poker.Number == Poker_Number_5:
            self.chip += 5
        if poker.Number == Poker_Number_6:
            self.chip += 6
        if poker.Number == Poker_Number_7:
            self.chip += 7
        if poker.Number == Poker_Number_8:
            self.chip += 8
        if poker.Number == Poker_Number_9:
            self.chip += 9
        if poker.Number == Poker_Number_10:
            self.chip += 10
        if poker.Number == Poker_Number_J:
            self.chip += 10
        if poker.Number == Poker_Number_Q:
            self.chip += 10
        if poker.Number == Poker_Number_K:
            self.chip += 10


    def Score(self):
        # 计算得分
        self.chip = 0
        self.mag = 0
        _type = self.FindPlayType()
        scorable = self.GetScorablePokers()
        self.chip, self.mag = BASE_SCORE[_type]
        bouns_chip, bouns_mag = BONUS_SCORE[_type]
        self.chip += bouns_chip
        self.mag += bouns_mag
        for poker in self.poker_play: # type: Poker
            if poker.id not in scorable:
                continue
            self.ScoreCard(poker)
            for joker in self.joker:
                pass
            if poker.Wax == Poker_Wax_Gold:
                self.gold += 3
            if poker.Wax == Poker_Wax_Red:
                self.ScoreCard(poker)
                for joker in self.joker:
                    pass
            if poker.Wax == Poker_Wax_Blue:
                # 生成一张当前出牌的星球牌
                pass
            if poker.Wax == Poker_Wax_Purple:
                # 生成一张塔罗牌
                pass
        return self.chip * self.mag