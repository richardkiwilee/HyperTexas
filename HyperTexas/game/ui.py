import imp
from rich.table import Table
from rich.console import Console
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.box import SQUARE, DOUBLE_EDGE, Box
from rich import box
from rich.columns import Columns
from rich.padding import Padding
import os
try:
    from HyperTexas.game.game_enum import GameStatus
    from HyperTexas.game.poker import Poker
except:
    from game_enum import GameStatus
    from poker import Poker

test_dict = {'game_status': 'game', 'current_player_index': 0, 
            'players': [
                {'username': 'host', 'chip': 300000, 'pokers': [], 
                'hand_cards': [
                    {'id': 25, 'Number': 'Number_7', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 
                    'visible': {'number': ['host'], 'color': ['host']}}, 
                    {'id': 12, 'Number': 'Number_3', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0,
                     'visible': {'number': ['host'], 'color': ['host']}}
                     ], 
                     'effects': [], 'skill': None}, 
                     {'username': 'player1', 'chip': 300000, 'pokers': [], 
                     'hand_cards': [
                        {'id': 13, 'Number': 'Number_4', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 
                        'change': 0, 'visible': {'number': ['player1'], 'color': ['player1']}}, 
                        {'id': 26, 'Number': 'Number_7', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 
                        'change': 0, 'visible': {'number': ['player1'], 'color': ['player1']}}
                        ], 
                        'effects': [], 'skill': None}], 
                        'public_cards': [], 'last_used_cards': [], 
                        'deck': [{'id': 11, 'Number': 'Number_3', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 10, 'Number': 'Number_3', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 7, 'Number': 'Number_2', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 16, 'Number': 'Number_4', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 35, 'Number': 'Number_9', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 1, 'Number': 'Number_A', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 32, 'Number': 'Number_8', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 24, 'Number': 'Number_6', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 15, 'Number': 'Number_4', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 6, 'Number': 'Number_2', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 33, 'Number': 'Number_9', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 42, 'Number': 'Number_J', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 34, 'Number': 'Number_9', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 31, 'Number': 'Number_8', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 39, 'Number': 'Number_10', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 47, 'Number': 'Number_Q', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 36, 'Number': 'Number_9', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 51, 'Number': 'Number_K', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 38, 'Number': 'Number_10', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 45, 'Number': 'Number_Q', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 44, 'Number': 'Number_J', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 18, 'Number': 'Number_5', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 40, 'Number': 'Number_10', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 21, 'Number': 'Number_6', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 9, 'Number': 'Number_3', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 20, 'Number': 'Number_5', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 22, 'Number': 'Number_6', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 52, 'Number': 'Number_K', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 8, 'Number': 'Number_2', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 17, 'Number': 'Number_5', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 5, 'Number': 'Number_2', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 28, 'Number': 'Number_7', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 4, 'Number': 'Number_A', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 49, 'Number': 'Number_K', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 46, 'Number': 'Number_Q', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 14, 'Number': 'Number_4', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 3, 'Number': 'Number_A', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 41, 'Number': 'Number_J', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 48, 'Number': 'Number_Q', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 29, 'Number': 'Number_8', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 23, 'Number': 'Number_6', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 30, 'Number': 'Number_8', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 43, 'Number': 'Number_J', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 50, 'Number': 'Number_K', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 2, 'Number': 'Number_A', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 27, 'Number': 'Number_7', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 19, 'Number': 'Number_5', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 37, 'Number': 'Number_10', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}]}

lobby_dict = {'game_status': 'lobby',
              'ready_status': {'player1': True, 'player2': False}
              }

def create_card_slot(index: int, card_info: dict = None) -> Panel:
    if card_info and 'Number' in card_info:
        color_map = {1: '', 2: '', 3: '', 4: ''}
        number_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        color = color_map.get(card_info['Color'], '?')
        number = number_map.get(card_info['Number'], str(card_info['Number']))
        content = f"{color} {number}"
        box_style = box.SQUARE
    else:
        content = "   "
        box_style = box.DOUBLE_EDGE
    return Panel(content, title=f"", box=box_style, width=8, height=5)

def format_poker_card(player_name: str, card: dict, index: int) -> str:
    return f"[{index}] {Poker.format(player_name, card)}"

