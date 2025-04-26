from enum import Enum

class GameStatus(Enum):
    LOBBY = 'lobby'                     # 大厅内 游戏未开始
    GAME = 'game'                      # 游戏进行中
    SCORE = 'score'                     # 计分环节

class LobbyAction(Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    READY = 'ready'
    CANCEL = 'cancel'
    START_GAME = 'start'
    KICK = 'kick'

class TurnAction(Enum):
    PASS = 'pass'
    USE_CARD = 'card'
    USE_SKILL = 'skill'
    FOLD = 'fold'

# class BroadcastType(Enum):
#     HEARTBEAT = 0
#     UPDATE_STATUS = 1
#     SET_CURRENT_PLAYER = 2
#     SYNC = 3
#     START_TIMER = 4
#     TIMEOUT = 5
#     CONFIRM_ACTION = 6
