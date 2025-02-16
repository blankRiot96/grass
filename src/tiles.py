from src import shared, utils


class Tile:
    def __init__(self, pos):
        self.collider = utils.Collider(pos, (shared.TILE_SIDE, shared.TILE_SIDE))

    def update(self):
        pass

    def draw(self):
        self.collider.draw()
