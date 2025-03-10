from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from game_widget import GameWidget
from battle_screen import BattleScreen
from join import StartScreen, MainMenu, PlayGame, OptionsMenu

class MyApp(App):
    # Add properties for sound, sfx, volume, and difficulty
    sound_enabled = BooleanProperty(True)
    sfx_enabled = BooleanProperty(True)
    volume_level = NumericProperty(0.7)
    difficulty_level = NumericProperty(2)

    def build(self):
        # Load background music
        try:
            self.background_music = SoundLoader.load('cool-hip-hop-loop.mp3')
            if self.background_music:
                self.background_music.volume = self.volume_level
                self.background_music.loop = True  # Loop the music
            else:
                print("Warning: Could not load background music file")
        except Exception as e:
            self.background_music = None
            print(f"Warning: Could not load background music file. Error: {e}")

        # Start playing background music after 1 second
        Clock.schedule_once(self.start_background_music, 1)

        sm = ScreenManager()

        # Add MainMenu, PlayGame, and OptionsMenu
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(PlayGame(name='play'))
        sm.add_widget(OptionsMenu(name='options'))

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

    def start_background_music(self, dt):
        # Start playing background music when the app starts
        if self.sound_enabled and self.background_music:
            self.background_music.play()
            print("Background music started")

    def update_background_music(self):
        # Update the background music status
        if self.background_music:
            if self.sound_enabled:
                if not self.background_music.state == 'play':
                    self.background_music.play()
                self.background_music.volume = self.volume_level
            else:
                self.background_music.stop()

    def on_stop(self):
        # Stop the background music when the app is closed
        if self.background_music:
            self.background_music.stop()

if __name__ == "__main__":
    MyApp().run()