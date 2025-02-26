from kivy.uix.image import Image
from kivy.core.window import Window
from PIL import Image as PILImage

class Map:
    def __init__(self, map_path):
        self.background = Image(source=map_path)
        self.background.size = (4096,4096)  
        self.background.pos = (0, 0)  
        with PILImage.open(map_path) as img:
            self.size = img.size
        self.collision_map = self._create_collision_map(map_path)

    def _create_collision_map(self, map_path):
        try:
            return PILImage.open(map_path).convert('RGBA')
        except Exception as e:
            print(f"Error creating collision map: {e}")
            return None

    def is_position_valid(self, position):
        if not self.collision_map:
            return True
        try:
            img_x = max(0, min(int(position[0]), self.size[0] - 1))
            img_y = max(0, min(int(self.size[1] - position[1]), self.size[1] - 1))
            pixel = self.collision_map.getpixel((img_x, img_y))
            return pixel[3] >= 250  # ตรวจสอบ alpha channel
        except Exception as e:
            print(f"Error checking position: {e}")
            return False