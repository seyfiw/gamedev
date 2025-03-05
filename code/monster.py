import random
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage

class Monster(Widget):
    def __init__(self, screen_width, screen_height, **kwargs):
        super().__init__(**kwargs)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = CoreImage("../image/monster.png")
        self.size = (self.image.width, self.image.height)
        with self.canvas:
            self.rect = Rectangle(texture=self.image.texture, pos=self.pos, size=self.size)
            
        self.randomize_position()

    def randomize_position(self):
        self.pos = (random.randint(0, self.screen_width - self.width),
                    random.randint(0, self.screen_height - self.height))
        self.rect.pos = self.pos

    def on_pos(self, instance, value):
        self.rect.pos = value

# Example usage:
# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
#
# class MonsterApp(App):
#     def build(self):
#         screen_width = 800
#         screen_height = 600
#         layout = FloatLayout()
#         monster = Monster(screen_width, screen_height)
#         layout.add_widget(monster)
#         return layout
#
# if __name__ == '__main__':
#     MonsterApp().run()
# monster.draw(screen)