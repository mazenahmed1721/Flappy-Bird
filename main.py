import sys
import pygame
from bird import Bird
from pipe import Pipe
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    SKY_BLUE,
    GROUND_BROWN,
    GROUND_GREEN,
    GROUND_DARK_GREEN,
    GROUND_Y,
    GROUND_HEIGHT,
    PIPE_SPEED,
    PIPE_SPACING,
    RESTART_DELAY,
)
from ui import draw_text
STATE_READY = "ready"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

def draw_ground(surface, offset):
    pygame.draw.rect( surface, GROUND_BROWN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(surface, GROUND_GREEN, (0, GROUND_Y, SCREEN_WIDTH, 12))
    for x in range(-40, SCREEN_WIDTH + 40, 40):
        stripe_x = x-int(offset)
        pygame.draw.rect(surface, GROUND_DARK_GREEN, (stripe_x, GROUND_Y, 20, 12))
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = []
        self.ground_offset = 0.0
        self.state = STATE_READY
        self.game_over_timer = 0.0
        self.running = True
    def reset(self):
        self.bird.reset()
        self.pipes = []
        self.state = STATE_READY
        self.game_over_timer = 0.0
    def game_over(self):
        self.state = STATE_GAME_OVER
        self.game_over_timer = 0.0
        if self.bird.velocity < 0:
            self.bird.velocity = 0
    def on_action(self):
        if self.state == STATE_READY:
            self.state = STATE_PLAYING
            self.bird.flap()
        elif self.state == STATE_PLAYING:
            self.bird.flap()
        elif self.state == STATE_GAME_OVER and self.game_over_timer >= RESTART_DELAY:
            self.reset()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.on_action()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_action()
    def scroll_ground(self, dt):
        self.ground_offset = (self.ground_offset + PIPE_SPEED * dt) % 40
    def scroll_pipes(self, dt):
        for pipe in self.pipes:
            pipe.update(dt, PIPE_SPEED)
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        if not self.pipes or self.pipes[-1].x <= SCREEN_WIDTH - PIPE_SPACING:
            self.pipes.append(Pipe(SCREEN_WIDTH + 20))
    def hit_floor(self):
        if self.bird.y + self.bird.radius >= GROUND_Y:
            self.bird.y = GROUND_Y - self.bird.radius
            self.bird.velocity = 0.0
            return True
        return False
    def hit_pipe(self):
        for pipe in self.pipes:
            for rect in pipe.rects():
                if self.bird.collide_with_rect(rect):
                    return True
        return False
    def update(self, dt):
        if self.state == STATE_READY:
            self.bird.idle(dt)
            self.scroll_ground(dt)
        elif self.state == STATE_PLAYING:
            self.bird.update(dt)
            self.scroll_ground(dt)
            self.scroll_pipes(dt)
            if self.hit_floor() or self.hit_pipe():
                self.game_over()
        elif self.state == STATE_GAME_OVER:
            self.game_over_timer += dt
            self.bird.update(dt)
            self.hit_floor()
    def draw(self):
        cx = SCREEN_WIDTH // 2
        self.screen.fill(SKY_BLUE)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        draw_ground(self.screen, self.ground_offset)
        self.bird.draw(self.screen)
        if self.state == STATE_READY:
            draw_text(self.screen, "GET READY", 56, (cx, 170))
            draw_text(self.screen, "Press SPACE or click to flap", 26, (cx, 220))
        elif self.state == STATE_GAME_OVER:
            draw_text(self.screen, "GAME OVER", 56, (cx, 200))
            if self.game_over_timer >= RESTART_DELAY:
                draw_text(self.screen, "PRess SPACE to restart", 28, (cx,250))
        pygame.display.flip()
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    Game().run()