import random
import sys
import pygame
from background import Background, Ground
from bird import Bird
from pipe import Pipe
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    GROUND_Y,
    WHITE,
    BLACK,
    OUTLINE,
    ORANGE_RED,
    GOLD,
    PANEL_BG,
    PIPE_SPEED,
    PIPE_SPACING,
    SCORE_PER_LEVEL,
    SPEED_STEP,
    MAX_PIPE_SPEED,
    RESTART_DELAY,
    HIT_FLASH_TIME,
    SHAKE_TIME,
    SHAKE_STRENGTH,
    MEDALS,
)
from sounds import Sounds
from storage import load_high_score, save_high_score
from ui import draw_text
STATE_READY = "ready"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
def medal_for(score):
    for threshold, name, color in MEDALS:
        if score >= threshold:
            return name, color
    return None
class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.flash_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.flash_overlay.fill(WHITE)
        self.pause_shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.pause_shade.fill((0, 0, 0, 120))
        self.background = Background()
        self.ground = Ground()
        self.sounds = Sounds()
        self.bird = Bird()
        self.pipes = []
        self.ground_offset = 0.0
        self.high_score = load_high_score()
        self.score = 0
        self.new_best = False
        self.state = STATE_READY
        self.paused = False
        self.game_over_timer = 0.0
        self.flash_timer = 0.0
        self.shake_timer = 0.0
        self.running = True
    @property
    def pipe_speed(self):
        speed = PIPE_SPEED + (self.score // SCORE_PER_LEVEL) * SPEED_STEP
        return min(speed, MAX_PIPE_SPEED)
    def reset(self):
        self.bird.reset()
        self.pipes = []
        self.score = 0
        self.new_best = False
        self.state = STATE_READY
        self.paused = False
        self.game_over_timer = 0.0
        self.flash_timer = 0.0
        self.shake_timer = 0.0
    def game_over(self):
        self.state = STATE_GAME_OVER
        self.game_over_timer = 0.0
        self.flash_timer = HIT_FLASH_TIME
        self.shake_timer = SHAKE_TIME
        if self.bird.velocity < 0:
            self.bird.velocity = 0
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_best = True
            save_high_score(self.high_score)
        self.sounds.play("hit")
    def flap(self):
        self.bird.flap()
        self.sounds.play("flap")
    def toggle_pause(self):
        if self.state == STATE_PLAYING:
            self.paused = not self.paused
    def on_action(self):
        if self.paused: 
            self.paused = False
        elif self.state == STATE_READY:
            self.state = STATE_PLAYING
            self.flap()
        elif self.state == STATE_PLAYING:
            self.flap()
        elif self.state == STATE_GAME_OVER and self.game_over_timer >= RESTART_DELAY:
            self.reset()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWFOCUSLOST:
                if self.state == STATE_PLAYING:
                    self.paused = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.on_action()
                elif event.key == pygame.K_p:
                    self.toggle_pause()
                elif event.key == pygame.K_m:
                    self.sounds.toggle()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_action()
    def scroll_world(self, dt):
        speed = self.pipe_speed
        self.background.update(dt)
        self.ground.update(dt, speed)
        for pipe in self.pipes:
            pipe.update(dt, speed)
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        if not self.pipes or self.pipes[-1].x <= SCREEN_WIDTH - PIPE_SPACING:
            self.pipes.append(Pipe(SCREEN_WIDTH + 20))
    def update_score(self):
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                self.sounds.play("score")
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
        self.flash_timer = max(0.0, self.flash_timer - dt)
        self.shake_timer - max(0.0, self.shake_timer - dt)
        if self.paused:
            return
        if self.state == STATE_READY:
            self.bird.idle(dt)
            self.bird.animate(dt)
            self.background.update(dt)
            self.ground.update(dt, PIPE_SPEED)            
        elif self.state == STATE_PLAYING:
            self.bird.update(dt)
            self.bird.animate(dt)
            self.scroll_world(dt)
            self.update_score()
            if self.hit_floor() or self.hit_pipe():
                self.game_over()
        elif self.state == STATE_GAME_OVER:
            self.game_over_timer += dt
            self.bird.update(dt)
            self.hit_floor()
    def draw_ready(self, surface):
        cx = SCREEN_WIDTH // 2
        draw_text(self.screen, "GET READT", 56, (cx, 170))
        draw_text(surface, "Press SPACE or click to flap", 26, (cx, 220))
        if self.high_score > 0:
            draw_text(surface, f"Best: {self.high_score}", 30, (cx, 110), color=GOLD)
        sound_state = "OFF" if self.sounds.muted else "ON"
        draw_text(surface, f"P: pause   M: sound {sound_state}", 22, (cx, 560))
    def draw_paused(self, surface):
        cx = SCREEN_WIDTH // 2
        surface.blit(self.pause_shade, (0, 0))
        draw_text(surface, "PAUSED", 64, (cx, 260))
        draw_text(surface, "Press P or SPACE to resume", 26, (cx, 315))
    def draw_game_over(self, surface):
        cx = SCREEN_WIDTH // 2
        draw_text(surface, "GAME OVER", 56, (cx, 130), color=ORANGE_RED)
        panel = pygame.Rect(0, 0, 250, 160)
        panel.center = (cx, 260)
        pygame.draw.rect(surface, PANEL_BG, panel, border_radius=10)
        pygame.draw.rect(surface, OUTLINE, panel, 4, border_radius=10)
        left, right = cx - 62, cx + 62
        draw_text(surface, "MEDAL", 24, (left, panel.top + 26), color=ORANGE_RED)
        draw_text(surface, "SCORE", 24, (right, panel.top + 26), color=ORANGE_RED)
        draw_text(surface, str(self.score), 42, (right, panel.top + 54))
        draw_text(surface, "BEST", 24, (right, panel.top + 98), color=ORANGE_RED)
        draw_text(surface, str(self.high_score), 42, (right, panel.top + 126))
        medal_center = (left, panel.top + 80)
        medal = medal_for(self.score)
        if medal:
            name, color = medal
            lighter = tuple(min(255, c + 60) for c in color)
            pygame.draw.circle(surface, color, medal_center, 24)
            pygame.draw.circle(surface, lighter, medal_center, 15, 3)
            pygame.draw.circle(surface, OUTLINE, medal_center, 24, 3)
            draw_text(surface, name, 20, (left, panel.top + 122))
        else: 
            pygame.draw.circle(surface, (196, 188, 120), medal_center, 24, 3)
        if self.new_best:
            draw_text(surface, "NEW BEST!", 30, (cx, panel.bottom + 26), color=GOLD)
        if self.game_over_timer >= RESTART_DELAY:
            draw_text(surface, "Press SPACE to restart", 28, (cx, panel.bottom + 66))
    def draw(self):
        surface = self.canvas
        cx = SCREEN_WIDTH // 2
        self.background.draw(surface)
        for pipe in self.pipes:
            pipe.draw(surface)
        self.ground.draw(surface)
        self.bird.draw(surface)
        if self.state == STATE_READY:
            self.draw_ready(surface)
        elif self.state == STATE_PLAYING:
            draw_text(surface, str(self.score), 64, (cx, 70))
        else: 
            self.draw_game_over(surface)
        if self.flash_timer > 0:
            alpha = int(200 * self.flash_timer / HIT_FLASH_TIME)
            self.flash_overlay.set_alpha(alpha)
            surface.blit(self.flash_overlay, (0, 0))
        offset = (0, 0)
        if self.shake_timer > 0:
            strength = max(1, int(SHAKE_STRENGTH * self.shake_timer / SHAKE_TIME))
            offsest = (
                random.randint(-strength, strength),
                random.randint(-strength, strength),
            )
        self.screen.fill(BLACK)
        self.screen.blit(surface, offset)
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