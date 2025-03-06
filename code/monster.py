from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math

class Monster(Image):
    def __init__(self, name, spawn_point, image_path, game_map, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.spawn_point = spawn_point 
        self.source = image_path
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.game_map = game_map
        
        self.world_position = list(spawn_point)
        self.original_position = list(spawn_point)
        
        self.pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )
        
        

        with self.canvas.after:
            Color(1, 0, 0, 0.5)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        # เอาไว้ debug ก่อน
        from kivy.uix.label import Label
        self.label = Label(text=self.name, color=(1,1,1,1), pos=self.pos, size=self.size)
        self.add_widget(self.label)
        
        self.movement_range = 50  # ระยะห่างสูงสุดจากจุดเริ่มต้น
        self.movement_speed = 2  # ความเร็วในการเคลื่อนที่
        self.current_direction = random.choice(["left", "right", "up", "down"])
        self.direction_change_time = 0
        self.direction_change_interval = 5  
        
        self.animations = {
            "walk_left": ["../image/Wl1.png"],
            "walk_right": ["../image/Wl1.png"],
            "idle": ["../image/Wl1.png"],
        }
        
        for key in self.animations:
            for i in range(len(self.animations[key])):
                self.animations[key][i] = image_path
        
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_interval = 0.2
        
        Clock.schedule_interval(self.update_animation, self.animation_interval)
        Clock.schedule_interval(self.move, 1/30)
        
    def update_animation(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
        self.source = self.animations[self.current_animation][self.current_frame]
    
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
            self.rect.pos = self.pos  
            self.label.pos = new_pos  