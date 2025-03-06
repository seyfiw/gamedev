from kivy.core.window import Window

class Camera:
    def __init__(self, game_map, player):
        self.game_map = game_map
        self.player = player

    def update(self):
        camera_offset_x = Window.width // 2 - self.player.position[0] - self.player.sprite.size[0] // 2
        camera_offset_y = Window.height // 2 - self.player.position[1] - self.player.sprite.size[1] // 2

        new_x = self.game_map.background.pos[0] + (camera_offset_x - self.game_map.background.pos[0]) * 0.1
        new_y = self.game_map.background.pos[1] + (camera_offset_y - self.game_map.background.pos[1]) * 0.1

        #print(f"Camera: background.pos = ({new_x}, {new_y})")

        min_x = Window.width - self.game_map.size[0]
        min_y = Window.height - self.game_map.size[1]
        new_x = max(min_x, min(0, new_x))
        new_y = max(min_y, min(0, new_y))

        self.game_map.background.pos = (new_x, new_y)
        
     