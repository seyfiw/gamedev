from kivy.core.window import Window

class Camera:
    def __init__(self, game_map, player):
        self.game_map = game_map
        self.player = player

    def update(self):
        camera_offset_x = Window.width // 2 - self.player.position[0] - self.player.sprite.size[0] // 2
        camera_offset_y = Window.height // 2 - self.player.position[1] - self.player.sprite.size[1] // 2
        camera_speed = 0.1
        self.game_map.background.pos = (
            self.game_map.background.pos[0] + (camera_offset_x - self.game_map.background.pos[0]) * camera_speed,
            self.game_map.background.pos[1] + (camera_offset_y - self.game_map.background.pos[1]) * camera_speed
        )