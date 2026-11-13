import random
import pygame
from settings import (
    PIPE_WIDTH,
    PIPE_GAP,
    PIPE_MARGIN,
    PIPE_GREEN,
    OUTLINE,
    GROUND_Y,
)
class Pipe:
    def __init__(self, x):
        self.x = float(x)
        self.width = PIPE_WIDTH
        self.gap_top = random.randint(PIPE_MARGIN, GROUND_Y - PIPE_GAP - PIPE_MARGIN)
        self.gap_bottom = self.gap_top + PIPE_GAP
        self.passed = False
    def update(self, dt, speed):
        self.x -= speed * dt
    def is_off_screen(self):
        return self.x + self.width < 0
    def rects(self):
        x = int(self.x)
        top = pygame.Rect(x, 0, self.width, self.gap_top)
        bottom = pygame.Rect(x,self.gap_bottom, self.width, GROUND_Y - self.gap_bottom)
        return [top, bottom]
    def draw(self, surfae):
        for ret in self.rects():
            pygame.draw.rect(surfae, PIPE_GREEN, ret)
            pygame.draw.rect(surfae, OUTLINE, ret, 3)
            