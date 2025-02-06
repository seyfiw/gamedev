from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
        self.map_size = (1024, 1024)  
        self.player_position = [self.map_size[0] // 2, self.map_size[1] // 2]  
        
        with self.canvas:
            self.background = Rectangle(source="image/map1.png", pos=(0, 0), size=self.map_size)
            self.player = Rectangle(source="image/removed-background.png", pos=(Window.width // 2 - 50, Window.height // 2 - 50), size=(32, 32))
       
        self._keyPressed = set()
        Clock.schedule_interval(self.update, 1/60)
    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self._keyPressed.add(text)
    
    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self._keyPressed:
            self._keyPressed.remove(text)
    
    def update(self, dt):
        step_size = 400 * dt
        
        if "w" in self._keyPressed:
            self.player_position[1] += step_size
        if "s" in self._keyPressed:
            self.player_position[1] -= step_size
        if "a" in self._keyPressed:
            self.player_position[0] -= step_size
        if "d" in self._keyPressed:
            self.player_position[0] += step_size
        
        self.player_position[0] = max(0, min(self.map_size[0] - self.player.size[0], self.player_position[0]))
        self.player_position[1] = max(0, min(self.map_size[1] - self.player.size[1], self.player_position[1]))

        camera_offset_x = Window.width // 2 - self.player_position[0] - self.player.size[0] // 2
        camera_offset_y = Window.height // 2 - self.player_position[1] - self.player.size[1] // 2

        self.background.pos = (camera_offset_x, camera_offset_y)
        self.player.pos = (Window.width // 2 - self.player.size[0] // 2, Window.height // 2 - self.player.size[1] // 2)
        
        
    
    
    
    
class MyApp(App):
    def build(self):
        return GameWidget()
    
if __name__ == "__main__":
    app = MyApp()
    app.run()