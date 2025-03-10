from __future__ import annotations

import typing as t

import pygame

if t.TYPE_CHECKING:
    from src.enums import State
    from src.player import Player
    from src.utils import Camera

# Const
TILE_SIDE = 32
WORLD_GRAVITY = 100
MAX_FALL_VELOCITY = 300

# Canvas
screen: pygame.Surface
srect: pygame.Rect
camera: Camera

# Events
events: list[pygame.event.Event]
mouse_pos: pygame.Vector2
mouse_press: tuple[int, ...]
keys: list[bool]
kp: list[bool]
kr: list[bool]
dt: float
clock: pygame.Clock

# States
next_state: State | None

# Objects
entities: list
player: Player
