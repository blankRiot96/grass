from src import shared, utils
from src.enums import State
from src.ui import HUD
from src.world import World


class GameState:
    def __init__(self):
        shared.camera = utils.Camera()
        self.world = World()
        self.hud = HUD()

    def update(self):
        self.world.update()
        self.hud.update()

    def draw(self):
        self.world.draw()
        self.hud.draw()
