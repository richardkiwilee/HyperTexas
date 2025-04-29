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
        self.change = 0        # 变更记录
        # 可见性 仅记录数字和花色. 材质和蜡封对所有人可见
        self.visible = {'number': [], 'color': []}

    def plus(self):
        if self.Number == Poker_Number_A:
            self.Number = Poker_Number_2
            self.change += 1
            return
        if self.Number == Poker_Number_2:
            self.Number = Poker_Number_3
            self.change += 1
            return
        if self.Number == Poker_Number_3:
            self.Number = Poker_Number_4
            self.change += 1
            return
        if self.Number == Poker_Number_4:
            self.Number = Poker_Number_5
            self.change += 1
            return
        if self.Number == Poker_Number_5:
            self.Number = Poker_Number_6
            self.change += 1
            return
        if self.Number == Poker_Number_6:
            self.Number = Poker_Number_7
            self.change += 1
            return
        if self.Number == Poker_Number_7:
            self.Number = Poker_Number_8
            self.change += 1
            return
        if self.Number == Poker_Number_8:
            self.Number = Poker_Number_9
            self.change += 1
            return
        if self.Number == Poker_Number_9:
            self.Number = Poker_Number_10
            self.change += 1
            return
        if self.Number == Poker_Number_10:
            self.Number = Poker_Number_J
            self.change += 1
            return
        if self.Number == Poker_Number_J:
            self.Number = Poker_Number_Q
            self.change += 1
            return
        if self.Number == Poker_Number_Q:
            self.Number = Poker_Number_K
            self.change += 1
            return
        if self.Number == Poker_Number_K:
            self.Number = Poker_Number_A
            self.change += 1
            return
        

    def from_dict(self, info: dict):
        self.id = info['id']
        self.Number = info['Number']      # 数字
        self.Color = info['Color']       # 花色
        self.Material = info['Material']    # 材质
        self.Wax = info['Wax']         # 蜡封
        self.change = info['change']
        self.visible = info['visible']

    def setVisible(self, user):
        if user not in self.visible['number']:
            self.visible['number'].append(user)
        if user not in self.visible['color']:
            self.visible['color'].append(user)

    def ResetVisible(self):
        self.visible = {'number': [], 'color': []}

    def to_dict(self):
        return {
            'id': self.id,
            'Number': self.Number,
            'Color': self.Color,
            'Material': self.Material,
            'Wax': self.Wax,
            'change': self.change,
            'visible': self.visible
        }

    @staticmethod
    def format(user, info):
        if user in info['visible']['number']:
            if info['Number'] == Poker_Number_A:
                number = 'A'
            elif info['Number'] == Poker_Number_2:
                number = '2'
            elif info['Number'] == Poker_Number_3:
                number = '3'
            elif info['Number'] == Poker_Number_4:
                number = '4'
            elif info['Number'] == Poker_Number_5:
                number = '5'
            elif info['Number'] == Poker_Number_6:
                number = '6'
            elif info['Number'] == Poker_Number_7:
                number = '7'
            elif info['Number'] == Poker_Number_8:
                number = '8'
            elif info['Number'] == Poker_Number_9:
                number = '9'
            elif info['Number'] == Poker_Number_10:
                number = '10'
            elif info['Number'] == Poker_Number_J:
                number = 'J'
            elif info['Number'] == Poker_Number_Q:
                number = 'Q'
            elif info['Number'] == Poker_Number_K:
                number = 'K'
        else:
            number = '?'
            if info['change']:
                number += f"+{info['change']}"
        if user in info['visible']['color']:
            if info['Color'] == Poker_Color_Heart:
                color = '[red]♥[/red]'
            elif info['Color'] == Poker_Color_Diamond:
                color = '[red]♦[/red]'
            elif info['Color'] == Poker_Color_Club:
                color = '[blue]♣[/blue]'
            elif info['Color'] == Poker_Color_Plum:
                color = '[blue]♠[/blue]'
        else:
            color = '?'
        if info['Material'] == Poker_Material_Universal:
            material = '<万能>'
        elif info['Material'] == Poker_Material_Gold:
            material = '<黄金>'
        elif info['Material'] == Poker_Material_Glass:
            material = '<玻璃>'
        elif info['Material'] == Poker_Material_Iron:
            material = '<钢铁>'
        elif info['Material'] == Poker_Material_Stone:
            material = '<石头>'
        elif info['Material'] == Poker_Material_Lucky:
            material = '<幸运>'
        elif info['Material'] == Poker_Material_Chip:
            material = '<筹码>'
        elif info['Material'] == Poker_Material_Magnification:
            material = '<倍率>'
        else:
            material = ''
        if info['Wax'] == Poker_Wax_Gold:
            wax = '[yellow]⚪[/yellow]'
        elif info['Wax'] == Poker_Wax_Red:
            wax = '[red]⚪[/red]'
        elif info['Wax'] == Poker_Wax_Blue:
            wax = '[blue]⚪[/blue]'
        elif info['Wax'] == Poker_Wax_Purple:
            wax = '[magenta]⚪[/magenta]'
        else:
            wax = ''
        return number + color + material + wax

    @staticmethod
    def format_slot(info):
        if info['Number'] == Poker_Number_A:
            number = 'A'
        elif info['Number'] == Poker_Number_2:
            number = '2'
        elif info['Number'] == Poker_Number_3:
            number = '3'
        elif info['Number'] == Poker_Number_4:
            number = '4'
        elif info['Number'] == Poker_Number_5:
            number = '5'
        elif info['Number'] == Poker_Number_6:
            number = '6'
        elif info['Number'] == Poker_Number_7:
            number = '7'
        elif info['Number'] == Poker_Number_8:
            number = '8'
        elif info['Number'] == Poker_Number_9:
            number = '9'
        elif info['Number'] == Poker_Number_10:
            number = '10'
        elif info['Number'] == Poker_Number_J:
            number = 'J'
        elif info['Number'] == Poker_Number_Q:
            number = 'Q'
        elif info['Number'] == Poker_Number_K:
            number = 'K'

        if info['Color'] == Poker_Color_Heart:
            color = '[red]♥[/red]'
        elif info['Color'] == Poker_Color_Diamond:
            color = '[red]♦[/red]'
        elif info['Color'] == Poker_Color_Club:
            color = '[blue]♣[/blue]'
        elif info['Color'] == Poker_Color_Plum:
            color = '[blue]♠[/blue]'

        if info['Material'] == Poker_Material_Universal:
            material = '<万能>'
        elif info['Material'] == Poker_Material_Gold:
            material = '<黄金>'
        elif info['Material'] == Poker_Material_Glass:
            material = '<玻璃>'
        elif info['Material'] == Poker_Material_Iron:
            material = '<钢铁>'
        elif info['Material'] == Poker_Material_Stone:
            material = '<石头>'
        elif info['Material'] == Poker_Material_Lucky:
            material = '<幸运>'
        elif info['Material'] == Poker_Material_Chip:
            material = '<筹码>'
        elif info['Material'] == Poker_Material_Magnification:
            material = '<倍率>'
        else:
            material = ''

        if info['Wax'] == Poker_Wax_Gold:
            wax = '[yellow]⚪[/yellow]'
        elif info['Wax'] == Poker_Wax_Red:
            wax = '[red]⚪[/red]'
        elif info['Wax'] == Poker_Wax_Blue:
            wax = '[blue]⚪[/blue]'
        elif info['Wax'] == Poker_Wax_Purple:
            wax = '[magenta]⚪[/magenta]'
        else:
            wax = ''
        return f'{color}{material}\n{number}{wax}'
