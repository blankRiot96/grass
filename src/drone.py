import math
import random
import time

import pygame

from src import shared, utils


class Line:
    def __init__(self, rad: float, speed: float):
        self.speed = speed
        self.radians = rad
        self.surf = pygame.Surface((5, 1), pygame.SRCALPHA)
        self.surf.fill("red")
        self.surf = pygame.transform.rotate(self.surf, math.degrees(rad))
        self.pos = pygame.Vector2()
        self.first = True
        self.alpha = 0
        self.original_pos = pygame.Vector2()
        self.alive = True
        self.radius = 70

    def draw(self, pos):
        self.pos = pygame.Vector2(pos) - (
            math.cos(self.radians) * self.radius,
            math.sin(-self.radians) * self.radius,
        )

        self.radius -= 10 * shared.dt

        self.alpha = 400 * (1.0 - (self.radius / 70))
        self.surf.set_alpha(self.alpha)

        if self.radius <= shared.TILE_SIDE / 3:
            self.alive = False

        shared.screen.blit(self.surf, shared.camera.transform(self.pos))


class SingleImplode:
    def __init__(self, speed):
        n = 20
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
        self.speed = 1000
        self.implosions: list[SingleImplode] = [SingleImplode(self.speed)]
        self.timer = utils.Timer(0.2)
        self.charged = False
        self.time_passed = 0.0
        self.start = time.perf_counter()

    def draw(self, pos):
        self.time_passed = time.perf_counter() - self.start

        if self.timer.tick():
            self.implosions.append(SingleImplode(self.speed))
            # if self.timer.time_to_pass > 0.1:
            #     self.timer.time_to_pass -= 0.3
            # else:
            #     self.charged = True

        for imp in self.implosions[:]:
            imp.draw(pos)

            if not imp.alive:
                self.implosions.remove(imp)


class Beam:
    FADE_TIME = 1.0

    def __init__(self):
        self._shoot = False
        self.alpha = 255
        self.start = time.perf_counter()
        self.first = True
        self.orig = pygame.Surface((1000, 20), pygame.SRCALPHA)
        self.orig.fill("red")
        self.rog = self.orig.copy()
        self.rect = self.rog.get_rect()

    @property
    def shoot(self) -> bool:
        return self._shoot

    @shoot.setter
    def shoot(self, val) -> bool:
        self.first = True
        self.start = time.perf_counter()
        self._shoot = val

    def draw(self, pos, rad, right, up):
        if not self._shoot:
            return

        if self.first:
            prefix = "bottom" if up else "top"
            suffix = "left" if right else "right"
            word = prefix + suffix

            d = {word: pos}

            rect = self.orig.get_rect(**d)
            self.rog = pygame.transform.rotate(self.orig, math.degrees(-rad))

            d2 = {word: getattr(rect, word)}
            self.rect = self.rog.get_rect(**d2)

            self.first = False

        alpha = 255 * (1 - ((time.perf_counter() - self.start) / Beam.FADE_TIME))
        self.rog.set_alpha(alpha)

        shared.screen.blit(self.rog, shared.camera.transform(self.rect))

        if alpha <= 5:
            self.first = True
            self._shoot = False


class Drone:
    SPEED = 20
    BEAM_CHARGE_TIME = 5.0

    def __init__(self, pos):
        self.body = pygame.transform.scale_by(
            utils.circle_surf(shared.TILE_SIDE / 4, (150, 150, 150)), 4
        )
        self.eye_color = pygame.Color("white")
        self.eye = utils.circle_surf(shared.TILE_SIDE / 3, self.eye_color)
        self.eye_rect = self.eye.get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect = self.body.get_rect(topleft=self.pos)

        self.tracking = True
        self.honing_animation = HoningAnimation()
        self.done = False
        self.st = time.perf_counter()

        self.beam = Beam()

    def update(self):

        dist = self.pos.distance_to(shared.player.collider.pos)
        if self.tracking:
            self.tracking = dist > 400

        if self.done:
            self.tracking = False

            if time.perf_counter() - self.st > 2.0:
                self.done = False

        if dist > 200 and not self.done:
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

        if not self.done:
            x = self.honing_animation.time_passed / Drone.BEAM_CHARGE_TIME
            x = 1 - x
            x = int(x * 255)
            if x <= 0:
                self.beam.shoot = True
                self.st = time.perf_counter()
                self.done = True
                self.honing_animation = HoningAnimation()
                x = 0
                self.tracking = True
                self.eye_color.g, self.eye_color.b = 255, 255
            else:
                self.eye_color.g, self.eye_color.b = x, x
            self.eye = utils.circle_surf(shared.TILE_SIDE / 3, self.eye_color)

    def draw(self):
        shared.screen.blit(self.body, shared.camera.transform(self.rect))
        shared.screen.blit(
            self.eye,
            shared.camera.transform(
                self.eye_rect.topleft
                + pygame.Vector2(random.randint(1, 3), random.randint(1, 3))
                * (not self.tracking)
                * (not self.done)
            ),
        )
        self.beam.draw(
            self.eye_rect.center,
            utils.rad_to(shared.player.collider.pos, self.pos),
            shared.player.collider.pos.x > self.pos.x,
            shared.player.collider.pos.y < self.pos.y,
        )

        if not self.tracking and not self.done:
            self.honing_animation.draw(self.eye_rect.center)
            if self.honing_animation.charged:
                self.honing_animation = HoningAnimation()
                print("new")
