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

# 检查是否顺子
def check_is_straight(cards):
    numbers = [trans_number_to_int(card) for card in cards]
    if len(numbers) < 5:
        return False
    _max = max(numbers)
    _min = min(numbers)
    if _max - _min == 4:
        if _max == 14:
            return 2     # 高顺
        return 1         # 常规顺子
    if set(numbers) == {2, 3, 4, 5, 14}:
        return 1         # 低顺
    return 0


def Find_Biggest_Card(cards):
    _ = 0
    _poker = None
    for card in cards:
        _num = trans_number_to_int(card)
        if _num > _:
            _ = _num
            _poker = card
    return _poker


def trans_number_to_int(poker):
    _ = poker.Number
    if Poker_Number_A == _:
        return 14
    if Poker_Number_2 == _:
        return 2
    if Poker_Number_3 == _:
        return 3
    if Poker_Number_4 == _:
        return 4
    if Poker_Number_5 == _:
        return 5
    if Poker_Number_6 == _:
        return 6
    if Poker_Number_7 == _:
        return 7
    if Poker_Number_8 == _:
        return 8
    if Poker_Number_9 == _:
        return 9
    if Poker_Number_10 == _:
        return 10
    if Poker_Number_J == _:
        return 11
    if Poker_Number_Q == _:
        return 12
    if Poker_Number_K == _:
        return 13


class PokerScorer:
    @staticmethod
    def score(pokers: list):     # list[Poker] -> (str, list[Poker])
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
        
        # 按数量排序  [(cnt, key, cards), ]
        number_groups = sorted([(len(v), k, v) for k, v in number_count.items()], reverse=True)
        color_groups = sorted([(len(v), k, v) for k, v in color_count.items()], reverse=True)

        is_flush = color_groups[0][0] == 5
        is_straight = check_is_straight(pokers)
        print('number_count: ', number_groups)
        print('color_count: ', color_groups)
        print(f'is_flush: {is_flush}, is_straight: {is_straight}')
        # 同花五条 
        if is_flush and number_groups[0][0] == 5:        
            return Score_Name_Five_Flush, number_groups[0][2]
        # 同花葫芦 
        if is_flush and len(number_groups) >= 2:
            if number_groups[0][0] == 3 and number_groups[1][0] == 2:
                return Score_Name_House_Flush, number_groups[0][2] + number_groups[1][2]
        # 五条 
        if number_groups[0][0] == 5:
            return Score_Name_Five, number_groups[0][2]
        # 皇家同花顺 
        if is_straight == 2 and is_flush:
            return Score_Name_Straight, pokers
        # 同花顺 
        if is_straight and is_flush:
            return Score_Name_Straight, pokers
        # 四条 
        if number_groups[0][0] == 4:
            return Score_Name_Four, number_groups[0][2]
        # 葫芦 
        if len(number_groups) >= 2:
            if number_groups[0][0] == 3 and number_groups[1][0] == 2:
                return Score_Name_House, number_groups[0][2] + number_groups[1][2]
        # 同花 
        if color_groups[0][0] == 5:
            return Score_Name_Flush, color_groups[0][2]
        # 顺子 
        if is_straight:
            return Score_Name_Straight, pokers
        # 三条 
        if number_groups[0][0] == 3:
            return Score_Name_Three, number_groups[0][2]
        # 两对 
        if len(number_groups) >= 2:
            if number_groups[0][0] == 2 and number_groups[1][0] == 2:
                return Score_Name_Two_Pair, number_groups[0][2] + number_groups[1][2]
        # 对子 
        if number_groups[0][0] == 2:
            return Score_Name_One_Pair, number_groups[0][2]
        # 高牌
        return Score_Name_No_Pair, [Find_Biggest_Card(pokers)]

if __name__ == "__main__":
    p = []
    for i in range(0, 5):
        c = Poker()
        c.from_dict({'id': 31, 'Number': 'Number_8', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': ['host'], 'color': ['host']}})
        p.append(c)
        break
    print(PokerScorer.score(p))
