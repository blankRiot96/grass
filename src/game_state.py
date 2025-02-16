from src import shared, utils
from src.enums import State
from src.world import World


class GameState:
    def __init__(self):
        shared.camera = utils.Camera()
        self.world = World()

    def update(self):
        self.world.update()

    def draw(self):
        self.world.draw()
