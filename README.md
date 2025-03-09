
เกมที่พัฒนาโดยใช้เฟรมเวิร์ก Kivy เกมดังกล่าวประกอบด้วยเมนูหลัก หน้าจอเกมที่มีผู้เล่นและสัตว์ประหลาด และระบบการต่อสู้แบบผลัดตา ด้านล่างนี้คือคำอธิบายของส่วนประกอบหลักและฟังก์ชันการทำงานของส่วนประกอบเหล่านี้
Main Components
Main Menu (join.py)
Game Widget (game_widget.py)
Player (player.py)
Monster (monster.py)
Map (map.py)
Camera (camera.py)
Keyboard Manager (keyboard.py)
Battle Screen (battle_screen.py)
Main Application (main.py)
เมนูหลัก (join.py)
เมนูหลักช่วยให้ผู้เล่นเริ่มเกมหรือเข้าถึงเมนูตัวเลือกได้
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        label = Label(text='Monster Gambit', font_size=74)
        layout.add_widget(label)
        play_button = Button(text='Play', size_hint=(None, None), size=(200, 50))
        play_button.bind(on_release=self.play_game)
        layout.add_widget(play_button)
        options_button = Button(text='Options', size_hint=(None, None), size=(200, 50))
        options_button.bind(on_release=self.options_menu)
        layout.add_widget(options_button)
        self.add_widget(layout)=
Game Widget (game_widget.py)
คลาส GameWidget เป็นหน้าจอเกมหลักที่ผู้เล่นสามารถเคลื่อนที่และโต้ตอบกับมอนสเตอร์ได้
\class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = KeyboardManager(self)
        self.map = Map("../gamedev/image/map/map1-4.png")
        self.player = Player("../image/player/Wr1.png", self.map)
        self.camera = Camera(self.map, self.player)
        self.add_widget(self.map.background)
        self.add_widget(self.player.sprite)
        map_center_x = self.map.size[0] // 2
        map_center_y = self.map.size[1] // 2
        self.monsters = [
            Monster("Red", (map_center_x + 1600, map_center_y), "../image/red/R/redR1.png", self.map),
            Monster("Stone", (map_center_x, map_center_y + 1600), "../image/stone/L/StoneL1.png", self.map),
            Monster("Golem", (map_center_x - 1600, map_center_y), "../image/golem/Idle/Golem1.png", self.map),
            Monster("Dragon", (map_center_x, map_center_y - 1600), "../image/dragon/L/dragonL1.png", self.map),
        ]
        for monster in self.monsters:
            self.add_widget(monster)
        Clock.schedule_interval(self.update, 1 / 60)
  Player (player.py)
  คลาส Player จัดการสไปรต์ การเคลื่อนไหว และแอนิเมชันของผู้เล่น

class Player:
    def __init__(self, image_path, game_map):
        self.sprite = Image(source=image_path, size=(100, 100), size_hint=(None, None), allow_stretch=True, keep_ratio=False)
        self.position = [game_map.size[0] // 2, game_map.size[1] // 2]
        self.game_map = game_map
        self.max_hp = 100
        self.hp = self.max_hp
        self.mana = 50
        self.animations = {
            "walk_left": ["../image/player/Wl1.png", "../image/player/Wl2.png", "../image/player/Wl3.png"],
            "walk_right": ["../image/player/Wr1.png", "../image/player/Wr2.png", "../image/player/Wr3.png"],
        }
        self.current_animation = "walk_left"
        self.current_frame = 0
        self.animation_interval = 0.1
        Clock.schedule_interval(self.update_animation, self.animation_interval)
Monster (monster.py)
 คลาสมอนสเตอร์จะควบคุมสไปรต์ การเคลื่อนไหว และแอนิเมชันของมอนสเตอร์
 class Monster(Image):
    def __init__(self, name, spawn_point, image_path, game_map, animations=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.spawn_point = spawn_point
        self.source = image_path
        self.size_hint = (None, None)
        self.size = (200, 200)
        self.game_map = game_map
        self.max_hp = 50
        self.hp = self.max_hp
        self.world_position = list(spawn_point)
        self.original_position = list(spawn_point)
        self.pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )
        self.animations = animations if animations else self.load_default_animations()
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.2
        Clock.schedule_interval(self.update_animation, self.animation_speed)
Battle Screen (battle_screen.py)
คลาส BattleScreen จัดการระบบการต่อสู้แบบผลัดตา
class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monster = None
        self.player = None
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#2E3440'))
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        self.message_label = Label(text="Turn-Based Battle", font_size=30, color=get_color_from_hex('#ECEFF4'), bold=True)
        self.layout.add_widget(self.message_label)
        self.player_hp_label = Label(text="Player HP: 100", font_size=20, color=get_color_from_hex('#88C0D0'))
        self.layout.add_widget(self.player_hp_label)
        self.monster_hp_label = Label(text="Monster HP: 50", font_size=20, color=get_color_from_hex('#BF616A'))
        self.layout.add_widget(self.monster_hp_label)
        self.mana_label = Label(text="Mana: 50", font_size=20, color=get_color_from_hex('#81A1C1'))
        self.layout.add_widget(self.mana_label)
        self.attack_button = Button(text="Attack", size_hint=(1, 0.2), background_color=get_color_from_hex('#5E81AC'), color=get_color_from_hex('#ECEFF4'), font_size=20)
        self.attack_button.bind(on_press=self.attack)
        self.layout.add_widget(self.attack_button)
        self.fireball_button = Button(text="Fireball 20 Damage, 10 Mana", size_hint=(0.5, 1), pos_hint={"center_x": 0.7, "center_y": 0.5}, background_color=(0, 0, 0, 0), color=get_color_from_hex('#ECEFF4'), font_size=16, bold=True)
        self.fireball_button.bind(on_press=self.use_fireball)
        self.layout.add_widget(self.fireball_button)
        self.heal_button = Button(text="Heal (30 HP, 15 Mana)", size_hint=(0.5, 1), pos_hint={"center_x": 0.7, "center_y": 0.5}, background_color=(0, 0, 0, 0), color=get_color_from_hex('#ECEFF4'), font_size=16, bold=True)
        self.heal_button.bind(on_press=self.use_heal)
        self.layout.add_widget(self.heal_button)
        self.defend_button = Button(text="Defend", size_hint=(1, 0.2), background_color=get_color_from_hex('#4C566A'), color=get_color_from_hex('#ECEFF4'), font_size=20)
        self.defend_button.bind(on_press=self.defend)
        self.layout.add_widget(self.defend_button)
        self.escape_button = Button(text="Escape", size_hint=(1, 0.2), background_color=get_color_from_hex('#BF616A'), color=get_color_from_hex('#ECEFF4'), font_size=20)
        self.escape_button.bind(on_press=self.escape)
        self.layout.add_widget(self.escape_button)
        self.back_button = Button(text="Back to Game", size_hint=(1, 0.2), background_color=get_color_from_hex('#A3BE8C'), color=get_color_from_hex('#ECEFF4'), font_size=20)
        self.back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(self.back_button)
Main Application (main.py)
คลาส MyApp จะเริ่มเกมและตั้งค่าตัวจัดการหน้าจอ
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        game_widget = GameWidget()
        game_screen = Screen(name='game')
        game_screen.add_widget(game_widget)
        sm.add_widget(game_screen)
        battle_screen = BattleScreen(name='battle')
        sm.add_widget(battle_screen)
        game_widget.screen_manager = sm
        return sm   
