from kivy.uix.image import Image
from PIL import Image as PILImage

class Map:
    def __init__(self, map_path):
        self.background = Image(source=map_path)
        with PILImage.open(map_path) as img:
            self.size = img.size  
        self.background.size = self.size  
        self.background.pos = (0, 0)  
        self.collision_map = self._create_collision_map(map_path)

    def _create_collision_map(self, map_path):
        try:
            return PILImage.open(map_path).convert('RGBA')
        except Exception as e:
            print(f"Error creating collision map: {e}")
            return None

    def is_position_valid(self, x, y):
        if not self.collision_map:
            return True
        try:
            img_x = max(0, min(int(x), self.size[0] - 1))
            img_y = max(0, min(int(self.size[1] - y), self.size[1] - 1))
            pixel = self.collision_map.getpixel((img_x, img_y))
            return pixel[3] >= 250  
        except Exception as e:
            print(f"Error checking position ({x}, {y}): {e}")
            return False
        
    