"""키보드의 WASD를 이용한 맵 스크롤"""
import sys
import pygame
from src.util import Tileset, Tilemap

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
    tileset = Tileset("asset/tileset_base.png")
    tilemap = Tilemap(tileset)
    clock = pygame.time.Clock()

    while True:
        tilemap.blit_to(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    tilemap.move(0, -15)
                elif pressed[pygame.K_s]:
                    tilemap.move(0, 15)
                elif pressed[pygame.K_a]:
                    tilemap.move(-15, 0)
                elif pressed[pygame.K_d]:
                    tilemap.move(15, 0)
        pygame.display.flip()
        clock.tick(15)
