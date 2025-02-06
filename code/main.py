from kivy.app import App
from game_widget import GameWidget   

class MyApp(App):
    def build(self):
        return GameWidget() 

if __name__ == "__main__":
    app = MyApp()
    app.run()
