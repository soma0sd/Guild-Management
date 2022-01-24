"""키보드의 WASD를 이용한 맵 스크롤"""
import sys

import pygame

from src import World, Tileset

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
    tileset = Tileset("asset/floor_tiles.png", (64, 64))
    world = World((64, 32), 2)

    world[0, :6, :4] = tileset[0]
    world[1, :6:2, :4] = tileset[3]
    cx, cy = display.get_rect().center

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        world.blit_to(display)
        world.key_event(pygame.key.get_pressed())
        ex = display.get_rect().right
        ey = display.get_rect().bottom
        pygame.draw.line(display, (255, 0, 0, 150), (0, cy), (ex, cy))
        pygame.draw.line(display, (255, 0, 0, 150), (cx, 0), (cx, ey))
        pygame.display.flip()
        clock.tick(30)
