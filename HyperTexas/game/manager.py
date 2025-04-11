from HyperTexas.game.table import Disable_Diamond, Disable_Head, Disable_Heart
from .level import Level
from .deck import Deck
from .character import *
from .tarot import Tarot
from .planet import Planet

class Manager:
    def __init__(self):
        self.level = Level()
        self.character_dict = dict()
        self.public_cards = []
        self.deck = Deck()
        self.deck.shuffle()
        self.table_effect = None
        self.current_round = 0
        self.active_players = []  # 当前回合活跃的玩家列表

    def CalInterest(self, character: Character):
        # 计算利息
        return min(character.max_interest, character.gold//character.per_interest)

    def FindPlayType(self, cards: list):
        # 根据self.poker_play找到类型
        _type = Score_Name_No_Pair
        return _type

    def GetScorablePokers(self, cards: list) -> list:
        # 获取可计算得分的扑克
        scorable_cards = []
        for card in cards:
            if self.table_effect == Disable_Heart and card.Color == Poker_Color_Heart:
                continue
            if card.table_effect == Disable_Diamond and card.Color == Poker_Color_Diamond:
                continue
            if card.table_effect == Disable_Club and card.Color == Poker_Color_Club:
                continue
            if card.table_effect == Disable_Spade and card.Color == Poker_Color_Spade:
                continue
            if card.table_effect == Disable_Head:
                if card.Number == Poker_Number_J:
                    continue
                if card.Number == Poker_Number_Q:
                    continue
                if card.Number == Poker_Number_K:
                    continue
                scorable_cards.append(card) 
        return scorable_cards

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
                for joker in self.joker:    # type: Joker
                    joker.Score(character, poker)
            if poker.Wax == Poker_Wax_Blue:
                if len(character.consume) < character.max_consume:
                    _planet = Planet(_type)
                    character.consume.append(_planet)
            if poker.Wax == Poker_Wax_Purple:
                if len(character.consume) < character.max_consume:
                    _tarot = Tarot(_type)
                    character.consume.append(_tarot)
        for joker in self.joker:    # type: Joker
            joker.Trig(character)
        self.TrigTableEffect(character)
        return character.chip * character.mag

    def deal_initial_cards(self):
        """发放初始牌：3张公共牌和每个玩家2张手牌"""
        self.public_cards = []
        # 发放3张公共牌
        for _ in range(3):
            card = self.deck.draw()
            if card:
                self.public_cards.append(card)
        
        # 给每个玩家发2张手牌
        for player in self.active_players:
            player.pokers = []
            for _ in range(2):
                card = self.deck.draw()
                if card:
                    player.pokers.append(card)

    def deal_community_card(self):
        """发放一张公共牌"""
        card = self.deck.draw()
        if card:
            self.public_cards.append(card)

    def player_action(self, character: Character):
        """玩家执行操作"""
        # TODO: 实现玩家的具体操作（check, bet, fold等）
        pass

    def play_round(self):
        """执行一个完整的德州扑克回合"""
        self.current_round += 1
        self.deck.shuffle()  # 每轮开始时洗牌
        
        # 重置玩家状态
        self.active_players = list(self.character_dict.values())
        
        # Pre-flop: 发放初始牌
        self.deal_initial_cards()
        
        # 第一轮操作
        for player in self.active_players:
            self.player_action(player)
        
        # Flop后的操作已完成，发第4张牌 (Turn)
        self.deal_community_card()
        
        # 第二轮操作
        for player in self.active_players:
            self.player_action(player)
            
        # 发第5张牌 (River)
        self.deal_community_card()
        
        # 最后一轮操作
        for player in self.active_players:
            self.player_action(player)
            
        # 结算所有玩家的分数
        for player in self.active_players:
            # 合并公共牌和手牌进行最终计算
            all_cards = player.pokers + self.public_cards
            self.Score(player)