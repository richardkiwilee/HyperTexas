import stat
import random
from HyperTexas.game.poker import *
from HyperTexas.game.base_score import *
from HyperTexas.game.manager import Manager
EFFECT_DICT = dict()

CONDITIN_GOLD_BASE = 10000
     
EFFECT_1 = "计分时, 黑桃+3倍率"
EFFECT_2 = "计分时, 红桃+3倍率"
EFFECT_3 = "计分时, 梅花+3倍率"
EFFECT_4 = "计分的黑桃牌给予x1.5倍率"
EFFECT_5 = "计分的红桃有1/2概率给予x1.5倍率"
EFFECT_6 = "计分的黑桃给予+50筹码"
EFFECT_7 = "计分的梅花给予+7倍率"
EFFECT_8 = "红桃无效"
EFFECT_9 = "黑桃无效"
EFFECT_10 = "梅花无效"
EFFECT_11 = "方块无效"
EFFECT_12 = "计分时, 人头牌+30筹码"
EFFECT_13 = "计分的奇数牌+30筹码"
EFFECT_14 = "计分时, A,2,3,5,8给予+8倍率"
EFFECT_15 = "计分的偶数牌+4倍率"
EFFECT_16 = "第一张计分的人头卡给予x2倍率"
EFFECT_17 = "人头牌在计分时+5倍率"
EFFECT_18 = "计分的K和Q给予x2倍率"
EFFECT_19 = "人头牌无效"
EFFECT_20 = "计分的A给予+4倍率和+20筹码"
EFFECT_21 = "计分的10和4给予+10筹码和+4倍率"
EFFECT_22 = "计分时, 打出的牌触发2次"
EFFECT_23 = "重新触发打出的2,3,4,5"
EFFECT_24 = "重新触发所有打出的牌"
EFFECT_25 = "重新触发所有打出的人头牌"
EFFECT_26 = "打出的第一张记分牌触发2次"
EFFECT_27 = "打出的每一张8在计分时有1/4概率生成一张技能卡"
EFFECT_28 = "所有计分的人头卡变成黄金卡"
EFFECT_29 = "计分后, +4倍率"
EFFECT_30 = "+100筹码"
EFFECT_31 = "1/5的概率, +20倍率"
EFFECT_32 = "+250筹码"
EFFECT_33 = "1/6的概率, +15倍率"
EFFECT_34 = "如果是对子牌型, +50筹码"
EFFECT_35 = "如果是三条牌型, +100筹码"
EFFECT_36 = "如果是两对牌型, +80筹码"
EFFECT_37 = "如果是顺子牌型, +100筹码"
EFFECT_38 = "如果是同花牌型, +80筹码"
EFFECT_39 = "如果是对子牌型, +8倍率"
EFFECT_40 = "如果是三条牌型, +12倍率"
EFFECT_41 = "如果是两对牌型, +10倍率"
EFFECT_42 = "如果是同花牌型, +10倍率"
EFFECT_43 = "如果出牌少于3张, +20倍率"
EFFECT_44 = "每一张计分的Q, 给予+13倍率"
EFFECT_45 = "如果有3张计分的人头牌, +10倍率"
EFFECT_46 = "如果牌记分牌中含有4种花色, x3倍率"
EFFECT_47 = "如果牌型为两对, x2倍率"
EFFECT_48 = "如果牌型为三条, x3倍率"
EFFECT_49 = "如果牌型为四条, x4倍率"
EFFECT_50 = "如果牌型为顺子, x3倍率"
EFFECT_51 = "如果牌型为同花, x2倍率"
EFFECT_52 = "同花无效"
EFFECT_53 = "1/4概率升级打出的牌型"
EFFECT_54  = "给予牌型等级总和x0.1的倍率"
EFFECT_55 = "所有牌型等级提升1级"
EFFECT_56 = "升级打出的牌型"
EFFECT_57 = "抽牌堆内剩余的每张牌, +2筹码"
EFFECT_58 = "抽牌堆内的每一张石头牌, +25筹码"
EFFECT_59 = "抽牌堆中的每张钢铁牌+0.2倍率"
EFFECT_60 = "抽牌堆中的每一张增强卡, 给予x0.1倍率"
EFFECT_61 = "超过52张的每张卡, 给予x0.25倍率"
EFFECT_62 = "比52张少的每张卡, 给予+4倍率"
EFFECT_63 = "抽牌堆中的每一张玻璃牌给予x0.75倍率"
EFFECT_64 = "如果牌组中含有16张以上的增加牌, x3倍率"
EFFECT_65 = "少于12的每张人头牌, 给予x1倍率"
EFFECT_66 = "未计分的每张K给与x1.5倍率"
EFFECT_67 = "如果没有手牌, +15倍率"
EFFECT_68 = "牌组中的每一张黄金牌给与1w资金"
EFFECT_69 = "计分时, 每一个效果+3倍率"
EFFECT_70 = "销毁每一张计分的6, 生成相应数量的技能卡"
EFFECT_71 = "每拥有1w资金, +20筹码"
EFFECT_72 = "1/6的概率, x4倍率"
EFFECT_73 = "会是什么效果呢?[印错小丑]"
EFFECT_74 = "每拥有1w资金, +2倍率"
EFFECT_75 = "如果出牌仅有1张牌, 复制这张卡加入牌组"
EFFECT_76 = "如果出牌包含A和顺子, 生成一张技能卡"
EFFECT_77 = "如果牌型为同花顺, 生成一张技能卡"
EFFECT_78 = "计分时, 若资金少于5w, 生成一张技能卡"
EFFECT_79 = "牌组内的每一张9生成一张技能卡"
EFFECT_80 = "生成一张技能卡"


