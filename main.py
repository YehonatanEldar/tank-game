import numpy as np
import pygame as pg

from constants import ScreenConstants
from controller import XboxController
from entities import EnemyWave, Gun, Player  # Import the entity classes

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
pg.display.set_caption("Simple Pygame Loop")

# Set up clock for controlling the frame rate
clock = pg.time.Clock()

# Initialize entities
player = Player(screen_width // 2, screen_height // 2)
enemy_wave = EnemyWave(5)

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # Check for window close
            running = False

    # Handle player input
    player.handle_input(controller)
    player.gun.handle_input(controller)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the player
    player.draw(screen)
    # Draw the gun
    player.gun.draw(screen)
    # Update and draw bullets
    for bullet in player.gun.bullets:
        bullet.update()  # Update bullet position
        bullet.draw(screen)

    # enemy wave
    enemy_wave.update(player)  # Update enemy wave state
    enemy_wave.draw(screen)  # Draw the enemy wave
    

    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()
