Poker_Number_A = 'Number_A'
Poker_Number_2 = 'Number_2'
Poker_Number_3 = 'Number_3'
Poker_Number_4 = 'Number_4'
Poker_Number_5 = 'Number_5'
Poker_Number_6 = 'Number_6'
Poker_Number_7 = 'Number_7'
Poker_Number_8 = 'Number_8'
Poker_Number_9 = 'Number_9'
Poker_Number_10 = 'Number_10'
Poker_Number_J = 'Number_J'
Poker_Number_Q = 'Number_Q'
Poker_Number_K = 'Number_K'

Poker_Numbers = [Poker_Number_A, Poker_Number_2, Poker_Number_3, Poker_Number_4, Poker_Number_5, Poker_Number_6, Poker_Number_7, Poker_Number_8, Poker_Number_9, Poker_Number_10, Poker_Number_J, Poker_Number_Q, Poker_Number_K]

Poker_Color_Heart = 'Color_Heart'    # 红桃
Poker_Color_Diamond = 'Color_Diamond'  # 方块
Poker_Color_Club = 'Color_Club'     # 黑桃
Poker_Color_Plum = 'Color_Plum'     # 梅花

Poker_Colors = [Poker_Color_Heart, Poker_Color_Diamond, Poker_Color_Club, Poker_Color_Plum]

Poker_Material_Universal = 'Material_Universal'     # 万能
Poker_Material_Gold = 'Material_Gold'     # 黄金牌
Poker_Material_Glass = 'Material_Glass'   # 玻璃牌
Poker_Material_Iron = 'Material_Iron'     # 钢铁
Poker_Material_Stone = 'Material_Stone'   # 石头
Poker_Material_Lucky = 'Material_Lucky'   # 幸运
Poker_Material_Chip = 'Material_Chip'   # 筹码
Poker_Material_Magnification = 'Material_Magnification'   # 倍率

Poker_Wax_Gold = 'Wax_Gold'
Poker_Wax_Red = 'Wax_Red'
Poker_Wax_Blue = 'Wax_Blue'
Poker_Wax_Purple = 'Wax_Purple'

Poker_Position_Hand = 'Hand'
Poker_Position_Deck = 'Deck'
Poker_Position_Discard = 'Discard'
Poker_Position_Score = 'Score'

class Poker:
    def __init__(self):
        self.id = None
        self.Number = None      # 数字
        self.Color = None       # 花色
        self.Material = None    # 材质
        self.Wax = None         # 蜡封
    