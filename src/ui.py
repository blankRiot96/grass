import pygame

from src import shared, utils
from src.coins import Coin


class CoinCounter:
    def __init__(self, pos) -> None:
        self.pos = pygame.Vector2(pos)
        self.image = pygame.transform.scale_by(Coin.map_image, 1.5)
        self.image_rect = self.image.get_rect(topleft=self.pos)
        self.font = utils.load_font(None, 16)

    def update(self):
        pass

    def draw(self):
        shared.screen.blit(self.image, self.image_rect)

        text_surf = self.font.render(
            f"{shared.player.coins_collected}x", False, "white"
        )
        text_rect = text_surf.get_rect()
        text_rect.midleft = self.image_rect.midright + pygame.Vector2(5, 1)

        # pygame.draw.rect(shared.screen, "red", self.image_rect, width=1)
        # pygame.draw.rect(shared.screen, "red", text_rect, width=1)

        shared.screen.blit(text_surf, text_rect)


class HUD:
    def __init__(self) -> None:
        self.coin_counter = CoinCounter((10, 10))

    def update(self):
        self.coin_counter.update()

    def draw(self):
        self.coin_counter.draw()
