import typing as t

import pygame

from src import shared, utils


class Tile:
    objects: list[t.Self] = []
    map_image: pygame.Surface

    def __init__(self, pos):
        self.collider = utils.Collider(pos, (shared.TILE_SIDE, shared.TILE_SIDE))
        Tile.objects.append(self)

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(Tile.map_image, shared.camera.transform(self.collider.pos))
