from typing import TYPE_CHECKING, Any, Optional, List, Dict, Set

if TYPE_CHECKING:
    from HyperTexas.game.manager import Manager

CARD_DICT: Dict[int, 'Card'] = dict()


class Card:
    def __init__(self, enabled: bool, id: int, name: str, desc: str = '') -> None:
        self.enabled = enabled
        self.id = id
        self.name = name
        self.desc = desc
        self.visible = []

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

    def setVisible(self, user):
        try:
            if user.username not in self.visible:
                self.visible.append(user.username)
        except:
            if user not in self.visible:
                self.visible.append(user)

    def ResetVisible(self):
        self.visible = []

    def from_dict(self, d: dict):
        self.enabled = 1
        self.id = d.get('id')
        self.name = d.get('name')
        self.desc = d.get('desc')
        self.visible = d.get('visible')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'visible': self.visible
        }

    @staticmethod
    def format(user, info):
        if user in info['visible']:
            return info['name']
        return '?'


class Card_1(Card):
    def __init__(self) -> None:
        super().__init__(0, 1, '愚者', '生成最后被使用的卡, 这张除外')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        for _id in mgr.last_used_cards:
            if _id != 1:
                break
        _card = CARD_DICT[f'Card_{_id}']
        current_player_index = mgr.current_player_index
        mgr.players[current_player_index].hand_cards.append(_card.id)


