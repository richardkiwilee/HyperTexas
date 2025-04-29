#encoding=utf-8
import imp
from rich.table import Table
from rich.console import Console
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.box import SQUARE, DOUBLE_EDGE, Box, HEAVY_HEAD, HORIZONTALS
from rich import box
from rich.columns import Columns
from rich.padding import Padding
from rich.text import Text
import os
try:
    from HyperTexas.game.game_enum import GameStatus
    from HyperTexas.game.poker import Poker
    from HyperTexas.game.card import *
except:
    from game_enum import GameStatus
    from poker import Poker
    from card import *

test_dict = {'game_status': 'game', 'current_player_index': 0, 'players': [{'username': 'host', 'chip': 300000, 'pokers': [{'id': 2, 'Number': 'Number_A', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': ['host'], 'color': ['host']}}, {'id': 14, 'Number': 'Number_4', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': ['host'], 'color': ['host']}}], 'hand_cards': [{'id': 65, 'name': '信用卡', 'desc': '计分结束后, 获得本轮损失的资金', 'visible': ['host']}, {'id': 24, 'name': '天王星', 'desc': '升级两对牌型1级', 'visible': ['host']}, {'id': 43, 'name': '占卜', 'desc': '将手牌转换为同一点数', 'visible': ['host']}], 'effects': [], 'skill': None}, {'username': 'player1', 'chip': 300000, 'pokers': [{'id': 43, 'Number': 'Number_J', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': ['player1'], 'color': ['player1']}}, {'id': 24, 'Number': 'Number_6', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': ['player1'], 'color': ['player1']}}], 'hand_cards': [{'id': 11, 'name': '命运之轮', 'desc': '1/4概率给予+50筹码, +10倍率, x1.5倍率', 'visible': ['player1']}, {'id': 80, 'name': '迷幻药', 'desc': '所有玩家的效果重新分配, 个数不变', 'visible': ['player1']}, {'id': 89, 'name': '噩运的护身符', 'desc': '回合开始时支付1w资金, 使用这张卡会将这张卡送到一名随机其他玩家手牌中', 'visible': ['player1']}], 'effects': [], 'skill': None}], 'public_cards': [], 'last_used_cards': [], 'deck': [{'id': 18, 'Number': 'Number_5', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 1, 'Number': 'Number_A', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 4, 'Number': 'Number_A', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 36, 'Number': 'Number_9', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 35, 'Number': 'Number_9', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 39, 'Number': 'Number_10', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 38, 'Number': 'Number_10', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 3, 'Number': 'Number_A', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 13, 'Number': 'Number_4', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 34, 'Number': 'Number_9', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 12, 'Number': 'Number_3', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 16, 'Number': 'Number_4', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 23, 'Number': 'Number_6', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 50, 'Number': 'Number_K', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 51, 'Number': 'Number_K', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 41, 'Number': 'Number_J', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 28, 'Number': 'Number_7', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 32, 'Number': 'Number_8', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 37, 'Number': 'Number_10', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 17, 'Number': 'Number_5', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 11, 'Number': 'Number_3', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 25, 'Number': 'Number_7', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 29, 'Number': 'Number_8', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 33, 'Number': 'Number_9', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 47, 'Number': 'Number_Q', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 30, 'Number': 'Number_8', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 31, 'Number': 'Number_8', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 9, 'Number': 'Number_3', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 10, 'Number': 'Number_3', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 8, 'Number': 'Number_2', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 49, 'Number': 'Number_K', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 48, 'Number': 'Number_Q', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 7, 'Number': 'Number_2', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 20, 'Number': 'Number_5', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 45, 'Number': 'Number_Q', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 5, 'Number': 'Number_2', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 21, 'Number': 'Number_6', 'Color': 'Color_Heart', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 26, 'Number': 'Number_7', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 40, 'Number': 'Number_10', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 6, 'Number': 'Number_2', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 27, 'Number': 'Number_7', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 46, 'Number': 'Number_Q', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 22, 'Number': 'Number_6', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 19, 'Number': 'Number_5', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 52, 'Number': 'Number_K', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 15, 'Number': 'Number_4', 'Color': 'Color_Club', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 42, 'Number': 'Number_J', 'Color': 'Color_Diamond', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}, {'id': 44, 'Number': 'Number_J', 'Color': 'Color_Plum', 'Material': None, 'Wax': None, 'change': 0, 'visible': {'number': [], 'color': []}}]}

