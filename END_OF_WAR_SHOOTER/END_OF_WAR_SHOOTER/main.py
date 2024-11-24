import os
import sys
import random
import pygame
from components import Ship, Laser, Meteor, Explosion


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Debug prints
print("Current working directory:", os.getcwd())
print("Resource path for audio:", resource_path("space shooter/audio"))
print("Resource path for images:", resource_path("space shooter/images"))
print("Files in current directory:", os.listdir("."))

# Initialize Pygame
pygame.init()
print(f"Pygame version: {pygame.__version__}")
print(f"Pygame initialization status: {pygame.get_init()}")

# Initialize audio
pygame.mixer.init()

# Set up the display
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("END OF WAR SHOOTER CREATED BY LULZSEC")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# background
background_image = pygame.image.load(
    # file for background 

    resource_path("space shooter/images/background.jpg")
)

# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# timer for meteor spawning
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 1000)  # Spawn meteor every 500ms
### time was 500
# sprite creation
ship = Ship(spaceship_group)

# Load sound effects
laser_sound = pygame.mixer.Sound(resource_path("space shooter/audio/laser.wav"))
explosion_sound = pygame.mixer.Sound(resource_path("space shooter/audio/explosion.wav"))
background_music = pygame.mixer.Sound(
    resource_path("space shooter/audio/game_music.wav")
)
background_music.play(loops=-1)  # Start playing background music on loop


# Game states
class GameState:
    WELCOME = "welcome"
    PLAYING = "playing"
    GAME_OVER = "game_over"


# Font setup
font_path = resource_path("space shooter/images/Oxanium-Bold.ttf")
try:
    game_font = pygame.font.Font(font_path, 40)
except:
    print(f"Could not load font from {font_path}, using default")
    game_font = pygame.font.Font(None, 40)

# Game state
current_state = GameState.WELCOME
score = 0


def draw_text(text, pos):
    text_surface = game_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=pos)
    display_surface.blit(text_surface, text_rect)


# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == GameState.WELCOME:
                current_state = GameState.PLAYING
            elif current_state == GameState.PLAYING:
                Laser(laser_group, ship.rect.midtop)
                laser_sound.play()
            elif current_state == GameState.GAME_OVER:
                # Reset game
                current_state = GameState.PLAYING
                score = 0
                ## changed
                meteor_group.empty()
                laser_group.empty()
                explosion_group.empty()

        if event.type == meteor_timer and current_state == GameState.PLAYING:
            x_pos = random.randint(0, WINDOW_WIDTH)
            meteor_speed = random.uniform(4, 8)
            Meteor(meteor_group, (x_pos, -50), meteor_speed)

    # Draw background
    display_surface.blit(background_image, (0, 0))

    if current_state == GameState.WELCOME:
        draw_text("END OF WAR SHOOTER  DEVELOPED BY LULZSEC", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        draw_text("Click to Start", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    elif current_state == GameState.PLAYING:
        ## done by us !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! for background 
        # Check for collisions between lasers and meteors
        for laser in laser_group:
            meteors_hit = pygame.sprite.spritecollide(laser, meteor_group, True)
            if meteors_hit:
                laser.kill()
                score += len(meteors_hit)
                for meteor in meteors_hit:
                    Explosion(explosion_group, meteor.rect.center)
                    explosion_sound.play()

        # Check for collisions between ship and meteors
        if pygame.sprite.spritecollide(ship, meteor_group, True):
            current_state = GameState.GAME_OVER
            Explosion(explosion_group, ship.rect.center)
            explosion_sound.play()

        # Update and draw sprites
        spaceship_group.draw(display_surface)
        spaceship_group.update()
        laser_group.draw(display_surface)
        laser_group.update()
        meteor_group.draw(display_surface)
        meteor_group.update()
        explosion_group.draw(display_surface)
        explosion_group.update()

        # Draw score
        draw_text(f"Score: {score}", (WINDOW_WIDTH - 100, 50))

    elif current_state == GameState.GAME_OVER:
        # done by us 
        
        ### done by us 

        explosion_group.draw(display_surface)
        explosion_group.update()
        background_image = pygame.image.load(
    # file for background 

    resource_path("space shooter/images/my.jpg")
    )
    
        #draw_text("CRETED BY LULZSEC", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        #draw_text(f"Final Score: {score}", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        #draw_text("Click to Play Again", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    # Update display
    pygame.display.update()
    clock.tick(60)
