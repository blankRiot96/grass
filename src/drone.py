import math

import pygame

from src import shared, utils


class Line:
    def __init__(self, rad: float, speed: float):
        self.speed = speed
        self.rad = rad
        self.surf = pygame.Surface((10, 2), pygame.SRCALPHA)
        self.surf.fill("red")
        self.surf = pygame.transform.rotate(self.surf, math.degrees(rad))
        self.pos = pygame.Vector2()
        self.first = True
        self.alpha = 0
        self.original_pos = pygame.Vector2()
        self.alive = True

    def draw(self, pos):
        if self.first:
            self.pos = pygame.Vector2(pos) - (
                math.cos(self.rad) * 100,
                math.sin(-self.rad) * 100,
            )
            self.original_pos = self.pos.copy()
            self.first = False
        self.pos.move_towards_ip(pos, 10 * shared.dt)

        self.alpha = 255 * ((self.original_pos.distance_to(self.pos) / 100))
        self.surf.set_alpha(self.alpha)

        if self.alpha > 200:
            self.alive = False

        shared.screen.blit(self.surf, shared.camera.transform(self.pos))


class SingleImplode:
    def __init__(self, speed):
        n = 10
        step = math.pi * 2 / n
        self.lines = [Line(step * i, speed) for i in range(n)]
        self.alive = True

    def draw(self, pos):

        for line in self.lines[:]:
            line.draw(pos)

            if not line.alive:
                self.lines.remove(line)

        self.alive = bool(self.lines)


class HoningAnimation:
    def __init__(self):
        self.speed = 10.0
        self.implosions: list[SingleImplode] = [SingleImplode(self.speed)]
        self.timer = utils.Timer(1.0)
        self.charged = False

    def draw(self, pos):
        if self.timer.tick():
            self.speed += 5.0
            self.implosions.append(SingleImplode(self.speed))
            self.timer.time_to_pass -= 0.1

            if self.speed >= 30:
                self.charged = True

        for imp in self.implosions[:]:
            imp.draw(pos)

            if not imp.alive:
                self.implosions.remove(imp)


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

        self.tracking = False
        self.honing_animation = HoningAnimation()

    def update(self):
        self.tracking = self.pos.distance_to(shared.player.collider.pos) > 400

        if self.tracking:
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

        if not self.tracking:
            self.honing_animation.draw(self.eye_rect.center)
