from HyperTexas.game.character import Character
from HyperTexas.game.manager import Manager
from HyperTexas.game.effects import *

class Skill:
    def __init__(self, id, cost, name, description):
        self.id = id
        self.cost = cost
        self.name = name
        self.description = description

    @staticmethod
    def OnRoundStart(self, manager: Manager, user: Character, target: dict):
        pass

    @staticmethod
    def OnRoundEnd(self, manager: Manager, user: Character, target: dict):
        pass
    
    @staticmethod
    def OnGameStart(self, manager: Manager):
        pass

"""
SKILL_0x0207 = "轮次开始前可发动, 本轮抽到的牌为6"
SKILL_0x0208 = "轮次开始前可发动, 抽2张牌"
SKILL_0x0209 = "指定玩家支付2w资金"
SKILL_0x020a = "计分时, 平衡筹码和倍率"
SKILL_0x020b = "本轮不会损失资金"
SKILL_0x020c = "将最多3张卡变成5"
SKILL_0x020d = "指定一名玩家下回合无法使用技能卡"
SKILL_0x020e = "无法被其他玩家选定为目标"
SKILL_0x020f = "随机一名其他玩家支付1w, 发动次数为你的手牌数"

SKILL_0x0211 = "所有玩家获得2w资金"
SKILL_0x0212 = "生成2张技能卡, 本回合可再使用一张卡"
SKILL_0x0213 = "将弃牌堆的最后2张加入手牌"
SKILL_0x0214 = "免疫因效果造成的支付效果"
SKILL_0x0215 = "抽取3张技能卡, 本回合可再使用3张卡, 但需要支付双倍成本"
SKILL_0x0216 = "手牌点数翻倍"
SKILL_0x0217 = "手牌点数+2"
SKILL_0x0218 = "合计为7的点数加到随机卡牌"
SKILL_0x0219 = "如果失败, 所有其他玩家额外支付相同的资金"
SKILL_0x021a = "消耗至多10w资金, 每消耗1w资金, +100筹码, 给予x1倍率"
SKILL_0x021b = "随机一名玩家支付5w资金"
SKILL_0x021c = "所有玩家抽牌到手牌上限, 获得抽牌总数*1w的资金"
SKILL_0x021d = "所有其他玩家的手牌变成2"
SKILL_0x021e = "除你以外的玩家抽一张牌然后弃一张牌, 再反转手牌"
SKILL_0x021f = "底注+1k"

SKILL_0x0221 = "底注+2k"
SKILL_0x0222 = "底注+5k"
SKILL_0x0223 = "底注+1w"
SKILL_0x0224 = "仅在公共牌为4张时可用,选择一张牌, 如果可能, 它将是第5张公共牌"
"""