from enum import Enum

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
