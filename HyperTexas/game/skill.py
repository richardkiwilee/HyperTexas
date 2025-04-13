from HyperTexas.game.character import Character
from HyperTexas.game.manager import Manager
from HyperTexas.game.effects import *

class Skill:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, manager: Manager, user: Character, target: dict):
        pass


class Skill1(Skill):
    def __init__(self):
        super().__init__('Skill1', 'Skill1 description')
    
    def use(self, manager: Manager, user: Character, target: dict):
        user.effects.append(BUFF_0x0001)

