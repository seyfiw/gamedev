from kivy.uix.widget import Widget
from kivy.clock import Clock
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

        self.add_widget(self.map.background)
        self.add_widget(self.player.sprite)
        
        self.monsters = [
            Monster("Goblin", (100, 200), "monster.png"),
            Monster("Orc", (5, 15), "monster.png"),
            Monster("Troll", (50, 75), "monster.png"),
            Monster("Dragon", (300, 400), "monster.png"),
            Monster("Vampire", (150, 250), "monster.png")
        ]
        for monster in self.monsters:
            self.add_widget(monster) 
       
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
    
        if "walk_left" in self.keyboard.pressed_keys:
            self.player.move_left()  
        elif "walk_right" in self.keyboard.pressed_keys:
            self.player.move_right() 
        else:
            self.player.idle()  

        self.player.update(dt, self.keyboard.pressed_keys)  
        self.camera.update()

        self.player.sprite.pos = (
            self.player.position[0] + self.map.background.pos[0],
            self.player.position[1] + self.map.background.pos[1]
    )

