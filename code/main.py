from kivy.app import App
from game_widget import GameWidget
from monster import Monster
from join import MainMenu, PlayGame, OptionsMenu
from kivy.uix.screenmanager import ScreenManager, Screen


class MyGameApp(App):
    def build(self):
        return GameWidget()
class MyscreenApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(PlayGame(name='play'))
        sm.add_widget(OptionsMenu(name='options'))
        return sm


if __name__ == "__main__":
    MyGameApp().run()
