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
from HyperTexas.game.game_enum import GameStatus, LobbyAction, TurnAction
import HyperTexas.protocol.service_pb2 as pb2
import HyperTexas.protocol.service_pb2_grpc as rpc
from HyperTexas.game.manager import Manager
from HyperTexas.game.poker import Poker
from HyperTexas.game.card import Card
from HyperTexas.game.effects import *
from HyperTexas.game.ui import RefreshScreen


class Client:
    def __init__(self, username: str, address='localhost', port=50051):
        self.username = username
        # 创建 gRPC 通道和存根
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.stub = rpc.LobbyStub(channel)
        # 启动一个新线程监听消息
        self.table_info = dict()
        self.running = True  # 添加运行状态标志
        retry = 0
        loginResp = self.sendMessage(LobbyAction.LOGIN.value, self.username, None, None, None, None)
        if loginResp.status != 200:
            print('Failed to login lobby: {}'.format(loginResp.msg))
            return
        self.listening_thread = threading.Thread(target=self.__listen_for_messages, daemon=True)
        self.listening_thread.start()
        # 初始化lobby
        self.sendMessage(LobbyAction.SYNC.value, self.username, None, None, None, None)
        self.input_thread = threading.Thread(target=self.add_input, daemon=True)
        self.input_thread.start()

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


    def add_input(self):
        # 从控制台获取输入并发送到服务器
        while self.running:
            try:
                # 等待用户输入
                command = input('> ')
                if not command:
                    continue
                # 解析命令和参数
                parts = command.strip().split()
                action = parts[0]
                arg1 = parts[1] if len(parts) > 1 else None
                arg2 = parts[2] if len(parts) > 2 else None
                arg3 = parts[3] if len(parts) > 3 else None
                arg4 = parts[4] if len(parts) > 4 else None
                arg5 = parts[5] if len(parts) > 5 else None                
                print('Command received:', action)
                if action == 'exit':
                    print('Exiting game...')
                    self.sendMessage(LobbyAction.LOGOUT.value, self.username, arg2, arg3, arg4, arg5)
                    self.running = False  # 设置运行状态为False
                    os._exit(0)  # 强制结束所有线程
                    break
                if action == 'sync':
                    self.sendMessage(LobbyAction.SYNC.value, self.username, arg2, arg3, arg4, arg5)
                # 根据游戏状态处理不同的命令
                if self.table_info.get('game_status') == GameStatus.LOBBY.value:
                    if action == LobbyAction.READY.value:
                        print(self.table_info)
                        self.sendMessage(action, self.username, arg2, arg3, arg4, arg5)
                    if action == LobbyAction.CANCEL.value:
                        self.sendMessage(action, self.username, arg2, arg3, arg4, arg5)
                    if action == LobbyAction.START_GAME.value:
                        self.sendMessage(action, self.username, arg2, arg3, arg4, arg5)
                if self.table_info.get('game_status') == GameStatus.GAME.value:
                    if action in ['skill', 'card']:
                        self.sendMessage(action, arg1, arg2, arg3, arg4, arg5)
                    else:
                        print('In game, available commands: skill, card, exit')
                if self.table_info.get('game_status') == GameStatus.WAIT_PLAY.value:
                    self.sendMessage(TurnAction.PLAY_CARD.value, arg1, arg2, arg3, arg4, arg5)
                if self.table_info.get('game_status') == GameStatus.SCORE.value:
                    pass
                    
            except KeyboardInterrupt:
                print('\nReceived keyboard interrupt, exiting...')
                self.sendMessage(LobbyAction.LOGOUT.value, self.username)
                self.running = False  # 设置运行状态为False
                os._exit(0)  # 强制结束所有线程
                break
            except Exception as ex:
                print('Error processing command:', str(ex))

    def __listen_for_messages(self):
        # 从服务器接收新消息并显示
        try:
            subscribeResps = self.stub.Subscribe(pb2.GeneralRequest(sender=self.username, body=json.dumps(dict())))
            subscribeResp = next(subscribeResps)
            if subscribeResp is None:
                print('Failed to subscribe game.')
                return
            print('Successfully joined the game.')
            for resp in subscribeResps:
                if not self.running:  # 检查运行状态
                    break
                self.table_info = json.loads(resp.body)
                RefreshScreen(self.username, self.table_info)
        except Exception as ex:
            if self.running:  # 只在正常运行时打印错误
                print('Error in message listener:', str(ex))

    def sendMessage(self, action, arg1=None, arg2=None, arg3=None, arg4=None, arg5=None):
        msg = {
            'action': action, 'arg1': arg1, 'arg2': arg2, 'arg3': arg3, 'arg4': arg4, 'arg5': arg5
        }
        resp = self.stub.Handle(pb2.GeneralRequest(sender=self.username, body=json.dumps(msg)))
        print('Server response: ', resp)
        return resp



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

