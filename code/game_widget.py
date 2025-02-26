from kivy.uix.widget import Widget
from kivy.clock import Clock
from player import Player
from map import Map
from camera import Camera
from utils.keyboard import KeyboardManager

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = KeyboardManager(self)
        self.map = Map("../image/map1-4.png")
        self.player = Player("../image/removed-background.png", self.map)
        self.camera = Camera(self.map, self.player)

        self.add_widget(self.map.background)
        self.add_widget(self.player.sprite)

        print(f"Map background size: {self.map.background.size}")
        print(f"Player sprite size: {self.player.sprite.size}")
        print(f"Map background pos: {self.map.background.pos}")
        print(f"Player sprite pos: {self.player.sprite.pos}")

        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.player.update(dt, self.keyboard.pressed_keys)
        self.camera.update()

        self.player.sprite.pos = (
            self.player.position[0] + self.map.background.pos[0],
            self.player.position[1] + self.map.background.pos[1]
        )