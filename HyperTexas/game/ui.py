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
from HyperTexas.game.enum import GameStatus

test_dict = {'game_status':'playing',
            'current_player_index': 0,
            'players': [{'name': 'Player 1', 'chip': 1000, 'pokers': [{'id': 1, 'Number': 13, 'Color': 1}, {'id': 2, 'Number': 12, 'Color': 2}], 
                        'hand_cards': [0x01], 'effects': [0x01], 'skill': "快速行动"}, 
                        {'name': 'Player 2', 'chip': 2000, 'pokers': [{'id': 3, 'Number': 11, 'Color': 3}, {'id': 4, 'Number': 10, 'Color': 4}], 
                        'hand_cards': [0x02], 'effects': [0x02], 'skill': "防御姿态"}],
            'public_cards': [{'id': 5, 'Number': 1, 'Color': 1}, {'id': 6, 'Number': 2, 'Color': 2}],
            'last_used_cards': [
                {'id': 7, 'Number': 7, 'Color': 1, 'player': 'Player 1'},
                {'id': 8, 'Number': 8, 'Color': 2, 'player': 'Player 2'},
                {'id': 9, 'Number': 9, 'Color': 3, 'player': 'Player 1'}
            ],
            'deck': [
                {'id': 10, 'Number': 3, 'Color': 1},
                {'id': 11, 'Number': 4, 'Color': 2},
                {'id': 12, 'Number': 5, 'Color': 3}
            ],
            'game_log': ['Player 1 使用了 红桃K', 'Player 2 使用了 方块Q']
}

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

def format_poker_card(card: dict, index: int) -> str:
    color_map = {1: '', 2: '', 3: '', 4: ''}
    number_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    color = color_map.get(card['Color'], '?')
    number = number_map.get(card['Number'], str(card['Number']))
    return f"[{index}] {color}{number}"

def create_player_table(players: list) -> Table:
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
        for j, card in enumerate(player['pokers']):
            poker_cards.append(format_poker_card(card, j + 1))
        poker_text = "\n".join(poker_cards)
        
        # 格式化技能卡
        # 假设每个玩家有2张扑克牌，所以技能卡的索引从3开始
        skill_cards = []
        if isinstance(player['skill'], (list, tuple)):
            for j, skill in enumerate(player['skill']):
                skill_cards.append(f"[{j + len(player['pokers']) + 1}] {skill}")
        else:
            skill_cards.append(f"[{len(player['pokers']) + 1}] {player['skill']}")
        skill_text = "\n".join(skill_cards)
        
        table.add_row(
            player_id,
            player['name'],
            str(player['chip']),
            poker_text,
            skill_text
        )
    
    return table

def format_card_list(cards: list, title: str, max_items: int = 3) -> Panel:
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
            formatted_cards.append(f"{color}{number}")
    
    # 如果卡片数量不足，用空行填充
    while len(formatted_cards) < max_items:
        formatted_cards.append("---")
    
    return Panel("\n".join(formatted_cards), title=title, width=20, box=box.SQUARE)

def RefreshScreen(info: dict):
    _ = os.system('cls')
    console = Console()
    console.clear()
    console.width = 120
    console.height = 40

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
        deck_panel = format_card_list(info['deck'], "抽牌堆顶部")
        used_panel = format_card_list(info['last_used_cards'], "最近使用的卡")
        
        # 创建玩家表格
        player_table = create_player_table(info['players'])

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
    RefreshScreen(test_dict)
