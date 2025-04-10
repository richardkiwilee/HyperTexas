import random
import base64
import os
import json
from enum import Enum
from rich.table import Table
from rich.console import Console
import cabo.protocol.service_pb2 as pb2
NUMBER_peek = [7, 8]
NUMBER_SPY = [9, 10]
NUMBER_SWITCH = [11, 12]

_DEBUG = False


class MainAction(Enum):
    SYSTEM = 0
    DRAW = 1
    DRAW_DISCARD = 2
    CABO = 3
    READY = 4
    SYNC = 5


class SubAction(Enum):
    DISCARD = 1
    CHANGE = 2      # 与自己交换
    peek = 3
    SPY = 4
    SWITCH = 5      # 发动卡片效果与别人交换


class SCORE(Enum):
    LOSE = 0
    WIN = 1
    SOMEONE_KAMIKAZE = 2


COLOR_ORDER = ['red', 'green', 'blue', 'yellow', 'megenta', 'cyan']


def create_seed(players=4):
    deck = [0, 0, 13, 13,
            1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
            5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
            9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12]
    if 4 < players <= 8:
        deck = deck * 2
    random.shuffle(deck)
    if _DEBUG:
        deck = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    _ = ''.join(['%02d' % i for i in deck])
    return base64.b64encode(_.encode('utf-8'))


class PlayerTurnOrder:
    def __init__(self):
        self.turnorder = []
        self.index = 0

    def setCurrent(self, player):
        self.index = self.turnorder.index(player)
    def AddPlayer(self, player):
        self.turnorder.append(player)

    def RemovePlayer(self, player):
        self.turnorder.remove(player)

    def shuffle(self):
        random.shuffle(self.turnorder)
        self.index = 0
        return [player for player in self.turnorder]

    def next(self) -> str:
        if self.index + 1 >= len(self.turnorder):
            self.index = 0
        else:
            self.index += 1
        return self.turnorder[self.index]

    def current(self) -> str:
        return self.turnorder[self.index]


class Card:
    def __init__(self, number: int):
        self.number = number
        # 0暗牌 1已偷看 2明牌
        self.face_up = False
        self.peek = set()

    def peeked_by(self, player):
        if player not in self.peek:
            self.peek.add(player)

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.load(json_str)
        return cls(**data)

    def print(self):
        print(f'{self.number}', end='')
        if self.number in NUMBER_peek:
            print('[ peek ]', end='')
        if self.number in NUMBER_SPY:
            print('[  SPY ]', end='')
        if self.number in NUMBER_SWITCH:
            print('[SWITCH]', end='')


class Player:
    def __init__(self, username: str, color: str):
        self.username = username
        self.color = color
        self.hand = []
        self.score = 0
        self.reborn = False  # 是否执行过reborn
        self.cabo = False  # 是否宣告cabo

    def rich_username(self):
        return f'[bold on {self.color}]{self.username}[/bold on {self.color}]'

    def reset(self):
        self.hand = []
        self.reborn = False
        self.cabo = False

    def AddCard(self, card):
        self.hand.append(card)

    def GetCard(self, index) -> Card:
        return self.hand[index]

    def SetCard(self, index, card: Card):
        self.hand[index] = card

    def RemoveCard(self, index) -> Card:
        return self.hand.pop(index)

    def GetHandsCount(self) -> int:
        return len(self.hand)

    def GetHandScore(self) -> int:
        return sum([card.number for card in self.hand] + [0])

    def IsKamikaze(self) -> bool:
        hand = [card.number for card in self.hand]
        hand.sort()
        return hand == [12, 12, 13, 13]

    def UpdateScore(self, status):
        if status == SCORE.LOSE:
            self.score += sum([card.number for card in self.hand] + [0])
            if self.cabo:
                self.score += 10
        if status == SCORE.SOMEONE_KAMIKAZE:
            self.score += 50
        if status == SCORE.WIN:
            if not self.cabo:
                self.score += sum([card.number for card in self.hand] + [0])
        if self.score == 100:
            self.score = 50
            self.reborn = True


class GameStatus(Enum):
    LOBBY = 1
    PLAYING = 2
    ROUND_GAP = 3


