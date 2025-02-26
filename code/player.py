from kivy.uix.image import Image
from kivy.vector import Vector

class Player:
    def __init__(self, image_path, game_map):
        self.sprite = Image(source=image_path, size=(64, 64))
        self.position = [game_map.size[0] // 2, game_map.size[1] // 2]  
        self.game_map = game_map

    def update(self, dt, pressed_keys):
        step_size = Vector(500 * dt, 500 * dt)
        new_position = Vector(self.position)

        if "w" in pressed_keys:
            new_position += Vector(0, step_size.y)
        if "s" in pressed_keys:
            new_position -= Vector(0, step_size.y)
        if "a" in pressed_keys:
            new_position -= Vector(step_size.x, 0)
        if "d" in pressed_keys:
            new_position += Vector(step_size.x, 0)

        player_size = self.sprite.size
        check_points = [
            (new_position[0], new_position[1]), 
            (new_position[0] + player_size[0], new_position[1]),  
            (new_position[0], new_position[1] + player_size[1]),  
            (new_position[0] + player_size[0], new_position[1] + player_size[1]),  
            (new_position[0] + player_size[0]/2, new_position[1] + player_size[1]/2)  
        ]

        can_move = all(self.game_map.is_position_valid(x, y) for x, y in check_points)

        if can_move:
            self.position = [
                max(0, min(self.game_map.size[0] - player_size[0], new_position[0])),
                max(0, min(self.game_map.size[1] - player_size[1], new_position[1]))
            ]