lobby_dict = {'game_status': 'lobby',
              'ready_status': {'player1': True, 'player2': False}
              }

def create_card_slot(index: int, card_info: dict = None) -> Panel:
    if card_info and 'Number' in card_info:
        content = Poker.format_slot(card_info)
        box_style = box.SQUARE
    else:
        content = "   "
        box_style = box.DOUBLE_EDGE
    return Panel(content, title=f"", box=box_style, width=8, height=5)

def format_poker_card(player_name: str, card: dict, index: int) -> str:
    return f"\[{chr(96+index)}] {Poker.format(player_name, card)}"

def format_hand_card(player_name: str, card: dict, index: int) -> str:
    return f"\[{chr(96+index)}] {Card.format(player_name, card)}"

def create_player_table(myname, players: list, info: dict) -> Table:
    table = Table(box=box.HORIZONTALS, show_header=True, header_style="bold", show_edge=True, padding=(0,1))
    table.add_column("编号", justify="center", no_wrap=True)
    table.add_column("", justify="center", no_wrap=True)
    table.add_column("名字")
    table.add_column("技能")
    table.add_column("分数", justify="right")
    table.add_column("底牌")
    table.add_column("手牌")

    current_player_index = info.get('current_player_index', 0)
    
    for i, player in enumerate(players):
        # 格式化底牌列表
        poker_cards = []
        _index = 1
        for card in player['pokers']:
            poker_cards.append(format_poker_card(myname, card, _index))
            _index += 1
        poker_text = "\n".join(poker_cards) if poker_cards else ""

        # 格式化手牌列表
        hand_cards = []
        for card in player['hand_cards']:
            hand_cards.append(format_hand_card(myname, card, _index))
            _index += 1
        hand_text = "\n".join(hand_cards) if hand_cards else ""

        # 格式化技能
        skill = player.get('skill', '')

        # 添加当前玩家指示器
        current_player_indicator = "[yellow]►[/yellow]" if i == current_player_index else ""

        table.add_row(
            str(i + 1),
            current_player_indicator,
            player['username'],
            skill or "",
            str(player.get('chip', 0)),
            poker_text,
            hand_text
        )
    
    return table

def create_public_cards_area(info: dict) -> Group:
    # 创建公共牌槽
    card_slots = []
    for i in range(5):
        card_info = info['public_cards'][i] if i < len(info['public_cards']) else None
        card_slots.append(create_card_slot(i + 1, card_info))
    
    # 创建编号
    slot_numbers = []
    for i in range(5):
        # TODO: 不够优雅
        slot_numbers.append(Text(f"  [{chr(96+i+1)}]   ", justify="center"))
    
    # 创建紧密排列的卡槽组和编号组
    card_slots_row = Columns(card_slots, equal=True, expand=False, padding=(0, 1))
    slot_numbers_row = Columns(slot_numbers, equal=True, expand=False, padding=(0, 1))
    
    return Group(card_slots_row, slot_numbers_row)

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

        public_cards_area = create_public_cards_area(info)
        centered_public_cards = Padding(public_cards_area, (1, 30))
        layout["top"].update(centered_public_cards)

        # 创建玩家表格
        player_table = create_player_table(myname, info['players'], info)

        # 创建卡组和使用记录面板
        deck_panel = format_card_list(myname, info['deck'], "抽牌堆顶部")
        used_panel = format_card_list(myname, info['last_used_cards'], "最近使用的卡")
        
        # 创建游戏记录
        log_panel = Panel("\n".join(info['game_log']), title="游戏记录", box=box.SQUARE)

        # 渲染布局
        layout["left"].update(player_table)
        layout["deck_area"].update(Padding(deck_panel, (0, 1)))
        layout["used_area"].update(Padding(used_panel, (0, 1)))
        layout["right_bottom"].update(log_panel)

        console.print(layout)
    elif info['game_status'] == GameStatus.LOBBY.value:
        # 创建大厅表格
        table = Table(title="游戏大厅")
        
        # 添加列
        table.add_column("玩家编号", justify="center")
        table.add_column("玩家名字")
        table.add_column("准备状态", justify="center")
        
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
