from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.clock import Clock

class Player:
    def __init__(self, image_path, game_map, max_hp=100, max_mana=100):
        self.sprite = Image(source=image_path, size=(100, 100), size_hint=(None, None), allow_stretch=True, keep_ratio=False)
        self.position = [game_map.size[0] // 2, game_map.size[1] // 2]
        self.game_map = game_map
        self.max_hp = max_hp
        self.hp = max_hp  # เลือดปัจจุบัน
        self.max_mana = max_mana  # เพิ่ม max_mana
        self.mana = max_mana
        self.skills = {
            "Fireball": {"damage": 20, "mana_cost": 30},
            "Heal": {"heal": 30, "mana_cost": 15},
        }
        self.mana = 100  
        self.animations = {
            "walk_left": ["../image/player/Wl1.png", "../image/player/Wl1.png","../image/player/Wl1.png","../image/player/Wl1.png","../image/player/Wl1.png",
                          "../image/player/Wl2.png", "../image/player/Wl3.png", "../image/player/Wl4.png", "../image/player/Wl4.png"
                          , "../image/player/Wl4.png", "../image/player/Wl3.png","../image/player/Wl2.png",
                          "../image/player/Wl1.png","../image/player/Wl1.png","../image/player/Wl1.png","../image/player/Wl1.png","../image/player/Wl1.png"],
            "walk_right": ["../image/player/Wr1.png","../image/player/Wr1.png","../image/player/Wr1.png", "../image/player/Wr2.png", "../image/player/Wr3.png", "../image/player/Wr4.png", "../image/player/Wr4.png"
                           , "../image/player/Wr4.png", "../image/player/Wr3.png","../image/player/Wr2.png","../image/player/Wr1.png","../image/player/Wr1.png","../image/player/Wr1.png","../image/player/Wr1.png"],
            "attack": ["../image/player/attack1.png", "../image/player/attack2.png", "../image/player/attack3.png"],
            "cast_fireball": ["../image/player/fireball1.png", "../image/player/fireball2.png", "../image/player/fireball3.png"],
            "heal": ["../image/player/heal1.png", "../image/player/heal2.png", "../image/player/heal3.png"],
            "defend": ["../image/player/defend1.png", "../image/player/defend2.png", "../image/player/defend3.png"],
        
        
        }
        self.current_animation = "walk_left"
        self.current_frame = 0
        self.animation_interval = 0.1
        Clock.schedule_interval(self.update_animation, self.animation_interval)

    def update(self, dt, pressed_keys):
        step_size = Vector(500 * dt, 500 * dt)
        new_position = Vector(self.position)

        if "w" in pressed_keys:
            new_position += Vector(0, step_size.y)
        if "s" in pressed_keys:
            new_position -= Vector(0, step_size.y)
        if "a" in pressed_keys:
            new_position -= Vector(step_size.x, 0)
            self.move_left()
        if "d" in pressed_keys:
            new_position += Vector(step_size.x, 0)
            self.move_right()

        # ตรวจสอบว่าสามารถเคลื่อนที่ไปยังตำแหน่งใหม่ได้หรือไม่
        player_size = self.sprite.size
        check_points = [
            (new_position[0], new_position[1]),
            (new_position[0] + player_size[0], new_position[1]),
            (new_position[0], new_position[1] + player_size[1]),
            (new_position[0] + player_size[0], new_position[1] + player_size[1]),
            (new_position[0] + player_size[0] / 2, new_position[1] + player_size[1] / 2)
        ]

        can_move = all(self.game_map.is_position_valid(x, y) for x, y in check_points)

        if can_move:
            self.position = [
                max(0, min(self.game_map.size[0] - player_size[0], new_position[0])),
                max(0, min(self.game_map.size[1] - player_size[1], new_position[1]))
            ]
            
        self.sprite.pos = (
            self.position[0] + self.game_map.background.pos[0],
            self.position[1] + self.game_map.background.pos[1]
        )

    def update_animation(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
        self.sprite.source = self.animations[self.current_animation][self.current_frame]

    def move_left(self):
        self.current_animation = "walk_left"

    def move_right(self):
        self.current_animation = "walk_right"

    def idle(self):
        pass