def score(poker: Poker, player):
    chip = 0
    mag = 0
    mult = 0
    color = poker.color
    number = poker.Number
    if EFFECT_19 in player.effects and number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:  # 人头无效
        return [chip, mag, mult]
    if color == Poker_Color_Heart:      # 红桃
        if EFFECT_8 in player.effects:
            return [chip, mag, mult]
        if EFFECT_2 in player.effects:
            mag += 3
        if EFFECT_5 in player.effects:
            if random.randint(1, 2) == 1:
                mag += 1.5
    if color == Poker_Color_Club:       # 黑桃
        if EFFECT_9 in player.effects:
            return [chip, mag, mult]
        if EFFECT_1 in player.effects:
            mag += 3
        if EFFECT_4 in player.effects:
            muilt += 1.5
        if EFFECT_6 in player.effects:
            chip += 50
    if color == Poker_Color_Plum:       # 梅花
        if EFFECT_10 in player.effects:
            return [chip, mag, mult]
        if EFFECT_3 in player.effects:
            mag += 3
        if EFFECT_7 in player.effects:
            mag += 7
    if color == Poker_Color_Diamond:    # 方块
        if EFFECT_11 in player.effects:
            return [chip, mag, mult]
    if number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:  # 人头牌
        if EFFECT_12 in player.effects:
            chip += 30
    if EFFECT_13 in player.effects:
        if number in [Poker_Number_A, Poker_Number_3, Poker_Number_5, Poker_Number_7, Poker_Number_9]:
            chip += 30
    if EFFECT_14 in player.effects:
        if number in [Poker_Number_A, Poker_Number_2, Poker_Number_3, Poker_Number_5, Poker_Number_8]:
            mag += 8
    if EFFECT_15 in player.effects:
        if number in [Poker_Number_2, Poker_Number_4, Poker_Number_6, Poker_Number_8, Poker_Number_10]:
            mag += 4
    if EFFECT_16 in player.effects:
        if number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:
            if EFFECT_16 not in player.custom_tag:
                mult += 2
                player.custom_tag.append(EFFECT_16)
    if EFFECT_17 in player.effects:
        if number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:
            mag += 5
    if EFFECT_18 in player.effects:
        if number in [Poker_Number_Q, Poker_Number_K]:
            mult += 2
    if EFFECT_20 in player.effects and number == Poker_Number_A:
        chip += 20
        mag += 4
    if EFFECT_21 in player.effects:
        if number in [Poker_Number_10, Poker_Number_4]:
            chip += 20
            mag += 4
    if EFFECT_22 in player.effects:
        pass
    if EFFECT_23 in player.effects:
        pass
    if EFFECT_24 in player.effects:
        pass
    if EFFECT_25 in player.effects:
        if number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:
            pass
    if EFFECT_26 in player.effects:
        pass
    if EFFECT_27 in player.effects:
        if number == Poker_Number_8:
            if random.randint(1, 4) == 1:
                pass
    if EFFECT_28 in player.effects:
        poker.Material = Poker_Material_Gold
    if EFFECT_44 in player.effects:
        if number == Poker_Number_Q:
            mag += 13
    return [chip, mag, mult]


