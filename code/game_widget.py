from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.image import Image
from PIL import Image as PILImage
import os

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
        map_path = "image/map1-4.png"
        try:
            with PILImage.open(map_path) as img:
                self.map_size = img.size
                print(f"Loaded map size: {self.map_size}")
        except Exception as e:
            print(f"Error loading map: {e}")
            self.map_size = (10240, 10240)
            
        self.player_position = [self.map_size[0] // 2, self.map_size[1] // 2]
        
        self.background = Image(source=map_path, size=self.map_size)
        self.collision_map = self.create_collision_map(map_path)
        
        self.player = Image(source="image/removed-background.png", size=(64, 64))
        self.add_widget(self.background)
        self.add_widget(self.player)
        
        self._keyPressed = set()
        Clock.schedule_interval(self.update, 1/60)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1] if keycode[1] else text
        self._keyPressed.add(key)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        key = keycode[1] if keycode[1] else ""
        if key in self._keyPressed:
            self._keyPressed.remove(key)
        return True

    def create_collision_map(self, map_path):
        """สร้าง collision map จากไฟล์ภาพ"""
        try:
            return PILImage.open(map_path).convert('RGBA')
        except Exception as e:
            print(f"Error creating collision map: {e}")
            return None

    def is_valid_position(self, x, y):
        """ตรวจสอบว่าตำแหน่งที่จะเดินไปนั้นสามารถเดินได้หรือไม่"""
        if not self.collision_map:
            return True

        try:
            img_x = max(0, min(int(x), self.map_size[0] - 1))
            img_y = max(0, min(int(self.map_size[1] - y), self.map_size[1] - 1))
            
            pixel = self.collision_map.getpixel((img_x, img_y))
            is_opaque = pixel[3] >= 250  
            
            return is_opaque
        except Exception as e:
            print(f"Error checking position ({x}, {y}): {e}")
            return False

    def update(self, dt):
        step_size = Vector(500 * dt, 500 * dt) 
        new_position = Vector(self.player_position)
        old_position = Vector(self.player_position)

       
        if "w" in self._keyPressed:
            new_position += Vector(0, step_size.y)
        if "s" in self._keyPressed:
            new_position -= Vector(0, step_size.y)
        if "a" in self._keyPressed:
            new_position -= Vector(step_size.x, 0)
        if "d" in self._keyPressed:
            new_position += Vector(step_size.x, 0)

        
        player_size = self.player.size
        check_points = [
            (new_position[0], new_position[1]), 
            (new_position[0] + player_size[0], new_position[1]),  
            (new_position[0], new_position[1] + player_size[1]),  
            (new_position[0] + player_size[0], new_position[1] + player_size[1]),  
            (new_position[0] + player_size[0]/2, new_position[1] + player_size[1]/2)  
        ]

       
        can_move = all(self.is_valid_position(x, y) for x, y in check_points)

        if can_move:
            self.player_position = [
                max(0, min(self.map_size[0] - player_size[0], new_position[0])),
                max(0, min(self.map_size[1] - player_size[1], new_position[1]))
            ]
        else:
            self.player_position = old_position

        camera_offset_x = Window.width // 2 - self.player_position[0] - self.player.size[0] // 2
        camera_offset_y = Window.height // 2 - self.player_position[1] - self.player.size[1] // 2

        camera_speed = 0.1
        self.background.pos = (
            self.background.pos[0] + (camera_offset_x - self.background.pos[0]) * camera_speed,
            self.background.pos[1] + (camera_offset_y - self.background.pos[1]) * camera_speed
        )

        self.player.pos = (
            self.player_position[0] + self.background.pos[0], 
            self.player_position[1] + self.background.pos[1]
        )
