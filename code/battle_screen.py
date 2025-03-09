from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monster = None
        self.player = None
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # ข้อความแสดงสถานะการต่อสู้
        self.message_label = Label(text="Turn-Based Battle", font_size=30)
        self.layout.add_widget(self.message_label)

        # แสดง HP ของผู้เล่นและมอนสเตอร์
        self.player_hp_label = Label(text="Player HP: 100", font_size=20)
        self.layout.add_widget(self.player_hp_label)

        self.monster_hp_label = Label(text="Monster HP: 50", font_size=20)
        self.layout.add_widget(self.monster_hp_label)

        # แสดง Mana ของผู้เล่น
        self.mana_label = Label(text="Mana: 50", font_size=20)
        self.layout.add_widget(self.mana_label)
        
         # ปุ่ม Attack
        self.attack_button = Button(text="Attack", size_hint=(1, 0.2))
        self.attack_button.bind(on_press=self.attack)
        self.layout.add_widget(self.attack_button)
        
        # ปุ่ม Fireball
        fireball_layout = RelativeLayout(size_hint=(1, 0.2))
        fireball_image = Image(source="image/skill/Fireball2.png", size_hint=(0.5, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        fireball_layout.add_widget(fireball_image)
        
        self.fireball_button = Button(
            text="Fireball 20 Damage, 10 Mana",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.7, "center_y": 0.5},
            background_color=(0, 1, 1, 0)  
        )
        
        self.fireball_button.bind(on_press=self.use_fireball)
        fireball_layout.add_widget(self.fireball_button)
        self.layout.add_widget(fireball_layout)

        # ปุ่ม Heal
        HP_layout = RelativeLayout(size_hint=(1, 0.2))
        HP_image = Image(source="image/skill/heal.png", size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        HP_layout.add_widget(HP_image)

        self.heal_button = Button(
            text="Heal (30 HP, 15 Mana)",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.7, "center_y": 0.5},
            background_color=(0, 1, 1, 1)  # ค่า Alpha ต้องเป็น 1 (ไม่โปร่งใสทั้งหมด)
        )
        self.heal_button.bind(on_press=self.use_heal)
        HP_layout.add_widget(self.heal_button)
        self.layout.add_widget(HP_layout)
        
        # ปุ่ม Defend
        self.defend_button = Button(text="Defend", size_hint=(1, 0.2))
        self.defend_button.bind(on_press=self.defend)
        self.layout.add_widget(self.defend_button)

        # ปุ่ม Escape
        self.escape_button = Button(text="Escape", size_hint=(1, 0.2))
        self.escape_button.bind(on_press=self.escape)
        self.layout.add_widget(self.escape_button)

        # ปุ่ม Back to Game
        self.back_button = Button(text="Back to Game", size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(self.back_button)

        
        

        
        
    def start_battle(self, monster, player):
        self.monster = monster
        self.player = player
        self.update_hp_labels()
        self.update_mana_label()
        self.message_label.text = f"Battle with {monster.name}!"

    #HP 
    def update_hp_labels(self):
        self.player_hp_label.text = f"Player HP: {self.player.hp}/{self.player.max_hp}"
        self.monster_hp_label.text = f"Monster HP: {self.monster.hp}/{self.monster.max_hp}"
        
    #Mana
    def update_mana_label(self):
        self.mana_label.text = f"Mana: {self.player.mana}"
    
    #skill 
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

    def back_to_game(self, instance):
        self.parent.current = 'game'
        
    def check_battle_result(self):
        if  self.monster.hp <= 0:
            self.message_label.text = "You won the battle!"
            self.give_rewards()
            self.monster.die()
            self.parent.current = 'game'
        elif self.player.hp <= 0:
            self.message_label.text = "You were defeated..."
            self.parent.current = 'game'
    
    # ให้รางวัลเมื่อชนะ        
    def give_rewards(self):
        self.player.hp = self.player.max_hp  # เติมเลือดให้เต็ม
        self.player.mana = 50  # เติม mana ให้เต็ม
        self.message_label.text = "Now restored your HP and Mana!"
    
    
        self.player.mana = 50  # เติม mana ให้เต็ม
        self.message_label.text = "You received 50 gold and restored your HP and Mana!"
     
