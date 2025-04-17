class Card:
    def __init__(self):
        self.visible = []
        self.func = None
    
    def call(self, arg1, arg2, arg3, arg4, arg5):
        if self.func:
            self.func(arg1, arg2, arg3, arg4, arg5)

    def from_dict(self, d: dict):
        self.func = d.get('func')
        self.visible = d.get('visible')

    def to_dict(self):
        return {
            'func': self.func,
            'visible': self.visible
        }