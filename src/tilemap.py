import itertools
from typing import Sequence, Tuple, Union

import pygame

from .tileset import Tileset


class Tilemap:
    def __init__(
        self,
        tileset: Union[Tileset, str],
        grid: Tuple[int, int],
        size: Tuple[int, int],
    ):
        self.__grid_size = grid
        self.__grid_map = [[0] * size[1]] * size[0]
        self.__map_size = size
        map_width = 0.5 * grid[0] * (size[0] + size[1])
        map_height = 0.5 * grid[1] * (size[0] + size[1])
        self.__cam_x = -0.5 * grid[0] * (size[0] - 1) + 0.5 * map_width
        self.__cam_y = 0.5 * map_height
        self.__cam_vx = 0
        self.__cam_vy = 0
        if isinstance(tileset, Tileset):
            self.__tileset = tileset
        elif isinstance(tileset, str):
            self.__tileset = Tileset.rect64(tileset)

    def blit_to(self, surface: pygame.Surface):
        surface.fill(pygame.Color(0, 0, 0, 0))
        xmod = surface.get_rect().centerx - self.__cam_x
        ymod = surface.get_rect().centery - self.__cam_y
        xrange, yrange = [range(i) for i in self.__map_size]
        iso_width, iso_height = [i / 2 for i in self.__grid_size]
        for _xi, _yi in itertools.product(xrange, yrange):
            tile = self.__tileset[self.__grid_map[_xi][_yi]]
            iso_x = -iso_width * _xi + iso_width * _yi
            iso_y = iso_height * _xi + iso_height * _yi
            surface.blit(tile, (iso_x + xmod, iso_y + ymod))

    def key_event(self, pressed: Sequence[bool]):
        if pressed[pygame.K_w]:
            self.__cam_vy -= 1 if self.__cam_vy > -10 else 0
        elif pressed[pygame.K_s]:
            self.__cam_vy += 1 if self.__cam_vy < 10 else 0
        else:
            self.__cam_vy = 0
        if pressed[pygame.K_a]:
            self.__cam_vx -= 1 if self.__cam_vx > -10 else 0
        elif pressed[pygame.K_d]:
            self.__cam_vx += 1 if self.__cam_vx < 10 else 0
        else:
            self.__cam_vx = 0
        self.__cam_x += self.__cam_vx
        self.__cam_y += self.__cam_vy
