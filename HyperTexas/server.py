import time
from concurrent import futures
import queue
import random
import json
from urllib.parse import uses_fragment
import grpc
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from concurrent.futures import ThreadPoolExecutor
from HyperTexas.action import *
import threading

queues = []

class GameStatus(Enum):
    LOBBY = 1                     # 大厅内 游戏未开始
    ROUND_START = 2               # 回合开始前 同步桌面信息
    BEFORE_GIVE_PLAYER_CARDS = 3  # 发玩家底牌前 有部分技能会触发
    BEFORE_PUBLIC_CARDS_3 = 4     # 发3张公共牌前 有部分技能会触发
    BEFORE_PUBLIC_CARDS_4 = 5     # 场上3张公共牌 第一次常规轮
    BEFORE_PUBLIC_CARDS_5 = 6     # 场上4张公共牌 第二次常规轮
    BEFORE_OPEN = 7               # 场上5张公共牌 第三次常规轮
    COLLECT_DEAL = 8              # 等待所有玩家确认出牌
    ROUND_END = 9                 # 返回所有玩家的出牌结果 等待所有玩家确认
    GAME_END = 10                 # 有玩家出局 游戏结束 等待所有玩家确认

class LobbyAction(Enum):
    LOGIN = 1
    LOGOUT = 2
    READY = 3
    CANCEL = 4
    START_GAME = 5
    KICK = 6

class TurnAction(Enum):
    PASS = 0
    USE_CARD = 1
    USE_SKILL = 2
    FOLD = 3

class BroadcastType(Enum):
    HEARTBEAT = 0
    UPDATE_STATUS = 1
    SET_CURRENT_PLAYER = 2
    SYNC = 3
    START_TIMER = 4
    TIMEOUT = 5
    CONFIRM_ACTION = 6

