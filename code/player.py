from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.clock import Clock



class Player:
    def __init__(self, image_path, game_map):
        self.sprite = Image(source=image_path, size=(64, 64), size_hint=(None, None))
        self.position = [game_map.size[0] // 2, game_map.size[1] // 2]
        self.game_map = game_map
        self.animations = {
            "walk_left": ["../image/Wl1.png", "../image/Wl1.png","../image/Wl1.png","../image/Wl1.png","../image/Wl1.png",
                          "../image/Wl2.png", "../image/Wl3.png", "../image/Wl4.png", "../image/Wl4.png"
                          , "../image/Wl4.png", "../image/Wl3.png","../image/Wl2.png",
                          "../image/Wl1.png","../image/Wl1.png","../image/Wl1.png","../image/Wl1.png","../image/Wl1.png"],
            "walk_right": ["../image/Wr1.png","../image/Wr1.png","../image/Wr1.png", "../image/Wr2.png", "../image/Wr3.png", "../image/Wr4.png", "../image/Wr4.png"
                           , "../image/Wr4.png", "../image/Wr3.png","../image/Wr2.png","../image/Wr1.png","../image/Wr1.png","../image/Wr1.png","../image/Wr1.png"],
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
class SwordAttack:
    def __init__(self, player, game_map):
        self.player = player
        self.game_map = game_map
        self.is_attacking = False
        self.attack_cooldown = 0
        self.max_cooldown = 0.5  # 0.5 วินาทีระหว่างการโจมตีแต่ละครั้ง
        self.attack_duration = 0.3  # 0.3 วินาทีสำหรับการแสดงอนิเมชั่นการโจมตี
        self.attack_timer = 0
        
        # สร้าง sprite สำหรับดาบ
        self.sword_sprite = Image(
            source="../image/Sword_1.png",
            size=(48, 48),
            size_hint=(None, None),
            opacity=0  # ซ่อนเมื่อไม่ได้ใช้งาน
        )
        
        # เพิ่มดาบลงใน game_map
        self.game_map.add_widget(self.sword_sprite)
        
        # สร้างอนิเมชั่นสำหรับการโจมตี
        self.attack_animations = {
            "attack_left": ["../image/Sword_1.png"],
            "attack_right": ["../image/Sword_1.png"]
        }
        
        # ระยะการโจมตี
        self.attack_range = 50
        
        # ความเสียหายจากการโจมตี
        self.attack_damage = 10
        
        # เป้าหมายที่ถูกโจมตี
        self.attack_targets = []
    
    def update(self, dt, pressed_keys):
        # อัพเดทเวลา cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # ตรวจสอบการกดปุ่มโจมตี (space)
        if " " in pressed_keys and not self.is_attacking and self.attack_cooldown <= 0:
            self.start_attack()
        
        # อัพเดทอนิเมชั่นการโจมตี
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.end_attack()
            else:
                self.update_sword_position()
    
    def start_attack(self):
        # เริ่มการโจมตี
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.sword_sprite.opacity = 1
        
        # กำหนดทิศทางการโจมตีตามทิศทางของตัวละคร
        if self.player.current_animation == "walk_left":
            self.current_attack_animation = "attack_left"
        else:
            self.current_attack_animation = "attack_right"
        
        # ตำแหน่งการโจมตี
        self.update_sword_position()
        
        # เล่นเสียงการโจมตี (ถ้ามี)
        # self.play_attack_sound()
        
        # ตรวจสอบการชนกับเป้าหมาย
        self.check_attack_collision()
    
    def end_attack(self):
        # จบการโจมตี
        self.is_attacking = False
        self.attack_cooldown = self.max_cooldown
        self.sword_sprite.opacity = 0
    
    def update_sword_position(self):
        # อัพเดทตำแหน่งของดาบตามทิศทางของตัวละคร
        player_pos = Vector(self.player.position)
        player_size = self.player.sprite.size
        
        # คำนวณตำแหน่งของดาบตามทิศทางการโจมตี
        if self.current_attack_animation == "attack_left":
            # โจมตีไปทางซ้าย
            sword_pos = Vector(
                player_pos.x - self.sword_sprite.width * 0.75,
                player_pos.y + player_size[1] * 0.3
            )
            # หมุนดาบ (ถ้าจำเป็น)
            self.sword_sprite.rotation = 0
        else:
            # โจมตีไปทางขวา
            sword_pos = Vector(
                player_pos.x + player_size[0] * 0.75,
                player_pos.y + player_size[1] * 0.3
            )
            # หมุนดาบ (ถ้าจำเป็น)
            self.sword_sprite.rotation = 180
        
        # อัพเดทตำแหน่ง
        self.sword_sprite.pos = (
            sword_pos.x + self.game_map.background.pos[0],
            sword_pos.y + self.game_map.background.pos[1]
        )
    
    def check_attack_collision(self):
        # ตรวจสอบการชนกับเป้าหมาย (ศัตรู)
        player_pos = Vector(self.player.position)
        attack_direction = Vector(0, 0)
        
        # กำหนดทิศทางการโจมตี
        if self.current_attack_animation == "attack_left":
            attack_direction = Vector(-1, 0)
        else:
            attack_direction = Vector(1, 0)
        
        # คำนวณพื้นที่การโจมตี
        attack_center = player_pos + attack_direction * self.attack_range
        
        # ตรวจสอบการชนกับเป้าหมายทุกตัวในรายการ
        for target in self.attack_targets:
            target_pos = Vector(target.position)
            
            # คำนวณระยะห่างระหว่างเป้าหมายกับจุดกลางของการโจมตี
            distance = (target_pos - attack_center).length()
            
            # ถ้าเป้าหมายอยู่ในระยะการโจมตี
            if distance < self.attack_range:
                # โจมตีเป้าหมาย
                self.hit_target(target)
    
    def hit_target(self, target):
        # ทำความเสียหายกับเป้าหมาย
        if hasattr(target, 'take_damage'):
            target.take_damage(self.attack_damage)
    
    def add_attack_target(self, target):
        # เพิ่มเป้าหมายในรายการเป้าหมายที่สามารถโจมตีได้
        if target not in self.attack_targets:
            self.attack_targets.append(target)
    
    def remove_attack_target(self, target):
        # ลบเป้าหมายออกจากรายการ
        if target in self.attack_targets:
            self.attack_targets.remove(target)
