class Settings():

    def __init__(self):
        # 屏幕属性
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船属性
        self.ship_speed_factor = 1.5

        # 子弹属性
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3
