import time
import grpc
import threading
import queue
import sys
import random
import string
import argparse
import json
import os
from HyperTexas.game.enum import LobbyAction
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from HyperTexas.game.poker import Poker
from HyperTexas.game.card import Card
from HyperTexas.game.effects import *
from HyperTexas.game.character import Character
from HyperTexas.game.ui import RefreshScreen


class Client:
    def __init__(self, username: str, address='localhost', port=50051):
        self.username = username
        # 创建 gRPC 通道和存根
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.stub = rpc.LobbyStub(channel)
        # 启动一个新线程监听消息
        self.table_info = dict()
        loginResp = self.sendMessage(LobbyAction.LOGIN.value, self.username)
        if loginResp.status != 200:
            print('Failed to login chatroom: {}'.format(loginResp.msg))
            return
        listening = threading.Thread(target=self.__listen_for_messages, daemon=True)
        listening.start()
        input_queue = queue.Queue()
        input_thread = threading.Thread(target=self.add_input, args=(input_queue, self.stub))
        input_thread.daemon = True
        input_thread.start()

    def isPlayer(self, s: str) -> bool:
        """
        检查参数是否符合玩家格式要求: p开头后跟数字
        例如: "p1", "p2" 等
        """
        if not isinstance(s, str) or not s:
            return False
        if not s.startswith('p'):
            return False
        try:
            num = int(s[1:])
            if num < 1 or num > len(self.table_info['players']):
                return False
            return True
        except ValueError:
            return False

    def isCard(self, s: str) -> bool:
        """
        检查参数是否符合卡牌格式要求: 玩家标识后跟.和一个字母
        例如: "p1.a", "p2.b" 等
        """
        if not isinstance(s, str) or not s:
            return False
        parts = s.split('.')
        if len(parts) != 2:
            return False
        if not self.isPlayer(parts[0]):
            return False
        if len(parts[1]) == 1 and parts[1].isalpha():
            num = int(ord(parts[1].lower()) - ord('a') + 1)
            player = self.table_info['players'][num - 1]
            if num < 1 or num > len(player.pokers):
                return False
            return True
        return False


    def add_input(self, input_queue, stub):
        while True:
            try:
                _input = input("").lower()
                parts = _input.split(' ')
                if len(parts) > 5:
                    print('Invalid parameter numbers')
                    continue
                parts += [None] * (5 - len(parts))
                action = parts[0]
                for arg in parts[1:]:
                    if arg is not None:
                        pass
                arg1 = parts[1]
                arg2 = parts[2]
                arg3 = parts[3]
                arg4 = parts[4]
                arg5 = parts[5]
                if action == 'exit':
                    break
                elif action == 'ready':
                    pass
                elif action == 'cancel':
                    pass
                elif action == 'skill':
                    pass
                elif action == 'card':
                    pass
                else:
                    print('Unknown action: {}'.format(action))
                    continue
                self.sendMessage(action, arg1, arg2, arg3, arg4, arg5)
            except KeyboardInterrupt:
                pass
            except Exception as ex:
                self.gm.refresh(username=self.username)

    def __listen_for_messages(self):
        # 从服务器接收新消息并显示
        subscribeResps = self.stub.Subscribe(pb2.GeneralRequest(name=self.username))
        subscribeResp = next(subscribeResps)
        if subscribeResp is None:
            print('Failed to subscribe game.')
            return
        print('Successfully joined the game.')
        self.gm.refresh_ready()
        for resp in subscribeResps:
            if resp.type == pb2.Broadcast.UNSPECIFIED:
                print(f'Unspecified: {resp.msg}')
            elif resp.type == pb2.Broadcast.FAILURE:
                print(f'Failure: {resp.msg}')
            elif resp.type == pb2.Broadcast.USER_JOIN:
                print(f'{resp.name} has joined the game.')
                self.gm.player_join(resp.name)
                self.gm.ready_status[resp.name] = False
                self.gm.refresh_ready()
            elif resp.type == pb2.Broadcast.USER_LEAVE:
                print(f'{resp.name} has lefted the game.')
                self.gm.player_exit(resp.msg)
                self.gm.refresh_ready()
            elif resp.type == pb2.Broadcast.USER_READY:
                body = json.loads(resp.msg)
                self.gm.ready_status = body
                if self.gm.accept_ready_message:
                    self.gm.refresh_ready()
            elif resp.type == pb2.Broadcast.GAME_START:
                self.gm.clear_score()
                self.gm.game_status = GameStatus.PLAYING.value
            elif resp.type == pb2.Broadcast.NEW_ROUND:
                msg = json.loads(resp.msg)
                _seed = msg['seed']
                _order = msg['order']
                _peek = msg['peek']
                # mask_peek = dict()
                # mask_peek[self.username] = _peek[self.username]
                self.gm.new_round(_seed, _order, peek_dict=_peek)
                self.gm.refresh(username=self.username)
            elif resp.type == pb2.Broadcast.GAME_END:
                self.gm.game_end()
            elif resp.type == pb2.Broadcast.ROUND_END:
                self.gm.round_end()
            elif resp.type == pb2.Broadcast.PLAYER_TURN:
                print(f'{resp.msg}\'s turn.')
                self.gm.turnorder.setCurrent(resp.msg)
                self.gm.refresh(username=self.username)
            elif resp.type == pb2.Broadcast.PLAYER_ACTION:
                print(f'{resp.name} do: {resp.msg}')
                self.gm.handle(resp)
                self.gm.refresh(msg=resp, username=self.username)
            else:
                print(f'Unknown message: {resp}')

    def sendMessage(self, action, arg1=None, arg2=None, arg3=None, arg4=None, arg5=None):
        msg = {
            'action': action, 'arg1': arg1, 'arg2': arg2, 'arg3': arg3, 'arg4': arg4, 'arg5': arg5
        }
        resp = self.stub.Handle(pb2.GeneralRequest(sender=self.username, body=json.dumps(msg)))
        if not resp.status:
            pass
        print(resp.msg)



def main(address='localhost', port=50051, username=None):
    chars = string.ascii_letters
    if username is None:
        username = ''.join(random.choice(chars) for _ in range(5))
    client = Client(username, address, port)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')


if __name__ == '__main__':
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     print('Bye')
    RefreshScreen(test_dict)
