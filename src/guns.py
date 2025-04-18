import time

import pygame

from src import shared, utils
from src.projectiles import StarProjectile


class StarShooter:
    COOLDOWN = 1.0

    def __init__(self) -> None:
        self.stars: list[StarProjectile] = []
        self.cooldown = utils.CooldownTimer(StarShooter.COOLDOWN)

    def update(self):
        self.cooldown.update()
        if shared.mjp[0] and not self.cooldown.is_cooling_down:
            self.stars.append(
                StarProjectile.from_mouse(
                    shared.player.collider.rect.center,
                    # utils.rad_to(
                    #     pygame.Vector2(shared.player.collider.rect.center),
                    #     pygame.Vector2(shared.camera.transform(shared.mouse_pos)),
                    # ),
                    50,
                    3.0,
                )
            )
            self.cooldown.start()

        for star in self.stars[:]:
            star.update()

            if not star.alive:
                self.stars.remove(star)

    def draw(self):
        for star in self.stars:
            star.draw()
