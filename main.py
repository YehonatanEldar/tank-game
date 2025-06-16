import pygame as pg

from constants import (BulletConstants, ControllerConstants, EnemyConstants,
                       GunConstants, PlayerConstants, ScreenConstants)
from controller import XboxController
from entities import (EnemyWave, Level, Obstacle,  # Import the entity classes
                      Player)
from text import DynamicText

# Initialize Pygame
pg.init()
pg.joystick.init()

# Initialize controllers
try:
    controller = XboxController()
except ValueError as e:
    print(f"Error initializing controller: {e}")
    pg.quit()
    exit()

# Set up the display
screen_width, screen_height = ScreenConstants.WIDTH.value, ScreenConstants.HEIGHT.value
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Tank Game")

# Set up clock for controlling the frame rate
clock = pg.time.Clock()

# Initialize player
player = Player(screen_width // 2, screen_height // 2)

# Initialize obstacles
obstacles = [
    Obstacle(100, 100, 50, 50),
    Obstacle(300, 200, 100, 50),
    Obstacle(500, 400, 75, 75)
]

# Initialize enemy waves
enemy_waves = [
    EnemyWave(5, EnemyConstants.SPEED.value, (255, 0, 0), 100),  # Red enemies worth 100 points
    EnemyWave(3, EnemyConstants.SPEED.value * 1.5, (0, 255, 0), 200),  # Green enemies worth 200 points
    EnemyWave(4, EnemyConstants.SPEED.value * 2, (0, 0, 255), 300)  # Blue enemies worth 300 points
]

# Define intervals between waves (in seconds)
wave_intervals = [0, 30, 20]  # Wait 5 seconds for the first wave, 10 seconds for the second wave

# Create a level instance
level = Level(controller, player, obstacles, enemy_waves, wave_intervals)

# text setup
text = DynamicText(
    get_text_func=lambda: f"Score: {level.score}",
    font=pg.font.Font('MinecraftTen-VGORe.ttf', 36),
    color=(255, 255, 255),
    position=(10, 10)
)

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # Check for window close
            running = False

    # Update the level
    level.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the level
    level.draw(screen)

    # Draw the dynamic text
    text.draw(screen)

    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()
