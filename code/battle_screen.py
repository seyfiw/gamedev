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

    def attack(self, instance):
        self.message_label.text = f"You attacked {self.monster.name}!"

    def back_to_game(self, instance):
        self.parent.current = 'game'