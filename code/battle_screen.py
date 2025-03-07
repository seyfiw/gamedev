from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monster = None
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.message_label = Label(text="Turn-Based Battle", font_size=30)
        self.layout.add_widget(self.message_label)

        self.attack_button = Button(text="Attack", size_hint=(1, 0.2))
        self.attack_button.bind(on_press=self.attack)
        self.layout.add_widget(self.attack_button)

        self.back_button = Button(text="Back to Game", size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(self.back_button)

    def start_battle(self, monster):
        self.monster = monster
        self.message_label.text = f"Battle with {monster.name}!"

    def attack(self, instance):
        self.message_label.text = f"You attacked {self.monster.name}!"

    def back_to_game(self, instance):
        self.parent.current = 'game'