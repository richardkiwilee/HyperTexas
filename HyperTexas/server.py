import time
from concurrent import futures
import queue
import random
import logging
import json
from urllib.parse import uses_fragment
import grpc
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from concurrent.futures import ThreadPoolExecutor
from HyperTexas.action import *
import threading
from HyperTexas.game.game_enum import *
from HyperTexas.game.player import PlayerInfo


queues = []
# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# 将处理器添加到日志记录器
logger.addHandler(console_handler)

class LobbyServicer(rpc.LobbyServicer):
    def __init__(self):
        self.gm = Manager()
        self.gm.game_status = GameStatus.LOBBY.value
        self.host = None
        self.users = dict()
        self.seq = 0
        self.player_timers = {}  # 存储玩家操作的定时器
        self.timeout_duration = 60  # 超时时间（秒）

    def _handle_timeout(self, player_name):
        """处理玩家操作超时"""
        if player_name in self.player_timers:
            del self.player_timers[player_name]
            self._broadcast()
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
        logger.info('Receive from {}: {}'.format(sender, body))
        
        # 强制刷新功能
        if body['action'] == LobbyAction.SYNC.value:
            self._broadcast()
            return self._response(1, 200, json.dumps(self._broadcast()))
        # 大厅状态
        if self.gm.game_status == GameStatus.LOBBY.value:
            if body['action'] == LobbyAction.LOGIN.value:
                username = body['arg1']
                if len(self.users) == 0:
                    self.host = username
                if username not in self.users:
                    self.users[username] = dict()
                    self.users[username]['ready'] = False
                    lobby_init = self._broadcast()
                    return self._response(1, 200, json.dumps(lobby_init))
                else:
                    self._broadcast()
                    return self._response(1, 200, json.dumps('username already in use'))
            
            if body['action'] == LobbyAction.LOGOUT.value:
                username = body['arg1']
                if username in self.users:
                    self.users.pop(username)
                    self._broadcast()
                return self._response(1, 200, json.dumps('Logout'))
            
            if body['action'] == LobbyAction.READY.value:
                if sender in self.users:
                    self.users[sender]['ready'] = True
                    self._broadcast()
                return self._response(1, 200, json.dumps('Ready'))
            
            if body['action'] == LobbyAction.CANCEL.value:
                if sender in self.users:
                    self.users[sender]['ready'] = False
                    self._broadcast()
                return self._response(1, 200, json.dumps('Cancel Ready'))
            
            if body['action'] == LobbyAction.START_GAME.value:
                # 检查是否所有玩家都准备好
                if sender == self.host:
                    if not all(user.get('ready', False) for user in self.users.values()):
                        self._broadcast()
                        return self._response(1, 400, json.dumps('Not all players are ready'))
                    # 设置游戏状态为游戏中
                    self.gm.game_status = GameStatus.GAME.value
                    # 洗牌
                    self.gm.deck.shuffle()
                    self.gm.consume.shuffle()
                    # 随机排序玩家位置
                    for k,v in self.users.items():
                        player = PlayerInfo()
                        player.username = k
                        player.chip = self.gm.base_chip
                        self.gm.player_order.append(player)
                    random.shuffle(self.gm.player_order)                
                    # 发初始手牌
                    for player in self.gm.player_order:
                        # TODO: 实现发牌逻辑
                        for i in range(2):
                            _ = self.gm.deck.Draw()
                            _.setVisible(player.username)
                            player.pokers.append(_)
                        for i in range(3):
                            _ = self.gm.consume.Draw()
                            _.setVisible(player.username)
                            player.hand_cards.append(_)
                        pass
                    self.gm.current_player_index = 0
                    self.gm.game_status = GameStatus.GAME.value
                else:
                    self._broadcast()
                    return self._response(1, 400, json.dumps('Not host'))
                self._broadcast()
                return self._response(1, 200, json.dumps('Game Started'))
        
        # 游戏进行中状态
        elif self.gm.game_status == GameStatus.GAME.value:
            # 检查是否是当前玩家的回合
            if sender != self.gm.player_order[self.gm.current_player_index].username:
                self._broadcast()
                return self._response(1, 400, json.dumps(f'Not your turn, current player index: {self.gm.current_player_index}'))            
            # 根据公共牌数量判断游戏阶段
            public_cards_count = len(self.gm.public_cards)
            if body['action'] == TurnAction.USE_CARD.value:
                # 处理使用卡牌
                card_id = body.get('arg1')
                if card_id:
                    # TODO: 实现使用卡牌逻辑
                    self._next_player()
                    self._broadcast()
            if body['action'] == TurnAction.USE_SKILL.value:
                # 处理使用技能
                skill_id = body.get('arg1')
                if skill_id:
                    # TODO: 实现使用技能逻辑
                    self._next_player()
                    self._broadcast()            
            if body['action'] == TurnAction.PASS.value:
                # 处理过牌
                self._next_player()
                self._broadcast()
            if body['action'] == TurnAction.FOLD.value:
                # 处理弃牌
                if sender in self.gm.player_order:
                    self.gm.player_order.remove(sender)
                    if len(self.gm.player_order) <= 1:
                        # 只剩一个玩家，进入计分阶段
                        self.gm.game_status = GameStatus.SCORE.value
                    self._next_player()
                    self._broadcast()

            # 检查是否需要发更多公共牌            
            if self._round_complete():
                if len(self.gm.public_cards) < 3:
                    while len(self.gm.public_cards) < 3:
                        _card = self.gm.deck.Draw()
                        for player in self.gm.player_order:
                            _card.setVisible(player.username)
                        self.gm.public_cards.append(_card)
                    self._broadcast()
                    return self._response(1, 200, json.dumps('Game Started'))
                if len(self.gm.public_cards) == 3:
                    _card = self.gm.deck.Draw()
                    for player in self.gm.player_order:
                        _card.setVisible(player.username)
                    self.gm.public_cards.append(_card)
                    self._broadcast()
                    return self._response(1, 200, json.dumps('Game Started'))
                if len(self.gm.public_cards) == 4:
                    _card = self.gm.deck.Draw()
                    for player in self.gm.player_order:
                        _card.setVisible(player.username)
                    self.gm.public_cards.append(_card)
                    self._broadcast()
                    return self._response(1, 200, json.dumps('Game Started'))
                if len(self.gm.public_cards) == 5:
                    # 进入等待出牌的阶段
                    self.gm.game_status = GameStatus.WAIT_PLAY.value
                    self._broadcast()
                    return self._response(1, 200, json.dumps('Game Started'))
        elif self.gm.game_status == GameStatus.WAIT_PLAY.value:
            if body['action'] == TurnAction.PLAY_CARD.value:
                # 处理玩家出牌
                if self._round_complete():
                    # TODO: 实现计分逻辑
                    self.gm.game_status == GameStatus.SCORE.value
                else:
                    self._next_player()
                self._broadcast()
                return self._response(1, 200, json.dumps('Turn Completed'))
        # 计分状态
        elif self.gm.game_status == GameStatus.SCORE.value:
            # TODO: 等待所有玩家确认
            # TODO: 重置游戏状态
            self.gm.game_status = GameStatus.LOBBY.value
            self.gm.public_cards = []
            self.gm.current_player_index = 0
            
            # 重置玩家准备状态
            for user in self.users.values():
                user['ready'] = False            
            self._broadcast()
            return self._response(1, 200, json.dumps('Round Complete'))
        self._broadcast()
        return self._response(1, 200, json.dumps('Action processed'))

    def _next_player(self):
        """移动到下一个玩家"""
        self.gm.current_player_index = (self.gm.current_player_index + 1) % len(self.gm.player_order)

    def _round_complete(self):
        """检查当前回合是否结束"""
        return self.gm.current_player_index + 1 == len(self.gm.player_order)

    def Subscribe(self, request, context):
        """
        Handle client subscription to game state updates
        """
        # Create a queue for this client's messages
        message_queue = queue.Queue()
        
        # Add the client to our users with their stream queue
        if request.sender not in self.users:
            self.users[request.sender] = {'name': request.sender, 'stream': message_queue}
        else:
            self.users[request.sender]['stream'] = message_queue
            
        # Send initial game state
        self._broadcast()
        
        try:
            while True:
                # Wait for messages in the queue
                message = message_queue.get()
                if message is None:  # Check for termination signal
                    break
                yield message
        except Exception as e:
            logger.error(f"Error in subscription stream for {request.sender}: {e}")
        finally:
            # Cleanup when client disconnects
            if request.sender in self.users:
                if 'stream' in self.users[request.sender]:
                    del self.users[request.sender]['stream']

    def _response(self, msgtype, status, body):
        return pb2.GeneralResponse(sequence=0, msgtype=msgtype, status=status, sender='__SERVER__', body=body)

    def Broadcast(self, info):
        return pb2.Broadcast(sequence=self.seq, msgtype=200, 
                            status=200, sender='SYSTEM',
                            body=json.dumps(info))

    def _broadcast(self):
        self.seq += 1
        data = dict()
        data['game_status'] = self.gm.game_status
        if data['game_status'] == GameStatus.LOBBY.value:
            ready_status = dict()
            for user, _data in self.users.items():
                ready_status[user] = _data['ready']
            data['ready_status'] = ready_status
        if data['game_status'] == GameStatus.GAME.value:
            data['current_player_index'] = self.gm.current_player_index
            data['players'] = [p.to_dict() for p in self.gm.player_order]
            data['public_cards'] = [c.to_dict() for c in self.gm.public_cards]
            data['last_used_cards'] = self.gm.last_used_cards
            data['deck'] = self.gm.deck.dump()
        _obj = pb2.Broadcast(
            sequence=self.seq,
            msgtype=0,
            status=200,
            sender='__SYSTEM__',
            body=json.dumps(data)
        )
        for user in self.users:
            if 'stream' in self.users[user]:
                self.users[user]['stream'].put(_obj)
        return data

    def _onDisconnectWrapper(self, request, context):
        def callback():
            curUser = request.name
            self._broadcast()
            del curUser['stream']
            self.gm.player_exit(curUser['name'])
        return callback


def server(port=50051):
    logger.info('Starting server')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    rpc.add_LobbyServicer_to_server(LobbyServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    logger.info('Server started')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Exiting')
        # to unblock all queues
        for q in queues:
            q.put(None)
        server.stop(0)


if __name__ == '__main__':
    server()
