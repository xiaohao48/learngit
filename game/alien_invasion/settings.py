class Settings():

    def __init__(self):
        # 屏幕属性
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船属性
        self.ship_limit = 3

        # 子弹属性
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 30
        # self.bullet_speed_factor = 10
        # 外星人属性
        self.fleet_drop_speed = 10

        self.alien_points = 50

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.3

        self.fleet_direction = 1

    def increate_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
