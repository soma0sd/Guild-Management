"""
타일 제어 클래스

클래스:
    Tileset: 타일셋 이미지 관리
    Tilemap: 단일 레이어 타일맵
"""

import itertools
from typing import List, Tuple, Union

import pygame


class Tileset:
    """타일셋 클래스

    타일셋 이미지를 읽어들이고 관리하는 클래스

    매개변수:
        path: 파일 경로
        size: 타일 크기

    """

    def __init__(self, path: str, size: Tuple[int, int]):
        self.__tile: List[pygame.Surface] = []
        self.__tile_size = size
        self.read(path, size)

    def __len__(self) -> int:
        """등록되어 있는 타일 수 출력

        예시:
        literal blocks::

            A = Tileset(...)
            len(A)

        """
        return len(self.__tile)

    def __getitem__(self, key: int) -> pygame.Surface:
        """타일 표면

        예제:
        literal blocks::

            A = Tileset(...)
            tile = A[1]

        """
        return self.__tile[key]

    @property
    def size(self) -> Tuple[int, int]:
        """타일 크기"""
        return self.__tile_size

    def read(self, path: str, size: Tuple[int, int]):
        """파일을 읽어들이는 메서드"""
        self.__tile.clear()
        self.__tile_size = size
        image = pygame.image.load(path).convert_alpha()
        image_width, image_height = image.get_rect().size
        tile_width, tile_height = size
        xrange = range(0, image_width, tile_width)
        yrange = range(0, image_height, tile_height)
        for y, x in itertools.product(yrange, xrange):
            _tile = pygame.Surface(size, pygame.SRCALPHA)
            _tile.blit(image, (0, 0), (x, y, *size))
            self.__tile.append(_tile)


class Tilemap:
    """타일맵 클래스

    타일을 배치하는 단독 레이어 타일맵.
    동적으로 맵크기 확장.

    매개변수:
        grid: 타일배치 격자의 크기
        size: 초기 맵 사이즈

    """

    def __init__(
        self,
        grid: Tuple[int, int],
        size: Tuple[int, int] = (2, 2),
    ):
        self.__tick_x = 0.5 * grid[0]
        self.__tick_y = 0.5 * grid[1]
        self.__tile_map = [[-1]]
        self.__tile_palette: List[pygame.Surface] = []
        self._extend(*size)

    def __setitem__(
        self,
        key: Tuple[Union[int, slice], Union[int, slice]],
        tile: Union[pygame.Surface, None],
    ):
        """타일 배치

        `Tilemap[x, y] = 타일이미지`로 사용

        예시:
        literal blocks::

            A = Tilemap(...)
            A[3, 2:3] = tile

        """

        def vrange(key, axis: int):
            if isinstance(key, int):
                return [key]
            elif isinstance(key, slice):
                return range(
                    key.start if key.start else 0,
                    key.stop if key.stop else self.len[axis],
                    key.step if key.step else 1,
                )
            else:
                return None

        if not tile is None:
            if tile not in self.__tile_palette:
                self.__tile_palette.append(tile)
            tid = self.__tile_palette.index(tile)
        else:
            tid = -1
        for _xi in vrange(key[0], 0):
            for _yi in vrange(key[1], 1):
                self._extend(_xi, _yi)
                self.__tile_map[_xi][_yi] = tid

    @property
    def surface(self) -> pygame.Surface:
        """배치한 타일을 그래픽 표면으로 출력"""
        _w, _h = self.len
        map_width, map_height = self.size
        surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        shift_x = self.__tick_x * (_w - 1)
        for _xi, _yi in itertools.product(range(_w), range(_h)):
            if self.__tile_map[_xi][_yi] < 0:
                continue
            tile = self.__tile_palette[self.__tile_map[_xi][_yi]]
            iso_x = -self.__tick_x * _xi + self.__tick_x * _yi + shift_x
            iso_y = self.__tick_y * _xi + self.__tick_y * _yi
            surface.blit(tile, (iso_x, iso_y))
        cx, cy = surface.get_rect().center
        return surface

    @property
    def size(self) -> Tuple[int, int]:
        """타일맵 이미지의 크기(픽셀)"""
        _w, _h = self.len
        width = self.__tick_x * (_w + _h)
        height = self.__tick_y * (_w + _h + 2)
        return width, height

    @property
    def len(self) -> Tuple[int, int]:
        """타일맵의 배치단위 크기"""
        len_x = len(self.__tile_map)
        len_y = min([len(self.__tile_map[i]) for i in range(len_x)])
        return len_x, len_y

    def _extend(self, index_x: int, index_y: int):
        """배치 타일이 기존 범위를 초과하는 경우 범위를 확장"""
        while self.len[0] <= index_x:
            self.__tile_map.append([-1 for _ in range(self.len[1])])
        for idx in range(self.len[0]):
            while len(self.__tile_map[idx]) <= index_y:
                self.__tile_map[idx].append(-1)
