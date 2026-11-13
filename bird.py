import math
import pygame
from settings import (
    BIRD_START_X,
    BIRD_START_Y,
    BIRD_RADIUS,
    BIRD_YELLOW,
    BIRD_ORANGE,
    BIRD_WING,
    WHITE,
    BLACK,
    GRAVITY,
    FLAP_VELOCITY,
    MAX_FALL_SPEED,
)
WING_OFFSETS = (-3, 1, 5, 1)
WING_FPS = 12
class Bird:
    def __init__(self):
        self.x = BIRD_START_X
        self.radius = BIRD_RADIUS
        self.reset()
    def reset(self):
        self.y = float(BIRD_START_Y)
        self.velocity = 0.0
        self.idle_time = 0.0
        self.anim_time = 0.0
    def idle(self, dt):
        self.idle_time += dt
        self.y = BIRD_START_Y + math.sin(self.idle_time * 5) * 6
    def animate(self,dt):
        self.anim_time +=dt
    def flap(self):
        self.velocity = FLAP_VELOCITY
    def update(self, dt):
        self.velocity += GRAVITY * dt
        if self.velocity > MAX_FALL_SPEED:
            self.velocity = MAX_FALL_SPEED
        self.y += self.velocity * dt
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0.0
    def collide_with_rect(self, rect):
        nearest_x = max(rect.left, min(self.x, rect.right))
        nearest_y = max(rect.top, min(self.y, rect.bottom))
        dx = self.x - nearest_x
        dy = self.y - nearest_y
        hit_radius = self.radius - 2
        return dx * dx + dy * dy < hit_radius * hit_radius
    def draw(self, surface):
        r = self.radius
        size = r * 4
        c = size // 2
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(sprite, BIRD_YELLOW, (c, c), r)
        pygame.draw.circle(sprite, BLACK, (c, c), r, 2)
        beak = [(c + r - 2, c-2), (c + r + 9, c + 2), (c + r - 2, c + 6)]
        pygame.draw.polygon(sprite, BIRD_ORANGE, beak)
        pygame.draw.polygon(sprite, BLACK, beak, 2)
        eye = (c + 5, c - 4)
        pygame.draw.circle(sprite, WHITE, eye, 5)
        pygame.draw.circle(sprite, BLACK, (eye[0] + 1, eye[1]), 2)
        frame = int(self.anim_time * WING_FPS) % len(WING_OFFSETS)
        wing = pygame.Rect(c - 11,c + WING_OFFSETS[frame], 14, 9)
        pygame.draw.ellipse(sprite, BIRD_WING, wing)
        pygame.draw.ellipse(sprite, BLACK, wing, 2)
        angle = max(-80.0, min(30.0, 30.0 -self.velocity * 0.08))
        rotated = pygame.transform.rotate(sprite, angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)
        