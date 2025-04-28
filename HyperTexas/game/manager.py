from typing import List, Set, Dict, Any, Optional
from HyperTexas.game.deck import Deck, ConsumeDeck
from HyperTexas.game.character import *
from HyperTexas.game.poker import *
import random
from HyperTexas.game.game_enum import *


class Manager:
    def __init__(self):
        self.public_cards = []
        self.last_used_cards = []
        self.deck = Deck()
        self.consume = ConsumeDeck()
        self.deck.shuffle()
        self.consume.shuffle()
        self.player_order = []  # 当前回合活跃的玩家列表 保存player类
        self.base_chip = 30 * 10000     # 初始30万筹码
        self.level = 1      # 每个回合 输的人要额外支付level * 1k的底注
        self.player_deals = {}  # 记录玩家的出牌
        self.current_player_index = 0  # 当前操作玩家的索引
        self.round_confirmations = set()  # type: Set[Any]  # 记录已确认结果的玩家
        self.game_status = GameStatus.LOBBY.value

    def get_all_pokers(self) -> List[Any]:
        """Get all pokers in the game"""
        return []

    def set_init_chips(self, chip: int) -> None:
        # 设置初始筹码数x万
        self.base_chip = chip * 10000

    def GameFinished(self) -> bool:
        """检查游戏是否结束"""
        for character in self.player_order:
            if character.gold <= 0:
                return True
        return False

    def deal_cards(self, count: int = 1, target: Optional[Any] = None) -> List[Any]:
        """通用的发牌函数
        
        Args:
            count: 要发的牌数
            target: 发给谁（None表示发公共牌）
            
        Returns:
            list: 发出的牌列表
        """
        cards = []
        for _ in range(count):
            card = self.deck.draw()
            if card:
                cards.append(card)
                if target:
                    target.pokers.append(card)
                else:
                    self.public_cards.append(card)
        return cards

    def get_current_player(self) -> Any:
        """获取当前回合的玩家"""
        if not self.player_order:
            return None
        return self.player_order[self.current_player_index]

    def next_player(self) -> Any:
        """移动到下一个玩家"""
        self.current_player_index = (self.current_player_index + 1) % len(self.player_order)
        return self.get_current_player()

    def record_player_deal(self, player_name: str, cards: List[Any]) -> bool:
        """记录玩家的出牌"""
        # TODO: 在这里添加出牌合法性检查
        self.player_deals[player_name] = cards
        return True

    def all_players_dealt(self) -> bool:
        """检查是否所有玩家都已出牌"""
        return len(self.player_deals) == len(self.player_order)

    def confirm_round_result(self, player_name: str) -> bool:
        """玩家确认回合结果"""
        self.round_confirmations.add(player_name)
        return len(self.round_confirmations) == len(self.player_order)

    def start_new_round(self, new_starter: Optional[str] = None) -> None:
        """开始新的一轮"""
        self.game_status = GameStatus.ROUND_START.value
        self.current_player_index = 0
        self.round_confirmations.clear()
        for poker in self.public_cards:
            self.deck.add(poker)
        self.public_cards.clear()
        for player in self.player_order:
            for poker in player.pokers:
                self.deck.add(poker)
            player.pokers.clear()
        for poker in self.deck:
            poker.ResetVisible()
        self.deck.shuffle()
        for player in self.player_order:
            player.pokers.clear()
        if new_starter:
            while True:
                _0 = self.player_order[0]
                if _0.username == new_starter:
                    break
                _tmp = self.player_order.pop(0)
                self.player_order.append(_tmp)

    def calculate_round_result(self) -> Dict[str, Any]:
        """计算本回合的结果"""
        result = {
            'deals': self.player_deals,
            'scores': {}
        }
        
        # 计算每个玩家的得分
        for player in self.player_order:
            # 合并公共牌和手牌进行最终计算
            all_cards = player.pokers + self.public_cards
            score = self.Score(player)
            result['scores'][player.name] = score
        
        return result

    def Score(self, character: Character) -> int:
        """计算玩家得分"""
        # 保留原有的得分计算逻辑
        _score_info = {
            'score_type': None,
            'score_level': 0,
            'add_chip': 0,
            'add_mag': 0,
            'mut_mag': 1.0
        }
        _type = self.FindPlayType()
        _score_info['score_type'] = _type
        character.played_type = _type
        scorable = self.GetScorablePokers()
        character.chip, character.mag = BASE_SCORE[_type]
        bouns_chip, bouns_mag = LEVEL_BOUNS_SCORE[_type]
        level = character.level.get(_type) or 0
        _score_info['score_level'] = level
        self._before_score(character, _score_info)
        for poker in self.poker_play: # type: Poker
            self._score_card(character, poker, _score_info)
            if poker.Wax == Poker_Wax_Gold:
                character.gold += 3
            if poker.Wax == Poker_Wax_Red:
                self._score_card(character, poker, _score_info)                
            if poker.Wax == Poker_Wax_Blue:
                if len(character.consume) < character.max_consume:
                    _planet = Planet(_type)
                    character.consume.append(_planet)
            if poker.Wax == Poker_Wax_Purple:
                if len(character.consume) < character.max_consume:
                    _tarot = Tarot(_type)
                    character.consume.append(_tarot)
        self._after_score(character, _score_info)
        return character.chip * character.mag

    def _before_score(self, character: Character, _score_info: Dict[str, Any]) -> None:
        pass

    def _after_score(self, character: Character, _score_info: Dict[str, Any]) -> None:
        pass
    
    def _score_card(self, character: Character, poker: Poker, _score_info: Dict[str, Any]) -> None:
        _chip = 0
        _mag = 0
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

    def FindPlayType(self, cards: List[Any]) -> Any:
        # 根据self.poker_play找到类型
        _type = Score_Name_No_Pair
        return _type

    def play_round(self) -> None:
        """执行一个完整的德州扑克回合"""
        self.current_round += 1
        self.deck.shuffle()  # 每轮开始时洗牌
        
        # Pre-flop: 发放初始牌
        for player in self.player_order:
            self.deal_cards(count=2, target=player)
        
        # 第一轮操作
        for player in self.player_order:
            self.player_action(player)
        
        # Flop后的操作已完成，发第4张牌 (Turn)
        self.deal_cards(count=1)
        
        # 第二轮操作
        for player in self.player_order:
            self.player_action(player)
            
        # 发第5张牌 (River)
        self.deal_cards(count=1)
        
        # 最后一轮操作
        for player in self.player_order:
            self.player_action(player)
            
        # 结算所有玩家的分数
        for player in self.player_order:
            # 合并公共牌和手牌进行最终计算
            all_cards = player.pokers + self.public_cards
            self.Score(player)

    def dumpPlayerInfo(self) -> Dict[str, Any]:
        info = dict()
        info['game_status'] = self.game_status
        info['current_player_index'] = self.current_player_index
        info['players'] = self.player_order   
        info['public_cards'] = [i.to_dict() for i in self.public_cards]
        info['last_used_cards'] = self.last_used_cards
        info['deck'] = [i.to_dict() for i in self.deck]       # 默认玩家是无法看到牌顶的
        return info
