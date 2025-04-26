import time
from concurrent import futures
import queue
import random
import logging
import json
from enum import Enum
from urllib.parse import uses_fragment
import grpc
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from concurrent.futures import ThreadPoolExecutor
from HyperTexas.action import *
import threading
from HyperTexas.game.enum import *


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
        if self.gm.game_status == GameStatus.LOBBY.value:
            if body['action'] == LobbyAction.LOGIN.value:
                username = body['arg1']
                if len(self.users) == 0:
                    self.host = username
                if username not in self.users:
                    self.users[username] = dict()
                    self._broadcast() 
                    return self._response(1, 200, json.dumps('Login'))
            if body['action'] == LobbyAction.LOGOUT.value:
                username = body['arg1']
                self.users.pop(username)
                self._broadcast()
                return self._response(1, 200, json.dumps('Logout'))
            if body['action'] == LobbyAction.READY.value:
                self._broadcast()
                return self._response(1, 200, json.dumps('Ready'))
            if body['action'] == LobbyAction.CANCEL.value:
                self._broadcast()
                return self._response(1, 200, json.dumps('Cancel Ready'))
            if body['action'] == LobbyAction.START_GAME.value:
                # 设置游戏状态为回合开始
                self.gm.game_status = GameStatus.ROUND_START.value
                self._broadcast()
                # 洗牌
                self.gm.deck.shuffle()
                # 随机排序玩家位置
                self.gm.active_players = list(self.character_dict.values())
                random.shuffle(self.gm.active_players)
                self._broadcast()
                self._broadcast()
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
                        self._broadcast()
                
                # 广播游戏开始消息
                start_msg = {
                    'type': 'game_start',
                    'player_order': [p.name for p in self.gm.active_players]
                }
                self._broadcast()
                
                return self._response(1, 200, json.dumps(start_msg))
            if body['action'] == LobbyAction.KICK.value:
                pass
        
        if self.gm.game_status == GameStatus.ROUND_START.value:
            # 广播回合开始消息
            round_start_msg = {
                'type': 'round_start',
                'player_order': [p.name for p in self.gm.active_players]
            }
            self._broadcast()
            # 进入发牌前阶段
            self.gm.game_status = GameStatus.BEFORE_GIVE_PLAYER_CARDS.value
            return self._response(1, 200, json.dumps('Round started'))

        if self.gm.game_status == GameStatus.BEFORE_GIVE_PLAYER_CARDS.value:
            # 按顺序等待玩家操作回合 每位玩家完成回合后发给他底牌并轮到下一位玩家
            current_player = self.gm.get_current_player()
            if not current_player or current_player.name != request.name:
                return self._response(1, 400, json.dumps('Not your turn'))

            # 处理玩家的操作
            if 'action' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 发底牌给当前玩家
            self.gm.deal_to_player(current_player.name)
            # 广播玩家获得底牌的消息（不包含具体牌面）
            self._broadcast()
            # 移动到下一个玩家
            next_player = self.gm.next_player()
            if next_player:
                self._broadcast()
            else:
                # 所有玩家都已获得底牌，进入下一阶段
                self.gm.game_status = GameStatus.BEFORE_PUBLIC_CARDS_3.value

            return self._response(1, 200, json.dumps('Action processed'))

        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_3.value:
            # 按顺序等待玩家操作回合 所有玩家完成回合后发3张公共牌
            current_player = self.gm.get_current_player()
            if not current_player or current_player.name != request.name:
                return self._response(1, 400, json.dumps('Not your turn'))

            # 处理玩家的操作
            if 'action' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 移动到下一个玩家
            next_player = self.gm.next_player()
            if next_player:
                self._broadcast()
            else:
                # 所有玩家都已完成操作，发3张公共牌
                public_cards = self.gm.deal_public_cards(3)
                self._broadcast()
                # 进入下一阶段
                self.gm.game_status = GameStatus.BEFORE_PUBLIC_CARDS_4.value

            return self._response(1, 200, json.dumps('Action processed'))

        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_4.value:
            # 按顺序等待玩家操作回合 所有玩家完成回合后发第4张公共牌
            current_player = self.gm.get_current_player()
            if not current_player or current_player.name != request.name:
                return self._response(1, 400, json.dumps('Not your turn'))

            # 处理玩家的操作
            if 'action' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 移动到下一个玩家
            next_player = self.gm.next_player()
            if next_player:
                self._broadcast()
            else:
                # 所有玩家都已完成操作，发第4张公共牌
                public_cards = self.gm.deal_public_cards(1)
                self._broadcast()
                # 进入下一阶段
                self.gm.game_status = GameStatus.BEFORE_PUBLIC_CARDS_5.value

            return self._response(1, 200, json.dumps('Action processed'))

        if self.gm.game_status == GameStatus.BEFORE_PUBLIC_CARDS_5.value:
            # 按顺序等待玩家操作回合 所有玩家完成回合后发第5张公共牌
            current_player = self.gm.get_current_player()
            if not current_player or current_player.name != request.name:
                return self._response(1, 400, json.dumps('Not your turn'))

            # 处理玩家的操作
            if 'action' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 移动到下一个玩家
            next_player = self.gm.next_player()
            if next_player:
                self._broadcast()
            else:
                # 所有玩家都已完成操作，发第5张公共牌
                public_cards = self.gm.deal_public_cards(1)
                self._broadcast()
                # 进入下一阶段
                self.gm.game_status = GameStatus.BEFORE_OPEN.value

            return self._response(1, 200, json.dumps('Action processed'))

        if self.gm.game_status == GameStatus.BEFORE_OPEN.value:
            # 按顺序等待玩家操作回合 所有玩家完成回合后进入开牌阶段
            current_player = self.gm.get_current_player()
            if not current_player or current_player.name != request.name:
                return self._response(1, 400, json.dumps('Not your turn'))

            # 处理玩家的操作
            if 'action' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 移动到下一个玩家
            next_player = self.gm.next_player()
            if next_player:
                self._broadcast()
            else:
                # 所有玩家都已完成操作，进入开牌阶段
                self.gm.game_status = GameStatus.COLLECT_DEAL.value
                self._broadcast()

            return self._response(1, 200, json.dumps('Action processed'))

        if self.gm.game_status == GameStatus.COLLECT_DEAL.value:
            # 所有玩家同时进行回合操作 等待所有玩家均完成开牌进入结算阶段
            # 检查是否是合法的出牌请求
            if 'action' not in body or 'cards' not in body:
                return self._response(1, 400, json.dumps('Invalid request format'))
            
            player_name = request.name
            # 记录玩家的出牌
            if not self.gm.record_player_deal(player_name, body['cards']):
                return self._response(1, 400, json.dumps('Invalid cards'))
            
            # 广播玩家的出牌信息
            self._broadcast()
            
            # 检查是否所有玩家都已出牌
            if self.gm.all_players_dealt():
                # 所有玩家都已出牌，进入回合结束阶段
                self.gm.game_status = GameStatus.ROUND_END.value
                # 计算本回合结果
                round_result = self.gm.calculate_round_result()
                # 广播回合结果
                self._broadcast()
                return self._response(1, 200, json.dumps('Round ended'))
            else:
                # 还有玩家未出牌
                return self._response(1, 200, json.dumps('Deal recorded'))

        if self.gm.game_status == GameStatus.ROUND_END.value:
            # 广播回合结束消息 广播计分结果 等待所有玩家确认后开启新的一轮
            if 'action' not in body or body['action'] != 'confirm_result':
                return self._response(1, 400, json.dumps('Invalid request format'))

            # 记录玩家确认
            if self.gm.confirm_round_result(request.name):
                # 所有玩家都已确认，开始新的一轮
                self.gm.start_new_round()
                self._broadcast()
            return self._response(1, 200, json.dumps('Result confirmed'))

        if self.gm.game_status == GameStatus.GAME_END.value:
            # 广播游戏结束消息 广播最终结果 回到大厅状态
            final_result = {
                'type': 'game_end',
                'final_scores': {p.name: p.score for p in self.gm.active_players}
            }
            self._broadcast()
            # 回到大厅状态
            self.gm.game_status = GameStatus.LOBBY.value
            return self._response(1, 200, json.dumps('Game ended'))
        
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
                self.gm.player_exit(request.sender)

    def _response(self, msgtype, status, body):
        return pb2.GeneralResponse(sequence=0, msgtype=msgtype, status=status, sender='__SERVER__', body=body)

    def Broadcast(self, info):
        return pb2.Broadcast(sequence=self.seq, msgtype=200, 
                            status=200, sender='SYSTEM',
                            body=json.dumps(info))

    def _broadcast(self):
        self.seq += 1
        game_state = self.gm.game_status  # Assuming this method exists to get current game state
        _obj = pb2.Broadcast(
            sequence=self.seq,
            msgtype=0,
            status=200,
            sender='__SYSTEM__',
            body=json.dumps(game_state)
        )
        for user in self.users:
            if 'stream' in self.users[user]:
                self.users[user]['stream'].put(_obj)

    def _onDisconnectWrapper(self, request, context):
        def callback():
            curUser = request.name
            self._broadcast()
            del curUser['stream']
            self.gm.player_exit(curUser['name'])
        return callback


def server(port=50051):
    logger.info('>>> Starting server...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    rpc.add_LobbyServicer_to_server(LobbyServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    logger.info('>>> Server started')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('>>> Exiting')
        # to unblock all queues
        for q in queues:
            q.put(None)
        server.stop(0)


if __name__ == '__main__':
    server()
