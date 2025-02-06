from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.graphics import Rectangle

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
        self.map_size = (10240, 10240)
        self.player_position = [self.map_size[0] // 2, self.map_size[1] // 2]
        
        with self.canvas:
            self.block = Rectangle(pos=(50,50), size=(64, 64))
        
        self.background = Image(source="image/map1-2.png", size=self.map_size)
        self.player = Image(source="image/removed-background.png", size=(64, 64))
        self.add_widget(self.background)
        self.add_widget(self.player)
        self.add_widget(self.block)

        self._keyPressed = set()
        Clock.schedule_interval(self.update, 1/60)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1] if keycode[1] else text  
        self._keyPressed.add(key)

    def _on_keyboard_up(self, keyboard, keycode):
        key = keycode[1] if keycode[1] else ""
        self._keyPressed.discard(key)  

    def update(self, dt):
        step_size = Vector(500 * dt, 500 * dt)
        
        if "w" in self._keyPressed:
            self.player_position = Vector(self.player_position) + Vector(0, step_size.y)
        if "s" in self._keyPressed:
            self.player_position = Vector(self.player_position) - Vector(0, step_size.y)
        if "a" in self._keyPressed:
            self.player_position = Vector(self.player_position) - Vector(step_size.x, 0)
        if "d" in self._keyPressed:
            self.player_position = Vector(self.player_position) + Vector(step_size.x, 0)

        self.player_position[0] = max(0, min(self.map_size[0] - self.player.size[0], self.player_position[0]))
        self.player_position[1] = max(0, min(self.map_size[1] - self.player.size[1], self.player_position[1]))

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
        
