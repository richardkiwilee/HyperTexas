LEVEL_SCORE = [150, 300, 450, 600, 800, 1200, 1600, 2000, 3000, 4000, 5000, 7500, 10000, 15000, 20000, 30000, 40000, 50000, 75000, 100000]

class Level:
    def __init__(self):
        self.current_level = 0

    def GetTargetScore(self):
        if self.current_level < len(LEVEL_SCORE):
            return LEVEL_SCORE[self.current_level]
        return (self.current_level - len(LEVEL_SCORE) + 1) * 50000 + 100000

    def NextLevel(self):
        self.current_level += 1
