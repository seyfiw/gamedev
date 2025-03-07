from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from player import Player
from map import Map
from camera import Camera
from monster import Monster
from utils.keyboard import KeyboardManager

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = KeyboardManager(self)
        self.map = Map("../gamedev/image/map1-4.png")
        self.player = Player("../image/Wr1.png", self.map)
        self.camera = Camera(self.map, self.player)
        
        #print(f"Map size: {self.map.size}")
        #print(f"Window size: {Window.width}, {Window.height}")
        #print(f"Initial map background pos: {self.map.background.pos}")
        #print(f"Initial player position: {self.player.position}")

        self.add_widget(self.map.background)
        self.add_widget(self.player.sprite)


        map_center_x = self.map.size[0] // 2
        map_center_y = self.map.size[1] // 2

        self.monsters = [
            Monster("Goblin", (map_center_x + 1600, map_center_y), "monster.png", self.map),
            Monster("Orc", (map_center_x, map_center_y + 1600), "monster.png", self.map),
            Monster("Troll", (map_center_x - 1600, map_center_y), "monster.png", self.map),
            Monster("Dragon", (map_center_x, map_center_y - 1600), "monster.png", self.map),
            Monster("Vampire", (map_center_x, map_center_y), "monster.png", self.map)
        ]
        
        

        for monster in self.monsters:
            self.add_widget(monster)

        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        if "walk_left" in self.keyboard.pressed_keys:
            self.player.move_left()
        elif "walk_right" in self.keyboard.pressed_keys:
            self.player.move_right()
        else:
            self.player.idle()

        self.player.update(dt, self.keyboard.pressed_keys)
        self.camera.update()

      

        for monster in self.monsters:
            monster.update_position()

        self.player.sprite.pos = (
            self.player.position[0] + self.map.background.pos[0],
            self.player.position[1] + self.map.background.pos[1]
        )