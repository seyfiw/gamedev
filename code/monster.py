from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window

class Monster(Image):
    def __init__(self, name, spawn_point, image_path, game_map, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.spawn_point = spawn_point 
        self.source = image_path
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.game_map = game_map
        
        self.world_position = list(spawn_point)
        
        self.pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )

        with self.canvas.after:
            Color(1, 0, 0, 0.5)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        # เอาไว้ debug ก่อน
        from kivy.uix.label import Label
        self.label = Label(text=self.name, color=(1,1,1,1), pos=self.pos, size=self.size)
        self.add_widget(self.label)

    def update_position(self):
        new_pos = (
            self.world_position[0] + self.game_map.background.pos[0],
            self.world_position[1] + self.game_map.background.pos[1]
        )

        #is_visible = (
            #0 <= new_pos[0] <= Window.width and
            #0 <= new_pos[1] <= Window.height
        #)
        
        #if is_visible and self.pos != new_pos:
            #print(f"Monster {self.name} world pos: ({self.world_position[0]}, {self.world_position[1]})")
            #print(f"Monster {self.name} screen pos: ({new_pos[0]}, {new_pos[1]})")
            #print(f"Map background pos: ({self.game_map.background.pos[0]}, {self.game_map.background.pos[1]})")

        if self.pos != new_pos:
            self.pos = new_pos
            self.rect.pos = self.pos  # อัปเดตตำแหน่งของ Rectangle ด้วย
            self.label.pos = new_pos  # อัปเดตตำแหน่งของ Label ด้วย