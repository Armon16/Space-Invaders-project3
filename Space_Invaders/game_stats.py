class GameStats:


    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start game in an inactive state.
        self.game_active = False
        self.high_score_active = False
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        # High score should never be reset.
        scoresheet = open('scoresheet.txt', 'r')
        self.high_score = int(scoresheet.read())

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