class LobbyServicer(rpc.LobbyServicer):
    def __init__(self):
        self.gm = Manager()
        self.gm.game_status = GameStatus.LOBBY.value
        self.host = None
        self.users = set()
        self.seq = 0
        self.player_timers = {}  # 存储玩家操作的定时器
        self.timeout_duration = 60  # 超时时间（秒）

    def _handle_timeout(self, player_name):
        """处理玩家操作超时"""
        if player_name in self.player_timers:
            del self.player_timers[player_name]
            self._broadcast(
                msgtype=BroadcastType.TIMEOUT.value,
                sender='__SYSTEM__',
                body=json.dumps({
                    'type': 'timeout',
                    'player': player_name
                })
            )
            # 这里可以添加默认的超时处理逻辑，比如跳过该玩家的操作


    def _start_player_timer(self, player_name):
        """为玩家启动操作定时器"""
        if player_name in self.player_timers:
            self.player_timers[player_name].cancel()
        timer = threading.Timer(self.timeout_duration, self._handle_timeout, args=[player_name])
        timer.start()
        self.player_timers[player_name] = timer

    def _stop_player_timer(self, player_name):
        """停止玩家的操作定时器"""
        if player_name in self.player_timers:
            self.player_timers[player_name].cancel()
            del self.player_timers[player_name]

    def Handle(self, request, context):
        sender = request.sender
        body = json.loads(request.body)
        if self.gm.game_status == GameStatus.LOBBY.value:
            if body['action'] == LobbyAction.LOGIN.value:
                username = body['username']
                if len(self.users) == 0:
                    self.host = username
                if username not in self.users:
                    self.users.add(username)
                    self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({}))                    
                    return self._response(1, 200, json.dumps('Login'))
            if body['action'] == LobbyAction.LOGOUT.value:
                self.users.remove(username)
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({}))
                return self._response(1, 200, json.dumps('Logout'))
            if body['action'] == LobbyAction.READY.value:
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({}))
                return self._response(1, 200, json.dumps('Ready'))
            if body['action'] == LobbyAction.CANCEL.value:
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({}))
                return self._response(1, 200, json.dumps('Cancel Ready'))
            if body['action'] == LobbyAction.START_GAME.value:
                # 设置游戏状态为回合开始
                self.gm.game_status = GameStatus.ROUND_START.value
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({}))
                # 洗牌
                self.gm.deck.shuffle()
                # 随机排序玩家位置
                self.gm.active_players = list(self.character_dict.values())
                random.shuffle(self.gm.active_players)
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({'PlayerOrder': [p.name for p in self.gm.active_players]}))
                self._broadcast(msgtype=1, status=200, sender='', body=json.dumps({'CurrentPlayer': self.gm.active_players[0].name}))
                # 设置游戏状态为发牌前
                self.gm.game_status = GameStatus.BEFORE_GIVE_PLAYER_CARDS.value
                # 检查每个玩家的发牌前可选操作
                for player in self.gm.active_players:
                    if player.has_pre_deal_options():  # 假设这个方法检查玩家是否有发牌前可选操作
                        # 启动该玩家的操作定时器
                        self._start_player_timer(player.name)                        
                        # 向玩家发送询问消息
                        options_msg = {
                            'type': 'pre_deal_options',
                            'options': player.get_pre_deal_options()  # 获取可选操作列表
                        }
                        self._broadcast(
                            msgtype=2,  # 假设2是询问消息类型
                            status=200,
                            sender=player.name,
                            body=json.dumps(options_msg)
                        )
                
                # 广播游戏开始消息
                start_msg = {
                    'type': 'game_start',
                    'player_order': [p.name for p in self.gm.active_players]
                }
                self._broadcast(
                    msgtype=1,
                    status=200,
                    sender='',
                    body=json.dumps(start_msg)
                )
                
                return self._response(1, 200, json.dumps(start_msg))
            if body['action'] == LobbyAction.KICK.value:
                pass
        if self.gm.game_status == GameStatus.ROUND_START.value:
            pass
        if self.gm.game_status == GameStatus.BEFORE_GIVE_PLAYER_CARDS.value:
            pass
        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_3.value:
            pass
        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_4.value:
            pass
        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_5.value:
            pass
        if self.gm.game_status == GameStatus.BEFORE_OPEN.value:
            pass
        if self.gm.game_status == GameStatus.COLLECT_DEAL.value:
            pass
        if self.gm.game_status == GameStatus.ROUND_END.value:
            pass
        if self.gm.game_status == GameStatus.GAME_END.value:
            pass
        
    def Subscribe(self, request, context):
        if not self._isAuthorized(request):
            return pb2.Broadcast()

        if request.name in self.users:
            return pb2.Broadcast(type=pb2.Broadcast.FAILURE, msg='Already subscribed')

        cb_added = context.add_callback(self._onDisconnectWrapper(request, context))

        if not cb_added:
            # print('Warning: disconnection will not be called')
            pass

        q = queue.Queue()
        self.queues.append(q)
        self.users[request.name]['stream'] = q
        yield pb2.Broadcast(type=pb2.Broadcast.UNSPECIFIED)

        while True:
            q = self.users[request.name]['stream']
            obj = q.get()
            if obj is None:
                yield pb2.Broadcast(type=pb2.Broadcast.FAILURE, msg='The server is shutting down')
                return
            yield pb2.Broadcast(**obj)
            q.task_done()

    def _response(self, msgtpye, status, body):
        return pb2.GeneralResponse(sequence=0, type=msgtpye, status=status, sender='__SERVER__', body=body)

    def _broadcast(self, msgtype, status, sender, body):
        self.seq += 1
        _obj = {'sequence': self.seq, 'type': msgtype, 'status': status, 'sender': sender, 'body': body}
        for _, user in self.users.items():
            if 'stream' in user:
                user['stream'].put(_obj)

    def _onDisconnectWrapper(self, request, context):
        def callback():
            curUser = request.name
            self._broadcast(msgtype=0, status=200, sender='', body=json.dumps({}))
            del curUser['stream']
            self.gm.player_exit(curUser['name'])
        return callback


def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    rpc.add_LobbyServicer_to_server(LobbyServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    # print('>>> Server started')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # print('>>> Exiting')
        # to unblock all queues
        for q in queues:
            q.put(None)
        server.stop(0)


if __name__ == '__main__':
    serve()
