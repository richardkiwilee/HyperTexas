from pdb import main
from collections import defaultdict

try:
    from HyperTexas.game.player import PlayerInfo
    from HyperTexas.game.poker import *
    from HyperTexas.game.base_score import *
except:
    from player import PlayerInfo
    from poker import *
    from base_score import *

class PokerScorer:
    @staticmethod
    def score(pokers: list):     # list[Poker] -> (str, list[Poker])
        for poker in pokers:
            print(poker.to_dict())
        if not pokers:
            largest = pokers[0]
            for poker in pokers:
                if poker.number > largest.number:
                    largest = poker
            return Score_Name_No_Pair, [largest]
        
        # 统计数字和花色
        number_count = defaultdict(list)
        color_count = defaultdict(list)
        for poker in pokers:
            number_count[poker.Number].append(poker)
            color_count[poker.Color].append(poker)
            
        # 按数量排序
        number_groups = sorted([(len(v), k, v) for k, v in number_count.items()], reverse=True)
        
        # 检查是否同花
        is_flush = any(len(cards) >= 5 for cards in color_count.values())
        if is_flush:
            return Score_Name_Flush, pokers

        # 检查是否顺子
        def is_straight(cards):
            numbers = sorted(set(card.Number for card in cards), key=lambda x: Poker_Numbers.index(x))
            if len(numbers) < 5:
                return False, []
            
            # 处理A2345特殊顺子
            if Poker_Number_A in numbers and Poker_Number_2 in numbers:
                low_straight = [n for n in numbers if n in [Poker_Number_A, Poker_Number_2, Poker_Number_3, Poker_Number_4, Poker_Number_5]]
                if len(low_straight) >= 5:
                    straight_cards = []
                    for num in [Poker_Number_A, Poker_Number_2, Poker_Number_3, Poker_Number_4, Poker_Number_5]:
                        straight_cards.extend(number_count[num][:1])
                    return True, straight_cards[:5]
            
            # 常规顺子
            for i in range(len(numbers) - 4):
                indices = [Poker_Numbers.index(numbers[j]) for j in range(i, i + 5)]
                if indices == list(range(min(indices), max(indices) + 1)):
                    straight_cards = []
                    for num in numbers[i:i+5]:
                        straight_cards.extend(number_count[num][:1])
                    return True, straight_cards
            return False, []
        
        has_straight, straight_cards = is_straight(pokers)
        
        # 判断牌型
        if is_flush and number_groups[0][0] == 5:
            return Score_Name_Five_Flush, flush_cards[:5]
        elif is_flush and number_groups[0][0] == 3 and number_groups[1][0] == 2:
            return Score_Name_House_Flush, flush_cards[:5]
        elif number_groups[0][0] == 5:
            return Score_Name_Five, number_groups[0][2][:5]
        elif is_flush and has_straight and all(card in flush_cards for card in straight_cards):
            return Score_Name_Straight_Flush, straight_cards
        elif number_groups[0][0] == 4:
            return Score_Name_Four, number_groups[0][2][:4] + number_groups[1][2][:1]
        elif number_groups[0][0] == 3 and number_groups[1][0] == 2:
            return Score_Name_Full_House, number_groups[0][2][:3] + number_groups[1][2][:2]
        elif is_flush:
            return Score_Name_Flush, flush_cards
        elif has_straight:
            return Score_Name_Straight, straight_cards
        elif number_groups[0][0] == 3:
            return Score_Name_Three, number_groups[0][2][:3] + number_groups[1][2][:1] + number_groups[2][2][:1]
        elif number_groups[0][0] == 2 and number_groups[1][0] == 2:
            return Score_Name_Two_Pair, number_groups[0][2][:2] + number_groups[1][2][:2] + number_groups[2][2][:1]
        elif number_groups[0][0] == 2:
            return Score_Name_One_Pair, number_groups[0][2][:2] + number_groups[1][2][:1] + number_groups[2][2][:1] + number_groups[3][2][:1]
        else:
            sorted_cards = sorted(pokers, key=lambda x: Poker_Numbers.index(x.Number))
            return Score_Name_No_Pair, sorted_cards[:5]
    
    @staticmethod
    def ScoreResult(score_type, score_list: list , player: PlayerInfo):
        
        return 0

if __name__ == "__main__":
    p = []
    for i in range(0, 5):
        c = Poker()
        c.from_dict({'id': None, 'Number': None, 'Color': None, 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}})
        p.append(c)
    print(PokerScorer.score(p))
