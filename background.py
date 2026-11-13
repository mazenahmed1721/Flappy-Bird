import random
import pygame
from settings import (
    SCREEN_WIDTH,
    GROUND_Y,
    GROUND_HEIGHT,
    SKY_TOP,
    SKY_BOTTOM,
    CITY_COLOR,
    GROUND_BROWN,
    GROUND_SAND_DARK,
    GROUND_GREEN,
    GROUND_DARK_GREEN,
    OUTLINE,
)
SKYLINE_HEIGHT = 110
SKYLINE_SPEED = 18.0
def _make_gradient(width, height, top, bottom):
    surface = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface
def _make_cloud(scale):
    width,height = int(90* scale), int(46 * scale)
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for cx, cy, radius in ((22, 32, 14), (42, 24, 18), (64, 30, 15), (45, 34, 12)):
        pygame.draw.circle(
            surface, 
            (255, 255, 255, 230),
            (int(cx * scale), int(cy * scale)),
            int(radius * scale),
        )
    return surface
def _make_skyline(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rng = random.Random(7)
    x = 0
    while x < width: 
        building_width = min(rng.randint(24, 46), width - x)
        building_height = rng.randint(int(height * 0.3), height)
        pygame.draw.rect(
            surface,
            CITY_COLOR,
            (x, height - building_height, building_width, building_height),
        )
        x += building_width
    return surface
class Background:
    def __init__(self):
        self.sky = _make_gradient(SCREEN_WIDTH, GROUND_Y, SKY_TOP, SKY_BOTTOM)
        self.skyline = _make_skyline(SCREEN_WIDTH, SKYLINE_HEIGHT)
        self.skyline_offset = 0.0
        rng = random.Random(3)
        self.clouds = []
        for _ in range(5):
            scale = rng.uniform(0.7, 1.3)
            self.clouds.append(
                {
                    "x": rng.uniform(0, SCREEN_WIDTH),
                    "y": rng.uniform(40, 220),
                    "speed": 8 + scale * 8,
                    "img": _make_cloud(scale),
                }
            )
    def update(self, dt):
        self.skyline_offset = (self.skyline_offset + SKYLINE_SPEED * dt) % SCREEN_WIDTH
        for cloud in self.clouds: 
            cloud["x"] -= cloud["speed"] * dt
            if cloud["x"] + cloud["img"].get_width():
                cloud["x"] = SCREEN_WIDTH + random.uniform(10, 80)
                cloud["y"] = random.uniform(40, 220)
    def draw(self, surface):
        surface.blit(self.sky, (0,0))
        for cloud in self.clouds:
            surface.blit(cloud["img"], (int(cloud["x"]), int(cloud["y"])))
        x = -int(self.skyline_offset)
        y = GROUND_Y - SKYLINE_HEIGHT
        surface.blit(self.skyline, (x, y))
        surface.blit(self.skyline, (x + SCREEN_WIDTH, y)) 
class Ground: 
    TILE = 40
    def __init__(self):
        width = SCREEN_WIDTH + self.TILE
        grass_height = 16
        self.surface = pygame.Surface((width, GROUND_HEIGHT)) 
        self.surface.fill(GROUND_BROWN)
        pygame.draw.rect(self.surface, GROUND_GREEN, (0, 0, width, grass_height)) 
        for x in range(-self.TILE, width, self.TILE):
            points = [
                (x, grass_height),
                (x + 20, grass_height),
                (x + 30, 0),
                (x + 10, 0),
            ]
            pygame.draw.polygon(self.surface, GROUND_DARK_GREEN, points)
        pygame.draw.line(
            self.surface, GROUND_SAND_DARK, (0, grass_height + 1), (width, grass_height + 1), 3
        )
        pygame.draw.line(self.surface, OUTLINE, (0,1), (width, 1), 3)
        self.offset = 0.0
    def update(self, dt, speed):
        self.offset = (self.offset + speed * dt) % self.TILE
    def draw(self, surface):
        surface.blit(self.surface, (-int(self.offset), GROUND_Y))