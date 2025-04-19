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

test_dict = {'status':'playing',
            'current_player_index': 0,
            'players': [{'name': 'Player 1', 'chip': 1000, 'pokers': [{'id': 1, 'Number': 13, 'Color': 1}], 
                        'hand_cards': [0x01], 'effects': [0x01], 'skill': 0x01}, 
                        {'name': 'Player 2', 'chip': 2000, 'pokers': [{'id': 2, 'Number': 12, 'Color': 2}], 
                        'hand_cards': [0x02], 'effects': [0x02], 'skill': 0x02}],
            'public_cards': [{'id': 0, 'Number': 0, 'Color': 0, 'Material': 0, 'Wax': 0, 'change': [], 'visible': {'number': [], 'color': []}}],
            'last_used_cards': [{}],
            'deck': [{}],
            'game_log': ['Player 1 使用了 红桃K', 'Player 2 使用了 方块Q']
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
        # 使用DOUBLE_EDGE作为虚线边框样式
        box_style = box.DOUBLE_EDGE
    return Panel(content, title=f"槽位 {index}", box=box_style, width=8, height=5)

def create_player_table(players: list) -> Table:
    table = Table(show_header=True, box=box.SIMPLE)
    table.add_column("编号", justify="center", style="cyan")
    table.add_column("名字", style="magenta")
    table.add_column("分数", justify="right", style="green")
    table.add_column("手牌", style="yellow")
    table.add_column("技能", style="blue")
    
    for i, player in enumerate(players):
        table.add_row(
            str(i + 1),
            player['name'],
            str(player['chip']),
            str(len(player['pokers'])),
            str(player['skill'])
        )
    return table

def RefreshScreen(info: dict):
    _ = os.system('cls')
    console = Console()
    console.clear()
    console.width = 120
    console.height = 40

    if info['status'] == 'playing':
        # Create main layout
        layout = Layout()
        layout.split(
            Layout(name="top", size=10),
            Layout(name="bottom")
        )
        layout["bottom"].split_row(
            Layout(name="players", ratio=2),
            Layout(name="log", ratio=1)
        )

        # Create card slots
        card_slots_list = []
        for i in range(5):
            card_info = info['public_cards'][i] if i < len(info['public_cards']) else None
            card_slots_list.append(create_card_slot(i + 1, card_info))
        
        # Create player table
        player_table = create_player_table(info['players'])

        # Create game log
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

        # Render layout
        layout["top"].update(centered_card_slots)
        layout["players"].update(player_table)
        layout["log"].update(log_panel)

        console.print(layout)
    elif info['status'] == 'lobby':
        pass
    elif info['status'] == 'score':
        pass

if __name__ == '__main__':
    RefreshScreen(test_dict)
