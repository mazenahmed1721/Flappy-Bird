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
    OUTLINE,
    ORANGE_RED,
    GOLD,
    PANEL_BG,
)
from storage import load_high_score, save_high_score
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
        self.high_score = load_high_score()
        self.score = 0
        self.new_best = False
        self.state = STATE_READY
        self.game_over_timer = 0.0
        self.running = True
    def reset(self):
        self.bird.reset()
        self.pipes = []
        self.score = 0
        self.new_best = False
        self.state = STATE_READY
        self.game_over_timer = 0.0
    def game_over(self):
        self.state = STATE_GAME_OVER
        self.game_over_timer = 0.0
        if self.bird.velocity < 0:
            self.bird.velocity = 0
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_best = True
            save_high_score(self.high_score)
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
    def update_score(self):
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
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
            self.update_score()
            if self.hit_floor() or self.hit_pipe():
                self.game_over()
        elif self.state == STATE_GAME_OVER:
            self.game_over_timer += dt
            self.bird.update(dt)
            self.hit_floor()
    def draw_game_over(self):
        cx = SCREEN_WIDTH // 2
        draw_text(self.screen, "GAME OVER", 56, (cx, 140), color=ORANGE_RED)
        panel = pygame.Rect(0, 0, 250,120)
        panel.center = (cx, 260)
        pygame.draw.rect(self.screen, PANEL_BG, panel, border_radius=10)
        pygame.draw.rect(self.screen, OUTLINE, panel, 4, border_radius=10)
        left, right = cx - 62, cx + 62
        draw_text(self.screen, "SCORE", 26, (left, panel.top + 30), color=ORANGE_RED)
        draw_text(self.screen, str(self.score), 52, (left, panel.top + 72))
        draw_text(self.screen, "BEST", 26, (right, panel.top + 30), color=ORANGE_RED)
        draw_text(self.screen,str(self.high_score), 52, (right, panel.top + 72))
        if self.new_best:
            draw_text(self.screen,"NEW BEST!", 30, (cx, panel.bottom + 26), color=GOLD)
        if self.game_over_timer >= RESTART_DELAY:
            draw_text(self.screen,"Press SPACE to restart", 28, (cx, panel.bottom + 66))
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
            if self.high_score > 0:
                draw_text(self.screen, f"best: {self.high_score}", 30, (cx, 110), color=GOLD)
        elif self.state == STATE_PLAYING:
            draw_text(self.screen, str(self.score), 64, (cx, 70))
        else: 
            self.draw_game_over()
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