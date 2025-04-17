import typing as t

from src import shared, utils


class Tile:
    objects: list[t.Self] = []

    def __init__(self, pos):
        self.collider = utils.Collider(pos, (shared.TILE_SIDE, shared.TILE_SIDE))
        Tile.objects.append(self)

    def update(self):
        pass

    def draw(self):
        self.collider.draw(fill=True, color="brown")
