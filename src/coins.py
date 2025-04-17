import typing as t

import pygame

from src import shared, utils


class Coin:
    objects: list[t.Self] = []
    map_image: pygame.Surface

    def __init__(self, pos) -> None:
        Coin.objects.append(self)
        self.rect = Coin.map_image.get_rect()
        drect = pygame.Rect(pos, (shared.TILE_SIDE, shared.TILE_SIDE))
        self.rect.center = drect.center

    def update(self):
        if shared.player.collider.rect.colliderect(self.rect):
            Coin.objects.remove(self)
            shared.player.coins_collected += 1

    def draw(self):
        shared.screen.blit(Coin.map_image, shared.camera.transform(self.rect))
