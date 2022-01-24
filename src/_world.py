from typing import List, Sequence, Tuple, Union

import pygame
from ._tile import Tilemap


class World:
    """여러 레이어로 구성한 월드맵 이미지 제어 클래스

    매개변수:
        grid: 타일 배치 격자의 크기
        layers: 배치레이어의 수

    """

    def __init__(self, grid: Tuple[int, int], layers: int):
        self.__grid = grid
        self.__layer = [Tilemap(grid) for _ in range(layers)]

    def __setitem__(
        self,
        key: Tuple[int, Union[int, slice], Union[int, slice]],
        tile: Union[pygame.Surface, None],
    ):
        """타일 이미지 배치

        World[레이어, x, y]로 사용
        """
        self.__layer[key[0]][key[1], key[2]] = tile
        self.__cam_x = 0
        self.__cam_y = 0
        self.__cam_vx = 0
        self.__cam_vy = 0

    @property
    def size(self) -> Tuple[int, int]:
        """이미지 크기 출력"""
        width = max([l.size[0] for l in self.__layer])
        height = max([l.size[1] for l in self.__layer])
        height += self.__grid[1] * (len(self.__layer) - 1)
        return width, height

    @property
    def surface(self) -> pygame.Surface:
        """이미지 출력"""
        width, height = self.size
        lenx = max([l.len[0] for l in self.__layer])
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for idx, layer in enumerate(self.__layer):
            _x = self.__grid[0] * 0.5 * (lenx - layer.len[0])
            _y = (len(self.__layer) - 1 - idx) * self.__grid[1]
            surface.blit(layer.surface, (_x, _y))
        return surface

    def blit_to(self, surface: pygame.Surface):
        """주어진 표면에 맵을 표시

        매개변수:
            surface: 표시할 표면
        """
        surface.fill(pygame.Color(0, 0, 0, 0))
        cx, cy = surface.get_rect().center
        width, height = self.size
        shift_x = 0.5 * width + self.__cam_x
        shift_y = 0.5 * height + self.__cam_y
        surface.blit(self.surface, (cx - shift_x, cy - shift_y))

    def key_event(self, pressed: Sequence[bool]):
        """맵의 WASD 이동"""
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
