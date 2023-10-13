from Config import PLAYER_INIT_X


class Info_send:
    def __init__(self):
        self.state = None
        self.remaining_time = None
        self.win = -1
        self.player_pos = PLAYER_INIT_X
        self.bullet_pos = []
        self.survive = True
        self.magazine = 10


class Game:
    def __init__(self):
        self.state = 'not ready'
        self.win = -1
        self.player_pos = [PLAYER_INIT_X, PLAYER_INIT_X]
        self.bullet_pos = [[], []]
        self.target_num = '30'
        self.magazines = [10, 10]