class Card_2(Card):
    def __init__(self) -> None:
        super().__init__(1, 2, '魔术师', '增强2张手牌为幸运卡[1/5概率+20倍率]')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_3(Card):
    def __init__(self) -> None:
        super().__init__(1, 3, '女祭司', '随机提升2个牌型各1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_4(Card):
    def __init__(self) -> None:
        super().__init__(1, 4, '皇后', '增强2张手牌为+4倍率卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_5(Card):
    def __init__(self) -> None:
        super().__init__(0, 5, '皇帝', '生成两张技能卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_6(Card):
    def __init__(self) -> None:
        super().__init__(1, 6, '教皇', '增强2张手牌为+30筹码卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_7(Card):
    def __init__(self) -> None:
        super().__init__(0, 7, '恋人', '增强1张手牌为万能卡[视为任何花色]')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_8(Card):
    def __init__(self) -> None:
        super().__init__(0, 8, '恋人', '增强1张手牌为钢铁卡[未计分时给予x1.5倍率]')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_9(Card):
    def __init__(self) -> None:
        super().__init__(1, 9, '正义', '增强1张手牌为玻璃卡[x2倍率, 1/4概率计分后摧毁]')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_10(Card):
    def __init__(self) -> None:
        super().__init__(0, 10, '隐者', '获得2w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_11(Card):
    def __init__(self) -> None:
        super().__init__(0, 11, '命运之轮', '1/4概率给予+50筹码, +10倍率, x1.5倍率')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_12(Card):
    def __init__(self) -> None:
        super().__init__(0, 12, '力量', '选定2张卡片, 使其点数+1')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_13(Card):
    def __init__(self) -> None:
        super().__init__(0, 13, '倒吊人', '摧毁至多2张卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_14(Card):
    def __init__(self) -> None:
        super().__init__(0, 14, '死神', '选定2张卡, 将一张变为另一张')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_15(Card):
    def __init__(self) -> None:
        super().__init__(0, 15, '节制', '1/5概率获得5w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_16(Card):
    def __init__(self) -> None:
        super().__init__(0, 16, '恶魔', '增强1张手牌为黄金卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_17(Card):
    def __init__(self) -> None:
        super().__init__(0, 17, '塔', '增强1张手牌为石头牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_18(Card):
    def __init__(self) -> None:
        super().__init__(0, 18, '星星', '将至多3张卡牌转换为方块')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_19(Card):
    def __init__(self) -> None:
        super().__init__(0, 19, '月亮', '将至多3张卡牌转换为梅花')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_20(Card):
    def __init__(self) -> None:
        super().__init__(0, 20, '太阳', '将至多3张卡牌转换为红桃')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass


class Card_21(Card):
    def __init__(self) -> None:
        super().__init__(0, 21, '世界', '将至多3张卡牌转换为黑桃')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_22(Card):
    def __init__(self) -> None:
        super().__init__(0, 22, '摩诃', '生成一个随机效果')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_23(Card):
    def __init__(self) -> None:
        super().__init__(0, 23, '水星', '升级对子牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_24(Card):
    def __init__(self) -> None:
        super().__init__(0, 24, '天王星', '升级两对牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_25(Card):
    def __init__(self) -> None:
        super().__init__(0, 25, '金星', '升级三条牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_26(Card):
    def __init__(self) -> None:
        super().__init__(0, 26, '海王星', '升级同花顺牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_27(Card):
    def __init__(self) -> None:
        super().__init__(0, 27, '地球', '升级葫芦牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_28(Card):
    def __init__(self) -> None:
        super().__init__(0, 28, '冥王星', '升级高牌牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_29(Card):
    def __init__(self) -> None:
        super().__init__(0, 29, '火星', '升级四条牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_30(Card):
    def __init__(self) -> None:
        super().__init__(0, 30, 'X行星', '升级五条牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_31(Card):
    def __init__(self) -> None:
        super().__init__(0, 31, '木星', '升级同花牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_32(Card):
    def __init__(self) -> None:
        super().__init__(0, 32, '谷神星', '升级同花葫芦牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_33(Card):
    def __init__(self) -> None:
        super().__init__(0, 33, '土星', '升级顺子牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_34(Card):
    def __init__(self) -> None:
        super().__init__(0, 34, '阋神星', '升级同花五条牌型1级')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_35(Card):
    def __init__(self) -> None:
        super().__init__(0, 35, '使魔', '随机摧毁1张手牌, 增加3张增强的人头牌到手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_36(Card):
    def __init__(self) -> None:
        super().__init__(0, 36, '严峻', '随机摧毁1张手牌, 增加2张增强的A到手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_37(Card):
    def __init__(self) -> None:
        super().__init__(0, 37, '咒语', '随机摧毁1张手牌, 增加4张增强的数字牌到手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_38(Card):
    def __init__(self) -> None:
        super().__init__(0, 38, '护身符', '选定一张牌, 添加金色蜡封')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_39(Card):
    def __init__(self) -> None:
        super().__init__(0, 39, '既视感', '选定一张牌, 添加红色蜡封')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_40(Card):
    def __init__(self) -> None:
        super().__init__(0, 40, '入迷', '选定一张牌, 添加蓝色蜡封')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_41(Card):
    def __init__(self) -> None:
        super().__init__(0, 41, '灵媒', '选定一张牌, 添加紫色蜡封')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_42(Card):
    def __init__(self) -> None:
        super().__init__(0, 42, '符印', '将手牌转换为同一花色')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_43(Card):
    def __init__(self) -> None:
        super().__init__(0, 43, '占卜', '将手牌转换为同一点数')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_44(Card):
    def __init__(self) -> None:
        super().__init__(0, 44, '火祭', '摧毁牌库5张牌, 获得2w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_45(Card):
    def __init__(self) -> None:
        super().__init__(0, 45, '生命', '随机复制一个效果, 摧毁其他所有效果')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_46(Card):
    def __init__(self) -> None:
        super().__init__(0, 46, '神秘', '选定1张手牌, 生成2张它的复制')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_47(Card):
    def __init__(self) -> None:
        super().__init__(0, 47, '妖法', '为随机一张手牌添加一个蜡封')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_48(Card):
    def __init__(self) -> None:
        super().__init__(0, 48, '偷窥', '查看指定2张卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_49(Card):
    def __init__(self) -> None:
        super().__init__(0, 49, '观星', '查看抽牌堆顶部的3张卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_50(Card):
    def __init__(self) -> None:
        super().__init__(0, 50, '偷渡', '将一张卡与自己的一张卡互换')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_51(Card):
    def __init__(self) -> None:
        super().__init__(0, 51, '智慧', '抽2张卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_52(Card):
    def __init__(self) -> None:
        super().__init__(0, 52, '勒索', '减少指定玩家1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_53(Card):
    def __init__(self) -> None:
        super().__init__(0, 53, '大扫除', '获得1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_54(Card):
    def __init__(self) -> None:
        super().__init__(0, 54, '迁怒于人', '失去筹码时, 除你以外拥有最多筹码的玩家失去相同的筹码')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_55(Card):
    def __init__(self) -> None:
        super().__init__(0, 55, '报酬金保险', '抵消失去筹码的效果')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_56(Card):
    def __init__(self) -> None:
        super().__init__(0, 56, '回款', '如果资金低于初始资金, 补齐到初始资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_57(Card):
    def __init__(self) -> None:
        super().__init__(0, 57, '买入', '如果破产, 恢复初始资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_58(Card):
    def __init__(self) -> None:
        super().__init__(0, 58, '大小姐的特权', '丢弃所有手牌, 抽3张牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_59(Card):
    def __init__(self) -> None:
        super().__init__(0, 59, '传统', '立刻进入出牌阶段')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_60(Card):
    def __init__(self) -> None:
        super().__init__(0, 60, '学生会长的特权', '本轮使用卡牌无需消耗资金, 你可以再使用一张技能卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_61(Card):
    def __init__(self) -> None:
        super().__init__(0, 61, '宝物小偷', '从指定玩家手里偷取1张卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_62(Card):
    def __init__(self) -> None:
        super().__init__(0, 62, '老实', '下一回合, 所有人无法使用卡牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_63(Card):
    def __init__(self) -> None:
        super().__init__(0, 63, '无人生还', '支付所有玩家1k资金, 结束此轮')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_64(Card):
    def __init__(self) -> None:
        super().__init__(0, 64, '狐假虎威', '本轮无法出牌, 计分视为场上最高资金与自己资金的差')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_65(Card):
    def __init__(self) -> None:
        super().__init__(0, 65, '信用卡', '计分结束后, 获得本轮损失的资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_66(Card):
    def __init__(self) -> None:
        super().__init__(0, 66, '豪赌', '无法出牌, 视为打出5张A或2')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_67(Card):
    def __init__(self) -> None:
        super().__init__(0, 67, '加注', '如果此轮获胜, 夺取的资金增加50%')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_68(Card):
    def __init__(self) -> None:
        super().__init__(0, 68, '纯洁', '移除所有的效果')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_69(Card):
    def __init__(self) -> None:
        super().__init__(0, 69, '破坏', '丢弃指定玩家1张手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_70(Card):
    def __init__(self) -> None:
        super().__init__(0, 70, '万箭齐发', '丢弃所有其他玩家1张手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_71(Card):
    def __init__(self) -> None:
        super().__init__(0, 71, '保护费', '减少所有其他玩家1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_72(Card):
    def __init__(self) -> None:
        super().__init__(0, 72, '和平', '跳过其他玩家的下一回合')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_73(Card):
    def __init__(self) -> None:
        super().__init__(0, 73, '礼物交换', '与指定玩家交换手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_74(Card):
    def __init__(self) -> None:
        super().__init__(0, 74, '火焰战车', '指定玩家支付5w资金, 如果他有技能卡, 改为丢弃所有技能卡')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_75(Card):
    def __init__(self) -> None:
        super().__init__(0, 75, '甜点大作战', '反转所有玩家的手牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_76(Card):
    def __init__(self) -> None:
        super().__init__(0, 76, '强买强卖', '丢弃所有手牌, 每张丢弃的手牌获得1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_77(Card):
    def __init__(self) -> None:
        super().__init__(0, 77, '电信诈骗', '随机玩家损失2w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_78(Card):
    def __init__(self) -> None:
        super().__init__(0, 78, '断网', '所有玩家无法使用卡牌')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_79(Card):
    def __init__(self) -> None:
        super().__init__(0, 79, '圣诞大争夺', '所有玩家的手牌重新分配, 张数不变')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_80(Card):
    def __init__(self) -> None:
        super().__init__(0, 80, '迷幻药', '所有玩家的效果重新分配, 个数不变')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_81(Card):
    def __init__(self) -> None:
        super().__init__(0, 81, '红包', '所有角色获得5w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_82(Card):
    def __init__(self) -> None:
        super().__init__(0, 82, '店长的游戏', '发牌员参与出牌, 目标计分为1w')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_83(Card):
    def __init__(self) -> None:
        super().__init__(0, 83, '着急下班', '所有玩家的资金变成5w')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_84(Card):
    def __init__(self) -> None:
        super().__init__(0, 84, '恐怖的推销', '除你以外的玩家抽牌到手牌上限, 每张抽牌支付1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_85(Card):
    def __init__(self) -> None:
        super().__init__(0, 85, '诸神的游戏', '从其他玩家手里随机发动一张技能卡, 无需支付资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_86(Card):
    def __init__(self) -> None:
        super().__init__(0, 86, '清洗', '所有玩家手牌送回牌堆')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_87(Card):
    def __init__(self) -> None:
        super().__init__(0, 87, '空中餐厅·纯洁', '丢弃场上的所有效果, 每损失一个效果, 玩家支付1w资金')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_88(Card):
    def __init__(self) -> None:
        super().__init__(0, 88, '无害', '本轮所有玩家计分为0')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_89(Card):
    def __init__(self) -> None:
        super().__init__(0, 89, '噩运的护身符', '回合开始时支付1w资金, 使用这张卡会将这张卡送到一名随机其他玩家手牌中')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_90(Card):
    def __init__(self) -> None:
        super().__init__(0, 90, '强运的护身符', '持有这张卡时, 抽到的牌会尽可能变成A~7')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_91(Card):
    def __init__(self) -> None:
        super().__init__(0, 91, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_92(Card):
    def __init__(self) -> None:
        super().__init__(0, 92, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_93(Card):
    def __init__(self) -> None:
        super().__init__(0, 93, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_94(Card):
    def __init__(self) -> None:
        super().__init__(0, 94, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_95(Card):
    def __init__(self) -> None:
        super().__init__(0, 95, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_96(Card):
    def __init__(self) -> None:
        super().__init__(0, 96, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_97(Card):
    def __init__(self) -> None:
        super().__init__(0, 97, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_98(Card):
    def __init__(self) -> None:
        super().__init__(0, 98, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_99(Card):
    def __init__(self) -> None:
        super().__init__(0, 99, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass

class Card_100(Card):
    def __init__(self) -> None:
        super().__init__(0, 100, '', '')

    @staticmethod
    def call(mgr: 'Manager', arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any) -> None:
        pass
