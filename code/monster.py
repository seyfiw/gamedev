from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math

class Monster(Image):
    def __init__(self, name, spawn_point, image_path, game_map, animations=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.spawn_point = spawn_point 
        self.source = image_path
        self.size_hint = (None, None)
        self.size = (200, 200)
        self.scale = 5.0
        self.allow_stretch = True  # อนุญาตให้ขยายภาพ
        self.keep_ratio = False  # ไม่ต้องรักษาอัตราส่วน
        self.game_map = game_map
        self.max_hp = 50  # เลือดสูงสุด
        self.hp = self.max_hp  # เลือดปัจจุบัน
        
        self.world_position = list(spawn_point)
        self.original_position = list(spawn_point)
        
        self.pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )

        if animations is not None:
            self.animations = animations
        else:
            self.animations = self.load_default_animations()
            
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.2  # เวลาเปลี่ยนเฟรม (วินาที)
        
        # เริ่ม Animation
        Clock.schedule_interval(self.update_animation, self.animation_speed)
        

        #with self.canvas.after:
        #    Color(1, 0, 0, 0.5)
        #    self.rect = Rectangle(size=self.size, pos=self.pos)
            
        # เอาไว้ debug ก่อน
        #from kivy.uix.label import Label
        #self.label = Label(text=self.name, color=(1,1,1,1), pos=self.pos, size=self.size)
        #self.add_widget(self.label)
        
        self.movement_range = 50  # ระยะห่างสูงสุดจากจุดเริ่มต้น
        self.movement_speed = 2  # ความเร็วในการเคลื่อนที่
        self.current_direction = random.choice(["left", "right", "up", "down"])
        self.direction_change_time = 0
        self.direction_change_interval = 5  
        
        Clock.schedule_interval(self.move, 1 / 30)
        
        
    def load_default_animations(self):
        if self.name == "Red":
            return {
                "walk_left": ["../image/red/L/redL1.png", "../image/red/L/redL2.png","../image/red/L/redL3.png", "../image/red/L/redL4.png"],
            "walk_right": ["../image/red/R/redR1.png", "../image/red/R/redR2.png","../image/red/R/redR3.png", "../image/red/R/redR4.png"],
            "idle": ["../image/red/R/redR1.png", "../image/red/R/redR2.png","../image/red/R/redR3.png", "../image/red/R/redR4.png"],
            "death": ["../image/red/R/redR1.png", "../image/red/R/redR2.png","../image/red/R/redR3.png", "../image/red/R/redR4.png"],
            }
        elif self.name == "Stone":
            return {
                "walk_left": ["../image/stone/L/StoneL1.png", "../image/stone/L/StoneL2.png", "../image/stone/L/StoneL3.png", "../image/stone/L/StoneL4.png", "../image/stone/L/StoneL5.png"],
                "walk_right": ["../image/stone/R/StoneR1.png", "../image/stone/R/StoneR2.png", "../image/stone/R/StoneR3.png", "../image/stone/R/StoneR4.png", "../image/stone/R/StoneR5.png"],
                "idle": ["../image/stone/R/StoneR1.png", "../image/stone/R/StoneR2.png", "../image/stone/R/StoneR3.png", "../image/stone/R/StoneR4.png", "../image/stone/R/StoneR5.png"],
                "death": ["../image/stone/R/StoneR1.png", "../image/stone/R/StoneR2.png", "../image/stone/R/StoneR3.png", "../image/stone/R/StoneR4.png", "../image/stone/R/StoneR5.png"],
            }
            
        elif self.name == "Golem":
            return {
                "walk_left": ["../image/golem/Idle/Golem1.png", "../image/golem/Idle/Golem2.png", "../image/golem/Idle/Golem3.png", "../image/golem/Idle/Golem4.png", "../image/golem/Idle/Golem5.png"],
                "walk_right": ["../image/golem/Idle/Golem1.png", "../image/golem/Idle/Golem2.png", "../image/golem/Idle/Golem3.png", "../image/golem/Idle/Golem4.png", "../image/golem/Idle/Golem5.png"],
                "idle": ["../image/golem/Idle/Golem1.png", "../image/golem/Idle/Golem2.png", "../image/golem/Idle/Golem3.png", "../image/golem/Idle/Golem4.png", "../image/golem/Idle/Golem5.png"],
                "death": ["../image/golem/Idle/Golem1.png", "../image/golem/Idle/Golem2.png", "../image/golem/Idle/Golem3.png", "../image/golem/Idle/Golem4.png", "../image/golem/Idle/Golem5.png"],
            }
            
        elif self.name == "Dragon":
            return {
                "walk_left": ["../image/dragon/L/dragonL1.png", "../image/dragon/L/dragonL2.png", "../image/dragon/L/dragonL3.png", "../image/dragon/L/dragonL4.png", "../image/dragon/L/dragonL5.png"],
                "walk_right": ["../image/dragon/R/dragonR1.png", "../image/dragon/R/dragonR2.png", "../image/dragon/R/dragonR3.png", "../image/dragon/R/dragonR4.png", "../image/dragon/R/dragonR5.png"],
                "idle": ["../image/dragon/R/dragonR1.png", "../image/dragon/R/dragonR2.png", "../image/dragon/R/dragonR3.png", "../image/dragon/R/dragonR4.png", "../image/dragon/R/dragonR5.png"],
                "death": ["../image/dragon/R/dragonR1.png", "../image/dragon/R/dragonR2.png", "../image/dragon/R/dragonR3.png", "../image/dragon/R/dragonR4.png", "../image/dragon/R/dragonR5.png"],
            }
        
    def update_animation(self, dt):
        frames = self.animations[self.current_animation]
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.source = frames[self.current_frame]
    
    def move(self, dt):
        self.direction_change_time += dt
        
        if self.direction_change_time >= self.direction_change_interval:
            self.current_direction = random.choice(["left", "right", "up", "down", "idle"])
            self.direction_change_time = 0
            
            if self.current_direction == "left":
                self.current_animation = "walk_left"
            elif self.current_direction == "right":
                self.current_animation = "walk_right"
            else:
                self.current_animation = "idle"
        
        new_position = list(self.world_position)
        
        if self.current_direction == "left":
            new_position[0] -= self.movement_speed
        elif self.current_direction == "right":
            new_position[0] += self.movement_speed
        elif self.current_direction == "up":
            new_position[1] += self.movement_speed
        elif self.current_direction == "down":
            new_position[1] -= self.movement_speed
        
        distance_from_origin = math.sqrt(
            (new_position[0] - self.original_position[0])**2 + 
            (new_position[1] - self.original_position[1])**2
        )
        
        if distance_from_origin <= self.movement_range:
            self.world_position = new_position
        else:
            if self.world_position[0] < self.original_position[0]:
                self.current_direction = "right"
                self.current_animation = "walk_right"
            elif self.world_position[0] > self.original_position[0]:
                self.current_direction = "left"
                self.current_animation = "walk_left"
            elif self.world_position[1] < self.original_position[1]:
                self.current_direction = "up"
            elif self.world_position[1] > self.original_position[1]:
                self.current_direction = "down"

    def update_position(self):
        new_pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )

        #is_visible = (
            #0 <= new_pos[0] <= Window.width and
            #0 <= new_pos[1] <= Window.height
        #)
        
        #if is_visible and self.pos != new_pos:
            #print(f"Monster {self.name} world pos: ({self.world_position[0]}, {self.world_position[1]})")
            #print(f"Monster {self.name} screen pos: ({new_pos[0]}, {new_pos[1]})")
            #print(f"Map background pos: ({self.game_map.background.pos[0]}, {self.game_map.background.pos[1]})")

        if self.pos != new_pos:
            self.pos = new_pos
            #self.rect.pos = self.pos  
            #self.label.pos = new_pos  
           
    #monster die        
    def die(self):
        self.current_animation = "death"
        self.current_frame = 0

        def remove_monster(dt):
            if self.parent:
                self.parent.remove_widget(self)  # ลบ Monster ออกจากหน้าจอ
            
        Clock.schedule_once(remove_monster, len(self.animations["death"]) * self.animation_speed)