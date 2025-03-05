from kivy.app import App
from game_widget import GameWidget
from monster import Monster


class MyGameApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    MyGameApp().run()
