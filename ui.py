import pygame
from settings import WHITE, BLACK
_font_cache = {}
def get_font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
def get_font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
def draw_text(surface, text, size, center, color=WHITE, outline=BLACK):
    font = get_font(size)
    base = font.render(text, True, color)
    rect = base.get_rect(center=center)
    if outline:
        edge = font.render(text, True, outline)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)):
            surface.blit(edge, rect.move(dx, dy))
    surface.blit(base, rect)
