from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

class Monster(Image):
    def __init__(self, name, spawn_point, image_path, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.spawn_point = spawn_point
        self.source = image_path  # ตั้งค่า path ของรูปภาพ
        self.size_hint = (None, None)  # ใช้ขนาดแบบ fix
        self.size = (50, 50)  # กำหนดขนาดมอนสเตอร์ (กว้างxสูง)
        self.pos = spawn_point  # กำหนดตำแหน่งเริ่มต้น

class MonsterGame(App):
    def build(self):
        layout = FloatLayout()

        # สร้างมอนสเตอร์ 5 ตัว
        monsters = [
            Monster("Goblin", (100, 200), "monster.png"),
            Monster("Orc", (5, 15), "monster.png"),
            Monster("Troll", (50, 75), "monster.png"),
            Monster("Dragon", (300, 400), "monster.png"),
            Monster("Vampire", (150, 250), "monster.png")
        ]

        # เพิ่มมอนสเตอร์ลงใน layout
        for monster in monsters:
            layout.add_widget(monster)

        return layout

if __name__ == "__main__":
    MonsterGame().run()