class GameManager:
    def __init__(self):
        self.players = dict()       # key: str username, value: Player
        self.ready_status = dict()  # key: str username, value: bool
        self.game_status = GameStatus.LOBBY.value
        self.turnorder = PlayerTurnOrder()
        self.draw = []      # 抽牌堆
        self.seq = 0        # 当前sequence
        self.discard = []   # 抽牌堆
        self.last_act = None
        self.accept_ready_message = True

    def player_join(self, username):
        if username not in self.players.keys():
            self.players[username] = Player(username, None)
            self.turnorder.AddPlayer(username)

    def player_exit(self, username):
        if username in self.players.keys():
            self.players.pop(username)
            self.turnorder.RemovePlayer(username)

    def clear_score(self):
        for player in self.players.values():
            player.score = 0

    def new_round(self, _seed, order: list, peek_dict: dict):
        self.last_act = None
        self.game_status = GameStatus.PLAYING.value
        self.turnorder.turnorder = order
        deck = base64.b64decode(_seed)
        self.draw = [int(deck[i:i + 2]) for i in range(0, len(deck), 2)]
        self.discard = []
        for num in range(0, len(self.turnorder.turnorder)):
            username = self.turnorder.turnorder[num]
            player = self.players[username]     # type: Player
            player.color = COLOR_ORDER[num]
            player.reset()
            for i in range(0, 4):
                player.AddCard(Card(self.draw.pop(0)))
        for user in peek_dict.keys():
            player = self.players[user]
            for i in peek_dict[user]:
                card = player.GetCard(i)
                card.peeked_by(user)
        _first_discard = Card(self.draw.pop(0))
        _first_discard.face_up = True
        self.discard.append(_first_discard)

    def handle(self, message):
        # 只处理handle_action
        user = message.name
        body = message.msg
        player = self.players[user]
        if ' ' in body:
            action = body.split(' ')[0]
            param = body.split(' ')[1]
        else:
            action = body
            param = ''
        if action == 'draw&peek':
            top_card = Card(self.draw.pop(0))  # type: Card
            top_card.face_up = True
            self.discard.append(top_card)
            index = int(param)
            card = player.GetCard(index)
            card.peeked_by(user)
        if action == 'draw&spy':
            top_card = Card(self.draw.pop(0))  # type: Card
            top_card.face_up = True
            self.discard.append(top_card)
            target_name = param.split(':')[0]
            target_index = int(param.split(':')[1])
            target_player = self.players[target_name]
            card = target_player.GetCard(target_index)
            card.peeked_by(user)
        if action == 'draw&switch':
            top_card = Card(self.draw.pop(0))  # type: Card
            top_card.face_up = True
            self.discard.append(top_card)
            my_index = int(param.split(',')[0])
            card1 = player.GetCard(my_index)
            target_name = param.split(',')[1].split(':')[0]
            target_index = int(param.split(',')[1].split(':')[1])
            target_player = self.players[target_name]
            card2 = target_player.GetCard(target_index)
            _ = card2
            target_player.SetCard(target_index, card1)
            player.SetCard(my_index, _)
        if action == 'draw&change':
            top_card = Card(self.draw.pop(0))  # type: Card
            top_card.peeked_by(user)
            if ',' not in param:
                index = int(param)
                card = player.GetCard(index)
                card.face_up = True
                print(f'{user}抽取了{top_card.number}, 与{card.number}交换')
                self.discard.append(card)
                player.SetCard(index, top_card)
            else:
                indexes = [int(i) for i in param.split(',')]
                indexes.sort(reverse=True)
                tmp = set()
                for index in indexes:
                    card = player.GetCard(index)
                    tmp.add(card.number)
                if len(tmp) == 1:
                    print(f'{user}抽取了{top_card.number}, 多重交换成功')
                    for index in indexes:
                        print(f'交换了{index}的{player.GetCard(index).number}')
                        _card = player.RemoveCard(index)
                        _card.face_up = True
                        self.discard.append(_card)
                    player.AddCard(top_card)
                else:
                    print(f'{user}抽取了{top_card.number}, 多重交换失败')
                    for index in indexes:
                        _card = player.GetCard(index)
                        _card.face_up = True
                    player.AddCard(top_card)
                    if len(indexes) >= 3:
                        punish = Card(self.draw.pop(0))
                        player.AddCard(punish)
        if action == 'draw&discard':
            top_card = Card(self.draw.pop(0))  # type: Card
            top_card.face_up = True
            self.discard.append(top_card)
        if action == 'discard&draw':
            top_card = self.discard.pop()  # type: Card
            if ',' not in param:
                index = int(param)
                card = player.GetCard(index)
                card.face_up = True
                self.discard.append(card)
                player.SetCard(index, top_card)
            else:
                indexes = [int(i) for i in param.split(',')]
                indexes.sort(reverse=True)
                tmp = set()
                for index in indexes:
                    card = player.GetCard(index)
                    tmp.add(card.number)
                if len(tmp) == 1:
                    for index in indexes:
                        _card = player.RemoveCard(index)
                        _card.face_up = True
                        self.discard.append(_card)
                    player.AddCard(top_card)
                else:
                    for index in indexes:
                        _card = player.GetCard(index)
                        _card.face_up = True
                    player.AddCard(top_card)
        if action == 'cabo':
            player.cabo = True
        self.refresh()
        next_player = self.players[self.turnorder.next()]
        if next_player.cabo or len(self.draw) == 0:
            self.game_status = GameStatus.ROUND_GAP.value

    def someoneCaboed(self):
        for player in self.players.values():
            if player.cabo:
                return True
        return False
    def rich_card(self, card: Card, _username=None):
        number = card.number
        if _username is None:
            rich_str = '%2d' % number
        else:
            if card.face_up:
                rich_str = '[%2d]' % number
                return rich_str
            if _username in card.peek:
                rich_str = '%2d' % number
            else:
                rich_str = '??'
        for username in self.turnorder.turnorder:
            if username == _username:
                continue
            if username in card.peek:
                rich_str += f'[{self.players[username].color}]█[/{self.players[username].color}]'
        return rich_str

    def valid_action(self, request) -> bool:
        msg = request.msg
        return True


    def refresh_ready(self):
        if not _DEBUG:
            _ = os.system('cls')
        table = Table()
        table.add_column('Id', justify='center')
        table.add_column('用户名', justify='center')
        table.add_column('准备状态', justify='center')
        for index in range(0, len(self.turnorder.turnorder)):
            _id = index + 1
            user = self.turnorder.turnorder[index]
            player = self.players[user]     # type: Player
            if self.turnorder.current() == user:
                rich_id = f'{_id}'
            else:
                rich_id = f'{_id}'
            table.add_row(f'{rich_id}',
                          f'{player.rich_username()}',
                          f'{"已准备" if self.ready_status[user] else "未准备"}'
                          )
        console = Console()
        console.print(table)
        if all(self.ready_status.values()):
            print('等待HOST开始游戏[start]...')

    def refresh(self, msg=None, username=None):
        if not _DEBUG:
            _ = os.system('cls')
        if self.game_status == GameStatus.LOBBY.value:
            return self.refresh_ready()
        table = Table()
        table.add_column('Id', justify='center')
        table.add_column('分数', justify='center')
        table.add_column('用户名', justify='center')
        max_hand = max([len(player.hand) for player in self.players.values()])
        for i in range(max_hand):
            table.add_column(f'手牌{i}', justify='center')
        table.add_column(f'动态', justify='center', style='magenta')
        for index in range(0, len(self.turnorder.turnorder)):
            _id = index + 1
            user = self.turnorder.turnorder[index]
            player = self.players[user]     # type: Player
            if self.turnorder.current() == user:
                rich_id = f'[bold on green]{_id}[/bold on green]'
            else:
                rich_id = f'{_id}'
            if player.reborn:
                rich_score = f'[bold on red]{player.score}[/bold on red]'
            else:
                rich_score = f'{player.score}'
            rich_row = [self.rich_card(card, username) if i < len(player.hand) else '' for i, card in enumerate(player.hand)]
            if len(rich_row) < max_hand:
                rich_row += ['' for _ in range(max_hand - len(rich_row))]
            table.add_row(f'{rich_id}',
                          f'{rich_score}',
                          f'{player.rich_username()}',
                          *rich_row,
                          f'{"CABO" if player.cabo else ""}'
                          )
        console = Console()
        console.print(f'当前回合的玩家: {self.turnorder.current()}')
        console.print(f'弃牌堆顶: {self.discard[-1].number}  抽牌堆剩余: {len(self.draw)}  弃牌堆剩余: {len(self.discard)}')
        console.print(table)
        if msg is not None:
            self.update_last_info(msg)
        if self.last_act is not None:
            console.print(f'{self.last_act}')
        if self.turnorder.current() == username:
            print(f'我的回合[draw/dd/cabo]:')

    def update_last_info(self, msg):
        user = msg.name
        action = msg.msg
        if action.startswith('draw&change'):
            index = action.split(' ')[1]
            self.last_act = f'{user}抽取了一张牌, 与自己的第 {index} 张卡交换'
        if action.startswith('draw&peek'):
            index = action.split(' ')[1]
            self.last_act = f'{user}抽取了一张牌, 偷看了自己的第 {index} 张卡'
        if action.startswith('draw&spy'):
            a = action.split(' ')[1]
            t = a.split(':')[0]
            index = a.split(':')[1]
            self.last_act = f'{user}抽取了一张牌, 偷看了 {t} 的第 {index} 张卡'
        if action.startswith('draw&switch'):
            a = action.split(' ')[1]
            _my = a.split(',')[0]
            _other = a.split(',')[1]
            t = _other.split(':')[0]
            index = _other.split(':')[1]
            self.last_act = f'{user}抽取了一张牌, 将自己的第 {_my} 张卡与 {t} 的第 {index} 张卡进行了交换'
        if action.startswith('draw&discard'):
            self.last_act = f'{user}抽取了一张牌, 然后弃掉了它'
        if action.startswith('discard&draw'):
            index = action.split(' ')[1]
            self.last_act = f'{user}从弃牌堆抽取了一张牌, 与自己的第 {index} 张卡交换'
        if action.startswith('cabo'):
            self.last_act = f'{user}呼唤了CABO'


    def print_score(self):
        if not _DEBUG:
            _ = os.system('cls')
        table = Table()
        table.add_column('Id', justify='center')
        table.add_column('分数', justify='center')
        table.add_column('用户名', justify='center')
        max_hand = max([len(player.hand) for player in self.players.values()])
        for i in range(max_hand):
            table.add_column(f'手牌{i}', justify='center')
        table.add_column(f'动态', justify='center', style='magenta')

        for index in range(0, len(self.turnorder.turnorder)):
            _id = index + 1
            user = self.turnorder.turnorder[index]
            player = self.players[user]  # type: Player
            if player.reborn:
                rich_score = f'[bold on red]{player.score}[/bold on red]'
            else:
                rich_score = f'{player.score}'
            user = self.turnorder.turnorder[index]
            player = self.players[user]     # type: Player
            rich_row = [self.rich_card(card, None) if i < len(player.hand) else '' for i, card in enumerate(player.hand)]
            if len(rich_row) < max_hand:
                rich_row += ['' for _ in range(max_hand - len(rich_row))]
            table.add_row(f'{_id}',
                          f'{rich_score}',
                          f'{player.rich_username()}',
                          *rich_row,
                          f'{"CABO" if player.cabo else ""}'
                          )
        console = Console()
        console.print(table)

    def is_round_end(self) -> bool:
        return self.game_status == GameStatus.ROUND_GAP.value

    def round_end(self):
        self.game_status = GameStatus.ROUND_GAP.value
        tmp = [player.username for player in self.players.values() if player.IsKamikaze()]
        if not tmp:
            tmp = {player.username: player.GetHandScore() for player in self.players.values()}
            winners = [player.username for player in self.players.values() if (player.GetHandScore() == min(tmp, key=tmp.get))]
            for player in self.players.values():
                if player.username in winners:
                    player.UpdateScore(SCORE.WIN)
                else:
                    player.UpdateScore(SCORE.LOSE)
        else:
            winner = tmp[0]
            for player in self.players.values():
                if player.username == winner:
                    player.UpdateScore(SCORE.WIN)
                else:
                    player.UpdateScore(SCORE.SOMEONE_KAMIKAZE)
        for name, player in self.players.items():
            self.ready_status[name] = False
        self.print_score()
        for player in self.ready_status.keys():
            self.ready_status[player] = False
        print('print READY to next round...')
        self.accept_ready_message = False

    def game_end(self):
        self.game_status = GameStatus.LOBBY.value
        tmp = [player.username for player in self.players.values() if player.IsKamikaze()]
        if not tmp:
            tmp = {player.username: player.GetHandScore() for player in self.players.values()}
            winner = min(tmp, key=tmp.get)
            for player in self.players.values():
                if player.username == winner:
                    player.UpdateScore(SCORE.WIN)
                else:
                    player.UpdateScore(SCORE.LOSE)
        else:
            winner = tmp[0]
            for player in self.players.values():
                if player.username == winner:
                    player.UpdateScore(SCORE.WIN)
                else:
                    player.UpdateScore(SCORE.SOMEONE_KAMIKAZE)
        for name, player in self.players.items():
            self.ready_status[name] = False
        self.print_score()
        for player in self.ready_status.keys():
            self.ready_status[player] = False
        print('print READY to next game...')

    def check_game_finish(self):
        for name, player in self.players.items():
            if player.score > 100:
                return True
        return False
