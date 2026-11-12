import sys
import pygame
from bird import Bird
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    SKY_BLUE,
    GROUND_BROWN,
    GROUND_GREEN,
    GROUND_Y,
    GROUND_HEIGHT,
)
def draw_ground(surface):
    pygame.draw.rect( surface, GROUND_BROWN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(surface, GROUND_GREEN, (0, GROUND_Y, SCREEN_WIDTH, 12))
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    bird = Bird()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    bird.flap()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird.flap()
        bird.update(dt)
        screen.fill(SKY_BLUE)
        draw_ground(screen)
        bird.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()