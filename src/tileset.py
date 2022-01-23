import itertools
import pygame
from typing import List, Tuple


class Tileset:
    @classmethod
    def rect64(cls, path):
        return cls(path, (64, 64))

    def __init__(self, path: str, size: Tuple[int, int]):
        self.__tile_surface: List[pygame.Surface] = []
        self.__tile_size = size
        self._read(path)

    def __len__(self) -> int:
        return len(self.__tile_surface)

    def __getitem__(self, key: int) -> pygame.Surface:
        return self.__tile_surface[key]

    def _read(self, path):
        image = pygame.image.load(path).convert_alpha()
        image_width, image_height = image.get_rect().size
        tile_width, tile_height = self.__tile_size
        xrange = range(0, image_width, tile_width)
        yrange = range(0, image_height, tile_height)
        for y, x in itertools.product(yrange, xrange):
            _tile = pygame.Surface(self.__tile_size, pygame.SRCALPHA)
            _tile.blit(image, (0, 0), (x, y, *self.__tile_size))
            self.__tile_surface.append(_tile)
