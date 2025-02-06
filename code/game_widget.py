from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics import Rectangle as GraphicsRectangle


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
        self.map_size = (10240, 10240)
        self.player_position = [self.map_size[0] // 2, self.map_size[1] // 2]

        self.background = Image(source="image/map1-2.png", size=self.map_size)
        self.player = Image(source="image/removed-background.png", size=(64, 64))
        self.add_widget(self.background)
        self.add_widget(self.player)
        

        self.black_box_position = [self.map_size[0] // 2 + 300, self.map_size[1] // 2 + 300]
        with self.canvas:
            Color(1, 0, 1, 1)  
            self.black_rect = GraphicsRectangle(size=(100, 100), pos=self.black_box_position)

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
        step_size = Vector(1000 * dt, 1000 * dt)


        if "w" in self._keyPressed:
            self.player_position = Vector(self.player_position) + Vector(0, step_size.y)
        if "s" in self._keyPressed:
            self.player_position = Vector(self.player_position) - Vector(0, step_size.y)
        if "a" in self._keyPressed:
            self.player_position = Vector(self.player_position) - Vector(step_size.x, 0)
        if "d" in self._keyPressed:
            self.player_position = Vector(self.player_position) + Vector(step_size.x, 0)


        self.collision("horizontal")

        self.collision("vertical")


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


        self.black_rect.pos = (
            self.black_box_position[0] + self.background.pos[0], 
            self.black_box_position[1] + self.background.pos[1]
        )

    def collision(self, direction):

        player_rect = (
            self.player.pos[0], 
            self.player.pos[1], 
            self.player.size[0], 
            self.player.size[1]
        )


        black_rect = (
            self.black_rect.pos[0], 
            self.black_rect.pos[1], 
            self.black_rect.size[0], 
            self.black_rect.size[1]
        )


        if self._check_collision(player_rect, black_rect):
            if direction == "horizontal":
                if self.player_position[0] < self.black_box_position[0]:
                    self.player_position[0] = self.black_box_position[0] - self.player.size[0]
                else:
                    self.player_position[0] = self.black_box_position[0] + self.black_rect.size[0]
            elif direction == "vertical":
                if self.player_position[1] < self.black_box_position[1]:
                    self.player_position[1] = self.black_box_position[1] - self.player.size[1]
                else:
                    self.player_position[1] = self.black_box_position[1] + self.black_rect.size[1]

    def _check_collision(self, player_rect, black_rect):

        return not (player_rect[0] + player_rect[2] <= black_rect[0] or  
                    player_rect[0] >= black_rect[0] + black_rect[2] or  
                    player_rect[1] + player_rect[3] <= black_rect[1] or  
                    player_rect[1] >= black_rect[1] + black_rect[3])  
