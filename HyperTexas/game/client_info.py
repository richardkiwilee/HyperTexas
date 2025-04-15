from .player import PlayerInfo


class ClientInfo:
    def __init__(self):
        self.current_player_index = 0 # 当前用户的下标
        self.users = []     # 记录玩家信息
        self.public_cards = []      # 公共牌信息
        self.last_used_cards = []   # 弃牌堆信息
        self.deck = []  # 牌堆信息

    def Reset(self):
        self.current_player_index = 0
        self.users = []
        self.public_cards = []
        self.last_used_cards = []
        self.deck = []

    def UpdateUserInfo(self, info: dict):
        if info.get('current_player_index'):
            self.current_player_index = info.get('current_player_index')
        if info.get('users'):
            self.users = [PlayerInfo(_) for _ in info.get('users')]
        if info.get('public_cards'):
            self.public_cards = info.get('public_cards')
        if info.get('last_used_cards'):
            self.last_used_cards = info.get('last_used_cards')
        if info.get('deck'):
            self.deck = info.get('deck')
