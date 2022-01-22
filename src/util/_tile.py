from itertools import product
from typing import TYPE_CHECKING, List, Tuple, Union

import numpy
import pygame

if TYPE_CHECKING:
    from pygame import Surface


class Tileset:
    """에셋의 타일셋을 읽는 클래스"""

    def __init__(self, path: str, size=(64, 64), spacing=0):
        """타일셋 클래스 초기화

        Args:
            path: 타일셋 이미지 파일 경로
            size: 단일 타일 크기
            spacing: 타일간 간격
        """
        self.__tile = []

        image = pygame.image.load(path).convert_alpha()
        image.set_colorkey((0, 0, 0))
        rect = image.get_rect()
        x0 = y0 = spacing
        w, h = rect.size
        dx, dy = size[0] + spacing, size[1] + spacing
        for y, x in product(range(y0, h, dy), range(x0, w, dx)):
            _tile = pygame.Surface(size, pygame.SRCALPHA)
            _tile.blit(image, (0, 0), (x, y, *size))
            self.__tile.append(_tile)

    @property
    def tile(self) -> List["Surface"]:
        """타일 객체 출력"""
        return self.__tile

    def __getitem__(self, key: int) -> "Surface":
        """인덱싱 및 슬라이싱"""
        return self.__tile[key]


class Tilemap:
    """타일셋을 배치하는 타일맵"""

    def __init__(self, tileset: "Tileset", grid=(64, 32), size=(8, 8)):
        """타일맵 초기화

        Args:
            tileset: 타일셋 클래스
            grid: 타일 배치를 위한 격자의 크기
            size: 타일맵의 크기
        """
        self.__tileset = tileset
        self.__grid = grid
        self.__map = numpy.zeros(size, numpy.uint8)
        box_width = size[0] * 0.5 * grid[0] + size[1] * 0.5 * grid[0]
        box_height = size[0] * 0.5 * grid[1] + size[1] * 0.5 * grid[1]
        mod_x = (1 - size[0] / size[1]) * box_width * 0.5
        mod_y = (1 - size[0] / size[1]) * box_height * 0.5
        self.__cam_pos_x = grid[0] * 0.5 + mod_x
        self.__cam_pos_y = -grid[1] + box_height * 0.5

    @property
    def shape(self) -> Tuple[int, int]:
        """타일맵의 너비와 높이"""
        return self.__map.shape

    def __len__(self) -> int:
        """타일맵의 전체 크기"""
        return len(self.__map)

    def __getitem__(self, key) -> Union[int, numpy.ndarray]:
        """지정 좌표의 타일번호 출력"""
        return self.__map[key]

    def __setitem__(self, key, value):
        """지정 좌표의 타일번호 설정"""
        self.__map[key] = value

    def blit_to(self, surface: "Surface"):
        """지정한 표면에 타일맵을 출력"""
        surface.fill(pygame.Color(0, 0, 0, 0))
        xlim, ylim = self.shape
        xcenter = surface.get_rect().centerx
        ycenter = surface.get_rect().centery
        xcam = self.__cam_pos_x - xcenter
        ycam = self.__cam_pos_y - ycenter
        _w, _h = self.__grid
        for _x, _y in product(range(xlim), range(ylim)):
            tile = self.__tileset[self[_x, _y]]
            iso_x = -_x * _w * 0.5 + _y * _w * 0.5
            iso_y = _x * _h * 0.5 + _y * _h * 0.5 - tile.get_size()[1]
            surface.blit(tile, (iso_x - xcam, iso_y - ycam))
        end_x = surface.get_rect().right
        end_y = surface.get_rect().bottom
        pygame.draw.line(surface, (255, 0, 0, 150), (0, ycenter), (end_x, ycenter))
        pygame.draw.line(surface, (255, 0, 0, 150), (xcenter, 0), (xcenter, end_y))
        return

    def move(self, dx: Union[int, float], dy: Union[int, float]):
        """전체 타일맵 이동"""
        self.__cam_pos_x += dx
        self.__cam_pos_y += dy
