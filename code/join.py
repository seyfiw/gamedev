from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        
        title = Label(text='Menu', font_size=74)
        layout.add_widget(title)
        
        play_button = Button(text='Play', size_hint=(None, None), size=(200, 50))
        play_button.bind(on_release=self.play_game)
        layout.add_widget(play_button)
        
        options_button = Button(text='Options', size_hint=(None, None), size=(200, 50))
        options_button.bind(on_release=self.options_menu)
        layout.add_widget(options_button)
        
        self.add_widget(layout)
    
    def play_game(self, instance):
        self.manager.current = 'play'
    
    def options_menu(self, instance):
        self.manager.current = 'options'

class PlayGame(Screen):
    def __init__(self, **kwargs):
        super(PlayGame, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        
        label = Label(text='Game Screen', font_size=74)
        layout.add_widget(label)
        
        back_button = Button(text='Back to Menu', size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.back_to_menu)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class OptionsMenu(Screen):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        
        label = Label(text='Options Screen', font_size=74)
        layout.add_widget(label)
        
        back_button = Button(text='Back to Menu', size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.back_to_menu)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(PlayGame(name='play'))
        sm.add_widget(OptionsMenu(name='options'))
        return sm

if __name__ == '__main__':
    GameApp().run()