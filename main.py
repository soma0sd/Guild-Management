"""키보드의 WASD를 이용한 맵 스크롤"""
import sys
import pygame

from src.tilemap import Tilemap

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
    tilemap = Tilemap("asset/floor_tiles.png", (64, 32), (6, 12))
    clock = pygame.time.Clock()

    while True:
        tilemap.blit_to(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tilemap.key_event(pygame.key.get_pressed())
        cx, cy = display.get_rect().center
        ex = display.get_rect().right
        ey = display.get_rect().bottom
        pygame.draw.line(display, (255, 0, 0, 150), (0, cy), (ex, cy))
        pygame.draw.line(display, (255, 0, 0, 150), (cx, 0), (cx, ey))
        pygame.display.flip()
        clock.tick(30)