def create_player_table(myname, players: list) -> Table:
    table = Table(show_header=True, box=box.SIMPLE_HEAVY)
    table.add_column("编号", justify="center", style="cyan", no_wrap=True)
    table.add_column("名字", style="magenta")
    table.add_column("分数", justify="right", style="green")
    table.add_column("手牌", style="yellow", width=15)
    table.add_column("技能", style="blue", width=15)
    
    # 添加行分隔符
    table.show_lines = True
    
    for i, player in enumerate(players):
        # 格式化玩家编号
        player_id = f"P{i + 1}"
        
        # 格式化手牌列表
        poker_cards = []
        # 显示手牌
        for j, card in enumerate(player['hand_cards']):
            poker_cards.append(format_poker_card(myname, card, j + 1))
        # 显示场上的牌
        for j, card in enumerate(player['pokers'], start=len(player['hand_cards'])):
            poker_cards.append(format_poker_card(myname, card, j + 1))
        poker_text = "\n".join(poker_cards)
        print(poker_text)
        # 格式化技能卡
        # 假设每个玩家有2张扑克牌，所以技能卡的索引从3开始
        skill_cards = []
        if isinstance(player['skill'], (list, tuple)):
            for j, skill in enumerate(player['skill']):
                skill_cards.append(f"[{j + len(player['pokers']) + len(player['hand_cards']) + 1}] {skill}")
        else:
            skill_cards.append(f"[{len(player['pokers']) + len(player['hand_cards']) + 1}] {player['skill']}")
        skill_text = "\n".join(skill_cards)
        
        table.add_row(
            player_id,
            player['username'],
            str(player['chip']),
            poker_text,
            skill_text
        )
    
    return table

def format_card_list(myname, cards: list, title: str, max_items: int = 3) -> Panel:
    formatted_cards = []
    for i, card in enumerate(cards[:max_items]):
        if 'player' in card:  # 用于显示最后使用的卡
            color_map = {1: '', 2: '', 3: '', 4: ''}
            number_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
            color = color_map.get(card['Color'], '?')
            number = number_map.get(card['Number'], str(card['Number']))
            formatted_cards.append(f"{color}{number} by {card['player']}")
        else:  # 用于显示抽牌堆
            color_map = {1: '', 2: '', 3: '', 4: ''}
            number_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
            color = color_map.get(card['Color'], '?')
            number = number_map.get(card['Number'], str(card['Number']))
            formatted_cards.append(Poker.format(myname, card))
    
    # 如果卡片数量不足，用空行填充
    while len(formatted_cards) < max_items:
        formatted_cards.append("---")
    
    return Panel("\n".join(formatted_cards), title=title, width=20, box=box.SQUARE)

def RefreshScreen(myname, info: dict):
    _ = os.system('cls')
    console = Console()
    console.clear()
    console.width = 120
    console.height = 40
    if 'game_log' not in info.keys():
        info['game_log'] = []
    if info['game_status'] == GameStatus.GAME.value:
        # 创建主布局：上下分割
        layout = Layout()
        layout.split(
            Layout(name="top", size=10),
            Layout(name="bottom")
        )
        
        # 底部分为左右两部分
        layout["bottom"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        # 右侧继续分为上下两部分
        layout["right"].split(
            Layout(name="right_top", size=10),
            Layout(name="right_bottom")
        )
        
        # 右上部分继续分为左右
        layout["right_top"].split_row(
            Layout(name="deck_area"),
            Layout(name="used_area")
        )

        # 创建公共牌槽
        card_slots_list = []
        for i in range(5):
            card_info = info['public_cards'][i] if i < len(info['public_cards']) else None
            card_slots_list.append(create_card_slot(i + 1, card_info))
        
        # 创建卡组和使用记录面板
        deck_panel = format_card_list(myname, info['deck'], "抽牌堆顶部")
        used_panel = format_card_list(myname, info['last_used_cards'], "最近使用的卡")
        
        # 创建玩家表格
        player_table = create_player_table(myname, info['players'])

        # 创建游戏记录
        log_panel = Panel("\n".join(info['game_log']), title="游戏记录", box=box.SQUARE)

        # 创建紧密排列的卡槽组
        card_slots_columns = Columns(
            card_slots_list,
            equal=True,
            expand=False,
            padding=(0, 1)  # 垂直padding为0，水平padding为1
        )
        
        # 添加水平居中的padding
        centered_card_slots = Padding(card_slots_columns, (1, 30))  # 上下padding为1，左右padding为30

        # 渲染布局
        layout["top"].update(centered_card_slots)
        layout["left"].update(player_table)
        layout["deck_area"].update(Padding(deck_panel, (0, 1)))
        layout["used_area"].update(Padding(used_panel, (0, 1)))
        layout["right_bottom"].update(log_panel)

        console.print(layout)
    elif info['game_status'] == GameStatus.LOBBY.value:
        # 创建大厅表格
        table = Table(title="游戏大厅")
        
        # 添加列
        table.add_column("玩家编号", justify="center", style="cyan")
        table.add_column("玩家名字", style="magenta")
        table.add_column("准备状态", justify="center", style="green")
        
        # 添加玩家数据
        for idx, (player_name, ready_status) in enumerate(info.get('ready_status', {}).items(), start=1):
            status_symbol = "✓" if ready_status else "✗"
            table.add_row(str(idx), player_name, status_symbol)
        
        # 打印表格
        console = Console()
        console.print("\n")  # 添加一些空行使显示更美观
        console.print(table)
        console.print("\n游戏指令:")
        console.print("- ready: 准备开始游戏")
        console.print("- cancel: 取消准备")
        console.print("- start: 开始游戏（仅房主可用）")
        console.print("- exit: 退出游戏")
    elif info['game_status'] == GameStatus.SCORE.value:
        pass

if __name__ == '__main__':
    RefreshScreen('player1', test_dict)
