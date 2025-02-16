import math

import pygame

from src import shared, utils


class Drone:
    SPEED = 20

    def __init__(self, pos):
        self.body = pygame.transform.scale_by(
            utils.circle_surf(shared.TILE_SIDE / 4, (150, 150, 150)), 4
        )
        self.eye = utils.circle_surf(shared.TILE_SIDE / 3, "red")
        self.eye_rect = self.eye.get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect = self.body.get_rect(topleft=self.pos)

    def update(self):

        if self.pos.distance_to(shared.player.collider.pos) > 400:
            self.pos.move_towards_ip(
                shared.player.collider.pos, Drone.SPEED * shared.dt
            )

        self.rect.topleft = self.pos

        mv = 10
        radians = utils.rad_to(self.pos, shared.player.collider.pos)
        self.eye_rect.center = (
            self.rect.centerx + math.cos(radians) * mv,
            self.rect.centery + math.sin(radians) * mv,
        )

    def draw(self):
        shared.screen.blit(self.body, shared.camera.transform(self.rect))
        shared.screen.blit(self.eye, shared.camera.transform(self.eye_rect))
