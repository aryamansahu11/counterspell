import pygame
import random
from settings import *
from components import Ship, Laser, Meteor, PowerUp, Explosion


class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("END OF WAR SHOOTER")

        # Load assets
        self.background = load_image("background.png")
        self.heart_image = load_image("heart.png")  # You'll need to create this
        self.laser_sound = load_sound("laser.wav")
        self.explosion_sound = load_sound("explosion.wav")
        self.powerup_sound = load_sound("powerup.wav")  # You'll need this sound
        self.background_music = load_sound("game_music.wav")
        self.background_music.play(loops=-1)

        self.reset_game()

    def reset_game(self):
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.spaceship_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        # Create player
        self.ship = Ship(self.spaceship_group)

        # Game state
        self.state = "welcome"
        self.score = 0
        self.lives = INITIAL_LIVES
        self.meteor_speed = INITIAL_METEOR_SPEED
        self.meteor_spawn_time = METEOR_SPAWN_TIME
        self.shield_active = False
        self.shield_timer = 0

        # Setup meteor spawning
        self.meteor_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_timer, self.meteor_spawn_time)

    def increase_difficulty(self):
        if self.score > 0 and self.score % DIFFICULTY_INCREASE_SCORE == 0:
            # Increase meteor speed
            self.meteor_speed = min(
                self.meteor_speed + METEOR_SPEED_INCREMENT, MAX_METEOR_SPEED
            )
            # Decrease spawn time
            self.meteor_spawn_time = max(
                self.meteor_spawn_time - METEOR_SPAWN_REDUCTION, MIN_METEOR_SPAWN_TIME
            )
            pygame.time.set_timer(self.meteor_timer, self.meteor_spawn_time)

    def spawn_meteor(self):
        if self.state == "playing":
            x_pos = random.randint(0, WINDOW_WIDTH)
            Meteor(self.meteor_group, (x_pos, -50), self.meteor_speed)

            # Chance to spawn power-up
            if random.random() < POWERUP_SPAWN_CHANCE:
                x_pos = random.randint(0, WINDOW_WIDTH)
                PowerUp(self.powerup_group, (x_pos, -50))

    def handle_collisions(self):
        # Laser hits meteor
        for laser in self.laser_group:
            meteors_hit = pygame.sprite.spritecollide(laser, self.meteor_group, True)
            if meteors_hit:
                self.explosion_sound.play()
                laser.kill()
                self.score += len(meteors_hit)
                self.increase_difficulty()
                for meteor in meteors_hit:
                    Explosion(self.explosion_group, meteor.rect.center)

        # Check power-up collection
        powerups_hit = pygame.sprite.spritecollide(self.ship, self.powerup_group, True)
        for powerup in powerups_hit:
            self.powerup_sound.play()
            if powerup.type == "shield":
                self.shield_active = True
                self.shield_timer = pygame.time.get_ticks()

        # Ship hits meteor
        if not self.shield_active and pygame.sprite.spritecollide(
            self.ship, self.meteor_group, True
        ):
            self.explosion_sound.play()
            self.lives -= 1
            Explosion(self.explosion_group, self.ship.rect.center)
            if self.lives <= 0:
                self.state = "game_over"

    def update_shield(self):
        if self.shield_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer > SHIELD_DURATION:
                self.shield_active = False

    def draw_lives(self):
        for i in range(self.lives):
            x = 50 + i * (self.heart_image.get_width() + 10)
            self.display_surface.blit(self.heart_image, (x, 50))

    def draw(self):
        # Draw background
        self.display_surface.blit(self.background, (0, 0))

        if self.state == "welcome":
            center_x = WINDOW_WIDTH // 2
            center_y = WINDOW_HEIGHT // 2
            self.draw_text("END OF WAR SHOOTER", (center_x, center_y - 50))
            self.draw_text("Click to Start", (center_x, center_y + 50))

        elif self.state == "playing":
            # Draw all sprite groups
            for group in [
                self.spaceship_group,
                self.laser_group,
                self.meteor_group,
                self.powerup_group,
                self.explosion_group,
            ]:
                group.draw(self.display_surface)

            # Draw UI
            self.draw_lives()
            self.draw_text(f"Score: {self.score}", (WINDOW_WIDTH - 100, 50))

            # Draw shield effect if active
            if self.shield_active:
                pygame.draw.circle(
                    self.display_surface,
                    (64, 64, 255, 128),
                    self.ship.rect.center,
                    50,
                    width=2,
                )

        elif self.state == "game_over":
            self.explosion_group.draw(self.display_surface)
            center_x = WINDOW_WIDTH // 2
            center_y = WINDOW_HEIGHT // 2
            self.draw_text("CREATED BY LULZSEC", (center_x, center_y - 50))
            # self.draw_text("GAME OVER", (center_x, center_y - 50))
            self.draw_text(f"Final Score: {self.score}", (center_x, center_y))
            self.draw_text("Click to Play Again", (center_x, center_y + 50))

    def update(self):
        if self.state == "playing":
            self.update_shield()
            self.handle_collisions()
            for group in [
                self.spaceship_group,
                self.laser_group,
                self.meteor_group,
                self.powerup_group,
            ]:
                group.update()
        self.explosion_group.update()
