import time
import traceback
from concurrent import futures
import queue
import random
import logging
import json
from urllib.parse import uses_fragment
import grpc
from HyperTexas.game.effects import EffectHelper
from HyperTexas.game.poker import Poker
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from concurrent.futures import ThreadPoolExecutor
from HyperTexas.action import *
import threading
from HyperTexas.game.game_enum import *
from HyperTexas.game.player import PlayerInfo
from HyperTexas.game.scorer import PokerScorer
from HyperTexas.game.base_score import BASE_SCORE, LEVEL_BOUNS_SCORE


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
        logger.info(f'Manager initialized')
        logger.info(f'Manager Poker Deck Count: {len(self.gm.deck.cards)}')
        logger.info(f'Manager Consume Deck Count: {len(self.gm.consume.cards)}')
        self.gm.game_status = GameStatus.LOBBY.value
        self.host = None
        self.users = dict()
        self.score_dict = dict()
        self.seq = 0

    def isAllPlayerReady(self):
        for k in self.users.keys():
            if not self.users[k]['ready']:
                return False
        return True

    def resetPlayerReadyStatus(self):
        for user in self.users.values():
            user['ready'] = False

    def getPlayerFromSender(self, sender: str):
        for player in self.gm.player_order:
            if player.username == sender:
                return player
        return None

    def Handle(self, request, context):
        sender = request.sender
        body = json.loads(request.body)
        logger.info('Status: {} , Receive from {}: {}'.format(self.gm.game_status, sender, body))
        
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
                    if not self.isAllPlayerReady():
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
                        for i in range(2):
                            try:
                                _ = self.gm.deck.Draw()
                                _.setVisible(player.username)
                                player.pokers.append(_)
                            except Exception as ex:
                                logger.error(f'Draw poker error: {ex}')
                                traceback.print_exc()
                        for i in range(3):
                            try:
                                _ = self.gm.consume.Draw()
                                _.setVisible(player.username)
                                player.hand_cards.append(_)
                            except Exception as ex:
                                logger.error(f'Draw consume error: {ex}')
                                traceback.print_exc()
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
            player = self.getPlayerFromSender(sender)
            public_cards_count = len(self.gm.public_cards)
            if body['action'] == TurnAction.USE_CARD.value:
                # 处理使用卡牌
                card_id = body.get('arg1')
                if card_id:
                    # TODO: 实现使用卡牌逻辑
                    num = int(ord(card_id) - ord('a')) - len(player.pokers)
                    _card = player.hand_cards.pop(num)
                    for p in self.gm.player_order:
                        _card.setVisible(p)
                    self.gm.last_used_cards.append(_card)
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
                    self.resetPlayerReadyStatus()
                    self._broadcast()
                    return self._response(1, 200, json.dumps('Game Started'))
        elif self.gm.game_status == GameStatus.WAIT_PLAY.value:
            if body['action'] == TurnAction.PLAY_CARD.value:
                # 处理玩家出牌
                if self.users[sender]['ready']:
                    return self._response(1, 200, json.dumps('You already played'))
                player = self.getPlayerFromSender(sender)
                _poker_play = []
                try:
                    # TODO: 'PlayerInfo' object is not subscriptable
                    _poker_play.append(self.getPokerByArg(body['arg1']))
                    _poker_play.append(self.getPokerByArg(body['arg2']))
                    _poker_play.append(self.getPokerByArg(body['arg3']))
                    _poker_play.append(self.getPokerByArg(body['arg4']))
                    _poker_play.append(self.getPokerByArg(body['arg5']))
                    _poker_play = [i for i in _poker_play if i is not None]
                except Exception as ex:
                    logger.error(f'In getPokerByArg: {ex}')
                    traceback.print_exc()
                try:
                    _type, _score_pokers = PokerScorer.score(_poker_play)
                    _unscore_pokers = set(self.gm.public_cards + player.pokers) - set(_score_pokers)
                    print(set(_score_pokers))
                    print(set(_unscore_pokers))
                    mult = 1
                    chip, mag = BASE_SCORE[_type]
                    _chip1, _mag1 = LEVEL_BOUNS_SCORE[_type]
                    level = player.level[_type]
                    chip += _chip1 * level
                    mag += _mag1 * level
                except Exception as ex:
                    logger.error(f'In calculating base score: {ex}')
                    traceback.print_exc()
                try:
                    chip, mag, mult = EffectHelper.CalculateStart(_type, chip, mag, mult, player, self.gm)
                    for i in range(0, len(_score_pokers)):
                        poker = _score_pokers[i]
                        chip, mag, mult = EffectHelper.CalculateScoredPoker(i, _type, chip, mag, mult, player, self.gm, poker)
                    for poker in _unscore_pokers:
                        chip, mag, mult = EffectHelper.CalculateUnScoredPoker(_type, chip, mag, mult, player, self.gm, poker)
                    chip, mag, mult = EffectHelper.CalculateEnd(_type, chip, mag, mult, player, self.gm)
                    self.users[sender]['ready'] = True
                    self.score_dict[sender] = {
                        'type': _type, 
                        'score': chip * mag * mult,
                        'chip': chip,
                        'mag': mag,
                        'mult': mult
                        }
                except Exception as ex:
                    logger.error(f'In creating score dict: {ex}')
                    traceback.print_exc()
                try:
                    if self.isAllPlayerReady():
                        # 计算分数
                        self.gm.game_status = GameStatus.SCORE.value
                        self.resetPlayerReadyStatus()
                        max_score = max(self.score_dict[play].get('score', 0) for play in self.score_dict.keys())
                        temp_chip = sum([max_score - self.score_dict[player.username]['score'] for player in self.gm.player_order])
                        winner_number = [player.username for player in self.gm.player_order if self.score_dict[player.username]['score'] == max_score]
                        for player in self.gm.player_order:
                            if player.username in winner_number:
                                _chg = int(temp_chip / len(winner_number))
                                player.chip += _chg
                                self.score_dict[player.username]['change'] = _chg
                                self.score_dict[player.username]['win'] = True
                                self.gm.current_player_index = self.gm.player_order.index(player)
                            else:
                                _chg = max_score - self.score_dict[player.username]['score']
                                player.chip -= _chg
                                self.score_dict[player.username]['change'] = _chg * -1
                                self.score_dict[player.username]['win'] = False                        
                except Exception as ex:
                    logger.error(f'In Calculate Score: {ex}')
                    traceback.print_exc()
                self._broadcast()
                return self._response(1, 200, json.dumps('Turn Completed'))
        # 计分状态
        elif self.gm.game_status == GameStatus.SCORE.value:
            # 重置玩家确认状态
            self.users[sender]['ready'] = True
            if self.isAllPlayerReady():
                if self.gm.GameFinished():
                    self.score_dict = dict()
                    self.gm.game_status = GameStatus.LOBBY.value
                    self.gm.public_cards = []
                    self.gm.current_player_index = 0
                else:
                    self.gm.game_status = GameStatus.GAME.value
                    while len(self.gm.public_cards) > 0:
                        try:
                            card = self.gm.public_cards.pop(0)
                            self.gm.deck.cards.append(card)
                        except Exception as ex:
                            logger.error(f'Pop from public cards error: {ex}')
                            traceback.print_exc()
                    for player in self.gm.player_order:
                        while len(player.pokers) > 0:
                            try:
                                card = player.pokers.pop(0)
                                self.gm.deck.cards.append(card)
                            except Exception as ex:
                                logger.error(f'Pop from player pokers error: {ex}')
                                traceback.print_exc()
                    self.gm.deck.shuffle()
                    for card in self.gm.deck.cards:
                        card.ResetVisible()
                    # 发初始手牌
                    for player in self.gm.player_order:
                        for i in range(2):
                            try:
                                _ = self.gm.deck.Draw()
                                _.setVisible(player.username)
                                player.pokers.append(_)
                            except Exception as ex:
                                logger.error(f'Draw poker error: {ex}')
                                traceback.print_exc()
                        for i in range(3):
                            try:
                                _ = self.gm.consume.Draw()
                                _.setVisible(player.username)
                                player.hand_cards.append(_)
                            except Exception as ex:
                                logger.error(f'Draw consume error: {ex}')
                                traceback.print_exc()
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
            traceback.print_exc()
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
        try:
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
                data['last_used_cards'] = [c.to_dict() for c in self.gm.last_used_cards]
                data['deck'] = self.gm.deck.dump()
            if data['game_status'] == GameStatus.WAIT_PLAY.value:
                data['current_player_index'] = self.gm.current_player_index
                data['players'] = [p.to_dict() for p in self.gm.player_order]
                data['public_cards'] = [c.to_dict() for c in self.gm.public_cards]
                data['last_used_cards'] = [c.to_dict() for c in self.gm.last_used_cards]
                data['deck'] = self.gm.deck.dump()
                _ = dict()
                for k, v in self.users.items():
                    _[k] = v['ready']
                data['ready_status'] = _
            if data['game_status'] == GameStatus.SCORE.value:
                data['current_player_index'] = self.gm.current_player_index
                data['players'] = [p.to_dict() for p in self.gm.player_order]
                data['public_cards'] = [c.to_dict() for c in self.gm.public_cards]
                data['last_used_cards'] = [c.to_dict() for c in self.gm.last_used_cards]
                data['deck'] = self.gm.deck.dump()
                data['score_dict'] = self.score_dict
                _ = dict()
                for k, v in self.users.items():
                    _[k] = v['ready']
                data['ready_status'] = _
                logger.info(f'broadcast score data: {data["ready_status"]}')
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
        except Exception as e:
            logger.error(f'Error in broadcast: {e}')
            logger.error(f'{data}')
            traceback.print_exc()

    def _onDisconnectWrapper(self, request, context):
        def callback():
            curUser = request.name
            self._broadcast()
            del curUser['stream']
            self.gm.player_exit(curUser['name'])
        return callback

    def getPokerByArg(self, arg):
        if arg is None:
            return None
        try:
            if arg.startswith('pub.') or arg.startswith('p.'):
                _ = arg.split('.')[1]
                num = int(ord(_) - ord('a'))
                return self.gm.public_cards[num]
            else:
                index = int(arg[1])
                _ = arg.split('.')[1]
                num = int(ord(_) - ord('a'))
                return self.gm.player_order[index - 1].pokers[num]
        except Exception as ex:
            logger.error(f'In getPokerByArg: {ex}')
            traceback.print_exc()

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
