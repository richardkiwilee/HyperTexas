from .level import Level
from .deck import Deck
from .character import *

class Manager:
    def __init__(self):
        self.level = Level()
        self.character_dict = dict()
        self.public_cards = []
        self.deck = Deck()
        self.deck.shuffle()
        self.table_effect = None

    def CalInterest(self, character: Character):
        # 计算利息
        return min(character.max_interest, character.gold//character.per_interest)

    def FindPlayType(self, cards: list):
        # 根据self.poker_play找到类型
        _type = Score_Name_No_Pair
        return _type

    def GetScorablePokers(self, cards: list) -> list:
        # 获取可计算得分的扑克
        return []

    def ScoreCard(self, character: Character, poker: Poker):
        if poker.Material == Poker_Material_Universal:
            pass
        if poker.Material == Poker_Material_Gold:
            character.gold += 3
        if poker.Material == Poker_Material_Glass:
            pass
        if poker.Material == Poker_Material_Iron:
            pass
        if poker.Material == Poker_Material_Stone:
            character.chip += 50
        if poker.Material == Poker_Material_Lucky:
            r = random.random(0, 100)
            if r < 20:
                character.mag += 20
            r = random.random(0, 100)
            if r < 7:
                character.gold += 20
        if poker.Material == Poker_Material_Chip:
            character.chip += 30
        if poker.Material == Poker_Material_Magnification:
            character.mag += 4
        if poker.Number == Poker_Number_A:
            character.chip += 11
        if poker.Number == Poker_Number_2:
            character.chip += 2
        if poker.Number == Poker_Number_3:
            character.chip += 3
        if poker.Number == Poker_Number_4:
            character.chip += 4
        if poker.Number == Poker_Number_5:
            character.chip += 5
        if poker.Number == Poker_Number_6:
            character.chip += 6
        if poker.Number == Poker_Number_7:
            character.chip += 7
        if poker.Number == Poker_Number_8:
            character.chip += 8
        if poker.Number == Poker_Number_9:
            character.chip += 9
        if poker.Number == Poker_Number_10:
            character.chip += 10
        if poker.Number == Poker_Number_J:
            character.chip += 10
        if poker.Number == Poker_Number_Q:
            character.chip += 10
        if poker.Number == Poker_Number_K:
            character.chip += 10

    def TrigTableEffect(self, character: Character):
        if self.table_effect == Enhance_No_Pair:
            if character.played_type == Score_Name_No_Pair:
                character.mag *= 2
        if self.table_effect == Enhance_One_Pair:
            if character.played_type == Score_Name_One_Pair:
                character.mag *= 2
        if self.table_effect == Enhance_Two_Pair:
            if character.played_type == Score_Name_Two_Pair:
                character.mag *= 2
        if self.table_effect == Enhance_Three:
            if character.played_type == Score_Name_Three:
                character.mag *= 2
        if self.table_effect == Enhance_Straight:
            if character.played_type == Score_Name_Straight:
                character.mag *= 2
        if self.table_effect == Enhance_Flush:
            if character.played_type == Score_Name_Flush:
                character.mag *= 2
                
        if self.table_effect == Lower_Level:
            pass
        if self.table_effect == Disable_Flush:
            pass
        if self.table_effect == Disable_Heart:
            pass
        if self.table_effect == Disable_Diamond:
            pass
        if self.table_effect == Disable_Club:
            pass
        if self.table_effect == Disable_Plum:
            pass
        if self.table_effect == Less_Hand:
            pass
        if self.table_effect == Disable_Head:
            pass
        if self.table_effect == Debuff_Tax:
            character.gold -= len(character.pokers)
            if character.gold < 0:
                character.gold = 0
        if self.table_effect == Debuff_Half:
            character.chip = character.chip // 2
            character.mag = character.mag // 2
        if self.table_effect == Buff_Small_Bet:
            pass
        if self.table_effect == Debuff_Big_Bet:
            pass


    def Score(self, character: Character) -> int:
        # 计算得分
        character.chip = 0
        character.mag = 0
        _type = self.FindPlayType()
        character.played_type = _type
        scorable = self.GetScorablePokers()
        character.chip, character.mag = BASE_SCORE[_type]
        bouns_chip, bouns_mag = LEVEL_BOUNS_SCORE[_type]
        level = character.level.get(_type) or 0
        # 特殊处理
        if self.table_effect == Lower_Level:
            level = level // 2
        character.chip += bouns_chip * level
        character.mag += bouns_mag * level
        for poker in self.poker_play: # type: Poker
            if poker.id not in scorable:
                continue
            self.ScoreCard(character, poker)
            for joker in self.joker:    # type: Joker
                joker.Score(character, poker)
            if poker.Wax == Poker_Wax_Gold:
                character.gold += 3
            if poker.Wax == Poker_Wax_Red:
                self.ScoreCard(character, poker)
                for joker in self.joker:
                    joker.Score(character, poker)
            if poker.Wax == Poker_Wax_Blue:
                # 生成一张当前出牌的星球牌
                pass
            if poker.Wax == Poker_Wax_Purple:
                # 生成一张塔罗牌
                pass
        for joker in self.joker:    # type: Joker
            joker.Trig(character)
        self.TrigTableEffect(character)
        return character.chip * character.mag