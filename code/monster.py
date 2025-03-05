class Monster:
    def __init__(self, name: str, spawn_point: tuple, image_path: str):
        self.name = name
        self.spawn_point = spawn_point
        self.position = spawn_point
        self.image_path = image_path

    def spawn(self) -> None:
        print(f"{self.name} has spawned at {self.spawn_point} with image {self.image_path}")

# Example usage
monster1 = Monster("Goblin", (10, 20), "monster.png")
monster1.spawn()

monster2 = Monster("Orc", (5, 15), "monster.png")
monster2.spawn()