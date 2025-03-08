from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.screenmanager import ScreenManager
from kivy.graphics import Rectangle
from player import Player,SwordAttack
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
        ]
        
        

        for monster in self.monsters:
            self.add_widget(monster)

        Clock.schedule_interval(self.update, 1 / 60)
        
    def check_collision(self):
        player_x, player_y = self.player.sprite.pos
        player_width, player_height = self.player.sprite.size

        for monster in self.monsters:
            monster_x, monster_y = monster.pos
            monster_width, monster_height = monster.size

            if (player_x < monster_x + monster_width and
                player_x + player_width > monster_x and
                player_y < monster_y + monster_height and
                player_y + player_height > monster_y):
                self.start_turn_based_battle(monster)
                break

    def get_collision_rect(self, entity):

        if hasattr(entity, 'sprite'):  # Player
            return Window.Rect(entity.sprite.pos[0], entity.sprite.pos[1], entity.sprite.size[0], entity.sprite.size[1])
        else:  # Monster
            return Window.Rect(entity.pos[0], entity.pos[1], entity.size[0], entity.size[1])

    def start_turn_based_battle(self, monster):
        if self.screen_manager:
            self.screen_manager.current = 'battle'
            battle_screen = self.screen_manager.get_screen('battle')
            battle_screen.start_battle(monster)

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
        
        
        self.check_collision()
    
       
       
    def update(self, dt):
        # รับการกดปุ่ม
        pressed_keys = set()
        keyboard = self.keyboard
        if keyboard.is_key_down(keyboard.keycodes['w']):
            pressed_keys.add('w')
        if keyboard.is_key_down(keyboard.keycodes['a']):
            pressed_keys.add('a')
        if keyboard.is_key_down(keyboard.keycodes['s']):
            pressed_keys.add('s')
        if keyboard.is_key_down(keyboard.keycodes['d']):
            pressed_keys.add('d')
        if keyboard.is_key_down(keyboard.keycodes['spacebar']):
            pressed_keys.add('spacebar')  
        
        # อัพเดทการเคลื่อนที่ของผู้เล่น
        self.player.update(dt, pressed_keys)
        
        # อัพเดทระบบการโจมตี
        self.sword_attack.update(dt, pressed_keys)
        
        # ลบศัตรูที่ตายแล้วออกจากรายการเป้าหมาย
        for enemy in self.enemies[:]:
            if not enemy.is_alive:
                self.sword_attack.remove_attack_target(enemy)
                self.enemies.remove(enemy)