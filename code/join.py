from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, NumericProperty

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
        
        # สร้าง layout หลัก
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        
        # หัวข้อหน้า Options
        title = Label(text='Options', font_size=74)
        main_layout.add_widget(title)
        
        # สร้าง GridLayout สำหรับตัวเลือกต่างๆ
        options_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=300)
        
        # ตัวเลือกเสียง (Sound)
        sound_label = Label(text='Sound:', font_size=24, halign='left', size_hint_x=0.5)
        options_layout.add_widget(sound_label)
        
        self.sound_switch = Switch(active=App.get_running_app().sound_enabled)
        self.sound_switch.bind(active=self.toggle_sound)
        options_layout.add_widget(self.sound_switch)
        
        # ตัวเลือกระดับเสียง (Volume)
        volume_label = Label(text='Volume:', font_size=24, halign='left', size_hint_x=0.5)
        options_layout.add_widget(volume_label)
        
        self.volume_slider = Slider(min=0, max=1, value=App.get_running_app().volume_level, step=0.1)
        self.volume_slider.bind(value=self.change_volume)
        options_layout.add_widget(self.volume_slider)
        
        # ตัวเลือกเสียงเอฟเฟกต์ (SFX)
        sfx_label = Label(text='SFX:', font_size=24, halign='left', size_hint_x=0.5)
        options_layout.add_widget(sfx_label)
        
        self.sfx_switch = Switch(active=App.get_running_app().sfx_enabled)
        self.sfx_switch.bind(active=self.toggle_sfx)
        options_layout.add_widget(self.sfx_switch)
        
        # ตัวเลือกความยากง่าย (Difficulty)
        difficulty_label = Label(text='Difficulty:', font_size=24, halign='left', size_hint_x=0.5)
        options_layout.add_widget(difficulty_label)
        
        self.difficulty_slider = Slider(min=1, max=3, value=App.get_running_app().difficulty_level, step=1)
        self.difficulty_slider.bind(value=self.change_difficulty)
        options_layout.add_widget(self.difficulty_slider)
        
        # เพิ่ม options_layout เข้าไปใน main_layout
        main_layout.add_widget(options_layout)
        
        # ปุ่มทดสอบเสียง
        test_sound_button = Button(text='Test Sound', size_hint=(None, None), size=(200, 50))
        test_sound_button.bind(on_release=self.test_sound)
        main_layout.add_widget(test_sound_button)
        
        # เพิ่มที่ว่างข้างล่าง
        spacer = BoxLayout(size_hint_y=0.5)
        main_layout.add_widget(spacer)
        
        # ปุ่มกลับไปยังเมนูหลัก
        back_button = Button(text='Back to Menu', size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.back_to_menu)
        main_layout.add_widget(back_button)
        
        # เพิ่ม main_layout เข้าไปในหน้าจอ
        self.add_widget(main_layout)
    
    def toggle_sound(self, instance, value):
        app = App.get_running_app()
        app.sound_enabled = value
        print(f"Sound {'enabled' if value else 'disabled'}")
    
    def change_volume(self, instance, value):
        app = App.get_running_app()
        app.volume_level = value
        print(f"Volume set to {value}")
    
    def toggle_sfx(self, instance, value):
        app = App.get_running_app()
        app.sfx_enabled = value
        print(f"SFX {'enabled' if value else 'disabled'}")
    
    def change_difficulty(self, instance, value):
        app = App.get_running_app()
        app.difficulty_level = int(value)
        difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        print(f"Difficulty set to {difficulty_names[int(value)]}")
    
    def test_sound(self, instance):
        app = App.get_running_app()
        if app.sound_enabled:
            # ทดสอบเสียงตัวอย่าง (ต้องมีไฟล์ test_sound.wav ในโฟลเดอร์เดียวกับโปรแกรม)
            try:
                sound = app.test_sound
                if sound:
                    sound.volume = app.volume_level
                    sound.play()
                    print("Testing sound...")
            except:
                print("Sound file not found or could not be played")
        else:
            print("Sound is disabled")
    
    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class GameApp(App):
    # เพิ่ม Properties สำหรับเก็บค่าต่างๆ
    sound_enabled = BooleanProperty(True)
    sfx_enabled = BooleanProperty(True)
    volume_level = NumericProperty(0.7)
    difficulty_level = NumericProperty(2)
    
    def build(self):
        # โหลดไฟล์เสียงตัวอย่างสำหรับการทดสอบ
        try:
            self.test_sound = SoundLoader.load('test_sound.wav')
        except:
            self.test_sound = None
            print("Warning: Could not load test sound file")
        
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(PlayGame(name='play'))
        sm.add_widget(OptionsMenu(name='options'))
        return sm

if __name__ == '__main__':
    GameApp().run()