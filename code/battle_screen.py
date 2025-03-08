from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monster = None
        self.player = None
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.message_label = Label(text="Turn-Based Battle", font_size=30)
        self.layout.add_widget(self.message_label)

        self.player_hp_label = Label(text="Player HP: 100", font_size=20)
        self.layout.add_widget(self.player_hp_label)

        self.monster_hp_label = Label(text="Monster HP: 50", font_size=20)
        self.layout.add_widget(self.monster_hp_label)

        self.mana_label = Label(text="Mana: 50", font_size=20)
        self.layout.add_widget(self.mana_label)
         
        self.back_button = Button(text="Back to Game", size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(self.back_button)

        self.defend_button = Button(text="Defend", size_hint=(1, 0.2))
        self.defend_button.bind(on_press=self.defend)
        self.layout.add_widget(self.defend_button)

        self.escape_button = Button(text="Escape", size_hint=(1, 0.2))
        self.escape_button.bind(on_press=self.escape)
        self.layout.add_widget(self.escape_button)

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
        damage = 10
        self.monster.hp -= damage
        if self.monster.hp < 0:
            self.monster.hp = 0
        self.update_hp_labels()
        self.message_label.text = f"You attacked {self.monster.name} for {damage} damage!"

        if self.monster.hp <= 0:
            self.message_label.text = f"{self.monster.name} has been defeated!"
            self.attack_button.disabled = True
            self.fireball_button.disabled = True
            self.heal_button.disabled = True

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

    def attack(self, instance):
        self.message_label.text = f"You attacked {self.monster.name}!"

    def back_to_game(self, instance):
        self.parent.current = 'game'