def score_end(mgr: Manager, poker: Poker, player, play_type):
    chip = 0
    mag = 0
    mult = 0
    """
    Score_Name_No_Pair = '高牌'
    Score_Name_One_Pair = '对子'
    Score_Name_Two_Pair = '两对'
    Score_Name_Three = '三条'
    Score_Name_Straight = '顺子'
    Score_Name_Flush = '同花'
    Score_Name_Full_House = '葫芦'
    Score_Name_Four = '四条'
    Score_Name_Straight_Flush = '同花顺'
    Score_Name_Five = '五条'
    Score_Name_House_Flush = '同花葫芦'
    Score_Name_Five_Flush = '同花五条'
    """
    if EFFECT_52 in player.effects and player_type == Score_Name_Flush:
        mult -= 9999
    if EFFECT_29 in player.effects:
        mag += 4
    if EFFECT_30 in player.effects:
        chip += 100
    if EFFECT_31 in player.effects:
        if random.randint(1, 5) == 1:
            mag += 20
    if EFFECT_32 in player.effects:
        chip += 250
    if EFFECT_33 in player.effects:
        if random.randint(1, 6) == 1:
            mag += 15
    if EFFECT_34 in player.effects:
        if poker.Type == Poker_Type_Double:
            chip += 50
    if EFEFECT_34 in player.effects and play_type == Score_Name_One_Pair:
        chip += 50
    if EFFECT_35 in player.effects and play_type == Score_Name_Three:
        chip += 100
    if EFFECT_36 in player.effects and play_type == Score_Name_Two_Pair:
        chip += 80
    if EFFECT_37 in player.effects and play_type == Score_Name_Straight:
        chip += 100
    if EFFECT_38 in player.effects and play_type == Score_Name_Flush:
        chip += 80
    if EFFECT_39 in player.effects and play_type == Score_Name_One_Pair:
        mag += 8
    if EFFECT_40 in player.effects and play_type == Score_Name_Three:
        mag += 12
    if EFFECT_41 in player.effects and play_type == Score_Name_Two_Pair:
        mag += 10
    if EFFECT_42 in player.effects and play_type == Score_Name_Flush:
        mag += 10
    if EFFECT_43 in player.effects and len(player.poker_play) <= 3:
        mag += 20
    if EFFECT_45 in player.effects:
        cnt = 0
        for card in player.poker_scored:
            if card.Number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:
                cnt += 1
        if cnt >= 3:
            mag += 10
    if EFFECT_46 in player.effects:
        cnt = [0, 0, 0, 0]
        for card in player.poker_scored:
            if card.color == Poker_Color_Heart:
                cnt[0] = 1
            if card.color == Poker_Color_Club:
                cnt[1] = 1
            if card.color == Poker_Color_Diamond:
                cnt[2] = 1
            if card.color == Poker_Color_Plum:
                cnt[3] = 1
        if sum(cnt) == 4:
            mult += 3
    if EFFECT_47 in player.effects and play_type == Score_Name_Two_Pair:
        mult += 2
    if EFFECT_48 in player.effects and play_type == Score_Name_Three:
        mult += 3
    if EFFECT_49 in player.effects and play_type == Score_Name_Four:
        mult += 4
    if EFFECT_50 in player.effects and play_type == Score_Name_Straight:
        mult += 3
    if EFFECT_51 in player.effects and play_type == Score_Name_Flush:
        mult += 2
    if EFFECT_53 in player.effects:
        if random.randint(1, 4) == 1:
            player.level[play_type] += 1
    if EFFECT_54 in player.effects:
        mag += sum(player.level.values()) * 0.1
    if EFFECT_55 in player.effects:
        for k, v in player.level:
            player.level[k] += 1
    if EFFECT_56 in player.effects:
        player.level[play_type] += 1
    if EFFECT_57 in player.effects:
        chip += 2 * len(mgr.deck.cards)
    if EFFECT_58 in player.effects:
        cnt = 0
        for card in mgr.deck.cards:
            if card.Material == Poker_Material_Stone:
                cnt += 1
        chip += 25 * cnt
    if EFFECT_59 in player.effects:
        cnt = 0
        for card in mgr.deck.cards:
            if card.Material == Poker_Material_Iron:
                cnt += 1
        mag += 0.2 * cnt
    if EFFECT_60 in player.effects:
        cnt = 0
        for card in mgr.deck.cards:
            if card.Material in [Poker_Material_Universal, Poker_Material_Gold, Poker_Material_Glass, Poker_Material_Iron, Poker_Material_Stone, Poker_Material_Lucky, Poker_Material_Chip, Poker_Material_Magnification]:
                cnt += 1
        mult += 0.1 * cnt
    if EFFECT_61 in player.effects:
        if len(mgr.get_all_pokers()) > 52:
            mult += 0.25 * (len(mgr.get_all_pokers()) - 52)
    if EFFECT_62 in player.effects:
        if len(mgr.get_all_pokers()) < 52:
            mag += 4 * (52 - len(mgr.get_all_pokers()))
    if EFFECT_63 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.Material == Poker_Material_Glass:
                cnt += 1
        mult += cnt * 0.75
    if EFFECT_64 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.Material is not None:
                cnt += 1
        if cnt > 16:
            mult += 3
    if EFFECT_65 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.Number in [Poker_Number_J, Poker_Number_Q, Poker_Number_K]:
                cnt += 1
        if cnt < 12:
            mult += cnt * 1
    if EFFECT_66 in player.effects:
        cnt = 0
        for card in player.poker_unscored:
            if card.number == Poker_Number_K:
                cnt += 1
        mult += cnt * 1.5
    if EFFECT_67 in player.effects:
        if len(player.poker_unscored) == 0:
            mg += 15
    if EFFECT_68 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.Material == Poker_Material_Gold:
                cnt += 1
        player.gold += cnt * CONDITIN_GOLD_BASE
    if EFFECT_69 in player.effects:
        mag += 3 * len(player.effects)
    if EFFECT_70 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.Number == Poker_Number_6:
                cnt += 1
        if cnt < 4:
            for i in range(0, cnt):
                pass
    if EFFECT_71 in player.effects:
        cnt = player.gold // CONDITIN_GOLD_BASE
        chip += cnt * 20
    if EFFECT_72 in player.effects:
        if random.randint(1, 6) == 1:
            mult += 4
    if EFFECT_73 in player.effects:
        pass
    if EFFECT_74 in player.effects:
        cnt = player.gold // CONDITIN_GOLD_BASE
        mag += 2 * cnt
    if EFFECT_75 in player.effects:
        if len(player.poker_play) == 1:
            card = player.poker_play[0]
            tmp = Poker()
            tmp.Color = card.Color
            tmp.Number = card.Number
            tmp.Material = card.Material
            tmp.Wax = card.Wax
            mgr.deck.Add(tmp)
    if EFFECT_76 in player.effects:
        if play_type == Score_Name_Straight:
            for card in player.poker_scored:
                if card.number == Poker_Number_A:
                    pass
                    break
    if EFFECT_77 in player.effects:
        if play_type == Score_Name_Straight_Flush:
            pass
    if EFFECT_78 in player.effects:
        if player.gold < 5 * CONDITIN_GOLD_BASE:
            pass
    if EFFECT_79 in player.effects:
        cnt = 0
        for card in mgr.get_all_pokers():
            if card.number == Poker_Number_9:
                cnt += 1
        for i in range(0, cnt):
            pass
    if EFFECT_80:
        pass
    return [chip, mag, mult]


class EffectHelper:
    @staticmethod
    def CalculateStart(_type, chip, mag, mult, player, gm):
        return chip, mag, mult

    @staticmethod
    def CalculateScoredPoker(_type, chip, mag, mult, player, gm, poker):
        return chip, mag, mult

    @staticmethod
    def CalculateUnScoredPoker(_type, chip, mag, mult, player, gm, poker):
        return chip, mag, mult

    @staticmethod
    def CalculateEnd(_type, chip, mag, mult, player, gm):
        return chip, mag, mult