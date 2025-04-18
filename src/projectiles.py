import math
import time

import pygame

from src import shared, utils


class StarProjectile:
    MAX_TAIL_SIZE = 30

    def __init__(self, pos, radians, speed, seconds) -> None:
        self.pos = pygame.Vector2(pos)
        self.radians = radians
        self.original_speed = speed
        self.speed = speed
        self.seconds = seconds
        self.start = time.perf_counter()
        self.direction = self.radians
        self.alive = True

        self.dx = math.cos(self.radians) * self.speed
        self.dy = math.sin(self.radians) * self.speed

    @classmethod
    def from_mouse(cls, pos, velocity, decel):
        return cls(
            pos,
            math.atan2(
                (shared.mouse_pos[1] + shared.camera.offset.y) - pos[1],
                (shared.mouse_pos[0] + shared.camera.offset.x) - pos[0],
            ),
            velocity,
            decel,
        )

    def update(self):
        start = self.pos.copy()

        self.dy += (shared.WORLD_GRAVITY / 10) * shared.dt
        self.pos += pygame.Vector2(self.dx, self.dy) * shared.dt

        self.direction = utils.rad_to(start, self.pos)

        if time.perf_counter() - self.start >= self.seconds:
            self.alive = False

    def points(self) -> list[pygame.typing.Point]:
        tail_size = StarProjectile.MAX_TAIL_SIZE * (
            time.perf_counter() - self.start / self.seconds
        )

        head = self.pos.copy()
        tail = utils.move_towards_rad(head, -self.direction, tail_size)

        forty_five = math.pi / 8
        left_wing = utils.move_towards_rad(
            head, -self.direction - forty_five, tail_size / 3
        )

        right_wing = utils.move_towards_rad(
            head, -self.direction + forty_five, tail_size / 3
        )

        return [left_wing, head, right_wing, tail]

    def draw(self):
        pygame.draw.polygon(
            shared.screen,
            "#bb7f57",
            [shared.camera.transform(pos) for pos in self.points()],
        )
