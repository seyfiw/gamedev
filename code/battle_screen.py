from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout


class ImageButtonWithText(ButtonBehavior, RelativeLayout):
    def __init__(self, image_source, button_text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        self.image = Image(
            source=image_source, 
            size_hint=(1, 1),  
            pos_hint={"center_x": 0.5, "center_y": 0.5}  
        )
        self.add_widget(self.image)

        self.label = Label(
            text=button_text, 
            size_hint=(0.8, 0.2), 
            pos_hint={"center_x": 0.5, "center_y": 0.2},  
            color=get_color_from_hex('#ECEFF4'), 
            font_size=16,
            bold=True
        )
        self.add_widget(self.label)


class AnimatedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_size = self.size
        self.original_color = self.background_color

    def on_press(self):
        anim = Animation(size=(self.width * 0.9, self.height * 0.9), duration=0.1) + \
               Animation(size=self.original_size, duration=0.1)
        anim.start(self)
        self.background_color = (self.original_color[0] * 1.2, self.original_color[1] * 1.2, self.original_color[2] * 1.2, 1)

    def on_release(self):
        self.background_color = self.original_color


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monster = None
        self.player = None

        # เพิ่มพื้นหลัง
        self.background = Image(source="image/background/battle_background.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        self.background.size = Window.size
        self.background.pos = self.pos
        self.bind(size=self._update_background, pos=self._update_background)

        self.main_layout = RelativeLayout()
        self.add_widget(self.main_layout)

        self.message_label = Label(
            text="Turn-Based Battle", 
            font_size=30, 
            color=get_color_from_hex('#ECEFF4'), 
            bold=True,
            size_hint=(1, 0.1),
            pos_hint={'top': 1}
        )
        self.main_layout.add_widget(self.message_label)

        # HP และ Mana
        self.player_hp_label = Label(
            text="Player HP: 100", 
            font_size=20, 
            color=get_color_from_hex('#88C0D0'),
            size_hint=(1, 0.1),
            pos_hint={'top': 0.9}
        )
        self.main_layout.add_widget(self.player_hp_label)

        self.monster_hp_label = Label(
            text="Monster HP: 50", 
            font_size=20, 
            color=get_color_from_hex('#BF616A'),
            size_hint=(1, 0.1),
            pos_hint={'top': 0.8}
        )
        self.main_layout.add_widget(self.monster_hp_label)

        self.mana_label = Label(
            text="Mana: 50", 
            font_size=20, 
            color=get_color_from_hex('#81A1C1'),
            size_hint=(1, 0.1),
            pos_hint={'top': 0.7}
        )
        self.main_layout.add_widget(self.mana_label)
        
        # Player และ Monster
        self.player_image = Image(
            size_hint=(0.15, 0.23),  
            pos_hint={'center_x': 0.25, 'center_y': 0.44},
            allow_stretch = True, 
            keep_ratio = False  
        )
        self.main_layout.add_widget(self.player_image)

        self.monster_image = Image(
            allow_stretch = True ,
            keep_ratio = False  
        )
        self.main_layout.add_widget(self.monster_image)

        # ปุ่มต่างๆ
        self.button_layout = GridLayout(
            cols=3, 
            rows=2, 
            spacing=10, 
            size_hint=(0.9, 0.3), 
            pos_hint={"center_x": 0.5, "y": 0.05}
        )
        self.main_layout.add_widget(self.button_layout)

        # ปุ่ม Attack (ซ้ายบน)
        self.attack_button = ImageButtonWithText(
            image_source="image/button/button_attack.png",  
            button_text="="  
        )
        self.attack_button.bind(on_press=self.attack)
        self.button_layout.add_widget(self.attack_button)

        # ปุ่ม Fireball (ขวาบน)
        self.fireball_button = ImageButtonWithText(
            image_source="image/button/button_fireball.png", 
            button_text="" 
        )
        self.fireball_button.bind(on_press=self.use_fireball)
        self.button_layout.add_widget(self.fireball_button)

        # ปุ่ม Heal (ซ้ายล่าง)
        self.heal_button = ImageButtonWithText(
            image_source="image/button/button_HP.png",  
            button_text=""  
        )
        self.heal_button.bind(on_press=self.use_heal)
        self.button_layout.add_widget(self.heal_button)

        # ปุ่ม Defend (ขวาล่าง)
        self.defend_button = ImageButtonWithText(
            image_source="image/button/button_defend.png", 
            button_text=""  
        )
        self.defend_button.bind(on_press=self.defend)
        self.button_layout.add_widget(self.defend_button)

        # ปุ่ม Escape 
        self.escape_button = ImageButtonWithText(
            image_source="image/button/button_escape.png", 
            button_text=""  
        )
        self.escape_button.bind(on_press=self.escape)
        self.button_layout.add_widget(self.escape_button)

    def _update_background(self, instance, value):
        self.background.size = instance.size
        self.background.pos = instance.pos

    def start_battle(self, monster, player):
        self.monster = monster
        self.player = player
        self.update_hp_labels()
        self.update_mana_label()
        self.message_label.text = f"Battle with {monster.name}!"
        self.player_image.source = player.sprite.source
        self.monster_image.source = monster.source
        self.monster_animations = monster.load_default_animations()
        self.death_frames = self.monster_animations.get("death", [])
        
        
        
        if monster.name == "Red":
            self.monster_image.size_hint = (0.2, 0.4)  
            self.monster_image.pos_hint = {'center_x': 0.7, 'center_y': 0.56}
            
        elif monster.name == "Stone":
            self.monster_image.size_hint = (0.15, 0.26)  
            self.monster_image.pos_hint = {'center_x': 0.7, 'center_y': 0.49}
            
        elif monster.name == "Golem":
            self.monster_image.size_hint = (0.3, 0.5)  
            self.monster_image.pos_hint = {'center_x': 0.8, 'center_y': 0.55}
            
        elif monster.name == "Dragon":
            self.monster_image.size_hint = (0.35, 0.7)  
            self.monster_image.pos_hint = {'center_x': 0.7, 'center_y': 0.7}

    def update_hp_labels(self):
        self.player_hp_label.text = f"Player HP: {self.player.hp}/{self.player.max_hp}"
        self.monster_hp_label.text = f"Monster HP: {self.monster.hp}/{self.monster.max_hp}"

    def update_mana_label(self):
        self.mana_label.text = f"Mana: {self.player.mana}"

    def attack(self, instance):
        damageMonster = 10
        damagePlayer = 5
        self.monster.hp -= damageMonster
        self.player.hp -= damagePlayer
        if self.monster.hp < 0:
            self.monster.hp = 0
        self.update_hp_labels()
        self.message_label.text = f"You attacked {self.monster.name} for {damageMonster} damage!"
        self.check_battle_result()

    def use_fireball(self, instance):
        if self.player.mana >= self.player.skills["Fireball"]["mana_cost"]:
            damage = self.player.skills["Fireball"]["damage"]
            self.monster.hp -= damage
            self.player.mana -= self.player.skills["Fireball"]["mana_cost"]
            if self.monster.hp < 0:
                self.monster.hp = 0
            self.update_hp_labels()
            self.update_mana_label()
            self.message_label.text = f"You used Fireball and dealt {damage} damage!"
        else:
            self.message_label.text = "Not enough mana!"
        self.check_battle_result()

    def use_heal(self, instance):
        if self.player.mana >= self.player.skills["Heal"]["mana_cost"]:
            heal = self.player.skills["Heal"]["heal"]
            self.player.hp += heal
            if self.player.hp > self.player.max_hp:
                self.player.hp = self.player.max_hp
            self.player.mana -= self.player.skills["Heal"]["mana_cost"]
            self.update_hp_labels()
            self.update_mana_label()
            self.message_label.text = f"You used Heal and recovered {heal} HP!"
        else:
            self.message_label.text = "Not enough mana!"

    def defend(self, instance):
        self.message_label.text = "You defended against the monster's attack!"

    def escape(self, instance):
        self.message_label.text = "You escaped from the battle!"
        self.parent.current = 'game'

    def check_battle_result(self):
        if self.monster.hp <= 0:
            self.message_label.text = "You won the battle!"
            self.give_rewards()
            self.play_animation(self.death_frames)
            self.monster.die()
            
            if hasattr(self, 'on_monster_defeated'):
                self.on_monster_defeated()
                
            Clock.schedule_once(self.back_to_game, 1.5)  
        elif self.player.hp <= 0:
            self.message_label.text = "You were defeated..."
            Clock.schedule_once(self.back_to_game, 1.5) 

    def give_rewards(self):
        self.player.hp = self.player.max_hp
        self.player.mana = 50
        self.message_label.text = "You received 50 gold and restored your HP and Mana!"

    def back_to_game(self, dt):
        self.parent.current = 'game'

    def play_animation(self, frames):
        def update_frame(dt):
            if frames:
                self.monster_image.source = frames.pop(0)
                if frames:
                    Clock.schedule_once(update_frame, 0.2)
                else:
                    self.monster_image.source = ""
        update_frame(0)