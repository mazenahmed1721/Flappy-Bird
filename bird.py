import pygame
from settings import (
    BIRD_START_X,
    BIRD_START_Y,
    BIRD_RADIUS,
    BIRD_YELLOW,
    BIRD_ORANGE,
    WHITE,
    BLACK,
    GRAVITY,
    FLAP_VELOCITY,
    MAX_FALL_SPEED,
    GROUND_Y,
)
class Bird:
    def __init__(self):
        self.x = BIRD_START_X
        self.y = float(BIRD_START_Y)
        self.velocity = 0.0
        self.radius = BIRD_RADIUS
    def reset(self):
        self.y = float(BIRD_START_Y)
        self.velocity = 0.0
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
        if self.y + self.radius > GROUND_Y:
            self.y = GROUND_Y - self.radius
            self.velocity = 0.0
    def draw(self, surface):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(surface, BIRD_YELLOW, center, self.radius)
        pygame.draw.circle(surface, BLACK, center, self.radius, 2)
        eye = (center[0] + 5, center[1] - 4)
        pygame.draw.circle(surface, WHITE, eye, 5)
        pygame.draw.circle(surface, BLACK, (eye[0] + 1, eye[1]), 2)
        beak = [
            (center[0] + self.radius - 2, center[1] -2),
            (center[0] + self.radius + 9, center[1] + 2),
            (center[0] + self.radius - 2, center[1] + 6),
        ]
        pygame.draw.polygon(surface, BIRD_ORANGE, beak)
        pygame.draw.polygon(surface, BLACK, beak, 2)
        