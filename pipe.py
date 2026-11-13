import random
import pygame
from settings import (
    PIPE_WIDTH,
    PIPE_GAP,
    PIPE_MARGIN,
    PIPE_CAP_HEIGHT,
    PIPE_CAP_EXTRA,
    PIPE_GREEN,
    PIPE_LIGHT,
    PIPE_DARK,
    OUTLINE,
    GROUND_Y,
)
def _draw_block(surface, rect):
    pygame.draw.rect(surface, PIPE_GREEN, rect)
    pygame.draw.rect(surface, PIPE_LIGHT, (rect.left + 4, rect.top, 8, rect.height))
    pygame.draw.rect(surface, PIPE_DARK, (rect.right -12, rect.top, 8, rect.height))
    pygame.draw.rect(surface, OUTLINE, rect, 3)
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
        return self.x + self.width + PIPE_CAP_EXTRA < 0
    def rects(self):
        x = int(self.x)
        cap_x = x - PIPE_CAP_EXTRA
        cap_width = self.width + 2 * PIPE_CAP_EXTRA
        top_body = pygame.Rect(x, 0, self.width, self.gap_top - PIPE_CAP_HEIGHT)
        top_cap = pygame.Rect(
            cap_x, self.gap_top - PIPE_CAP_HEIGHT, cap_width, PIPE_CAP_HEIGHT
        )
        bottom_cap = pygame.Rect(cap_x, self.gap_bottom, cap_width, PIPE_CAP_HEIGHT)
        bottom_body = pygame.Rect(
            x, 
            self.gap_bottom + PIPE_CAP_HEIGHT,
            self.width,
            GROUND_Y - self.gap_bottom - PIPE_CAP_HEIGHT,
        )
        return [top_body, top_cap, bottom_cap, bottom_body]
    def draw(self, surface):
        for rect in self.rects():
            _draw_block(surface, rect)
            