from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from game_widget import GameWidget
from battle_screen import BattleScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()

        #หน้า เกมหลัก
        game_widget = GameWidget()
        game_screen = Screen(name='game')
        game_screen.add_widget(game_widget)
        sm.add_widget(game_screen)

        #หน้า Turn-Based Battle
        battle_screen = BattleScreen(name='battle')
        sm.add_widget(battle_screen)

        game_widget.screen_manager = sm

        return sm

if __name__ == "__main__":
    MyApp().run()