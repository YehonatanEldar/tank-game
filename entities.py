import numpy as np
import pygame as pg

from constants import (BulletConstants, ControllerConstants, EnemyConstants,
                       EnemyWaveConstants, GunConstants, PlayerConstants, ScreenConstants)


class Entity:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color  # Color of the entity

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PlayerConstants.WIDTH.value, PlayerConstants.HEIGHT.value, PlayerConstants.COLOR.value)
        self.speed = PlayerConstants.SPEED.value  # Movement speed
        self.gun = Gun(self)  # Create a gun for the player

    def handle_input(self, controller):
        # Get joystick axis values
        left_x = controller.get_axis(0)  # Left joystick X-axis
        left_y = controller.get_axis(1)  # Left joystick Y-axis

        # Calculate movement
        dx = left_x * self.speed
        dy = left_y * self.speed

        # Prevent moving outside the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > ScreenConstants.WIDTH.value:
            dx = ScreenConstants.WIDTH.value - self.rect.right
        if self.rect.top + dy < 0:
            dy = -self.rect.top
        if self.rect.bottom + dy > ScreenConstants.HEIGHT.value:
            dy = ScreenConstants.HEIGHT.value - self.rect.bottom

        self.move(dx, dy)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)


class Gun(Entity):
    MAX_TOLERANCE = 0.7  # Define tolerance for detecting maximum joystick position

    def __init__(self, player, angle=0):
        super().__init__(player.rect.centerx, player.rect.centery, GunConstants.WIDTH.value, GunConstants.WIDTH.value, GunConstants.COLOR.value)
        self.angle = angle  # Initial angle of the gun
        self.length = GunConstants.LENGTH.value  # Length of the gun
        self.player = player  # Store a reference to the player
        self.bullets = []  # List to store bullets
        self.shoot_pressed = False  # Track shoot button state
        self.last_max_angle = angle  # Track the last maximum angle

    def handle_input(self, controller):
        # Get joystick axis values for gun rotation
        right_x = controller.get_axis(2)
        right_y = controller.get_axis(3)

        # If joystick is moved, update the angle temporarily
        if right_x != 0 or right_y != 0:
            self.angle = np.degrees(np.arctan2(right_y, right_x))

            # Check if the joystick has reached a new maximum position within tolerance
            if abs(right_x) >= self.MAX_TOLERANCE or abs(right_y) >= self.MAX_TOLERANCE:
                self.last_max_angle = self.angle  # Update the last maximum angle
        else:
            # If joystick returns to (0, 0), revert to the last maximum angle
            self.angle = self.last_max_angle

        # Check for shooting input (button ID from constants)
        if controller.get_button(ControllerConstants.SHOOT_BUTTON_ID.value):  # Button ID for shooting
            if not self.shoot_pressed:  # Only shoot if the button was not already pressed
                self.shoot()
                self.shoot_pressed = True  # Mark the button as pressed
        else:
            self.shoot_pressed = False  # Reset when the button is released

    def move(self):
        # Update the position of the gun based on the player's position
        self.rect.center = (
            self.player.rect.centerx + np.cos(np.radians(self.angle)) * self.length,
            self.player.rect.centery + np.sin(np.radians(self.angle)) * self.length
        )

    def shoot(self):
        # Calculate the tip of the gun
        tip_x = self.player.rect.centerx + np.cos(np.radians(self.angle)) * self.length
        tip_y = self.player.rect.centery + np.sin(np.radians(self.angle)) * self.length

        # Create a new bullet at the tip of the gun
        bullet = Bullet(tip_x, tip_y, self.angle)
        self.bullets.append(bullet)

    def draw(self, surface):
        pg.draw.line(
            surface,
            self.color,
            self.player.rect.center,
            (
                self.player.rect.centerx + np.cos(np.radians(self.angle)) * self.length,
                self.player.rect.centery + np.sin(np.radians(self.angle)) * self.length
            ),
            5  # Line thickness
        )

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)


class Bullet(Entity):
    def __init__(self, x, y, angle):
        super().__init__(x, y, BulletConstants.RADIUS.value * 2, BulletConstants.RADIUS.value * 2, BulletConstants.COLOR.value)  # Bullets are small circles
        self.angle = angle
        self.speed = BulletConstants.SPEED.value  # Speed of the bullet

    def update(self):
        # Move the bullet in the direction of its angle
        self.rect.x += int(np.cos(np.radians(self.angle)) * self.speed)
        self.rect.y += int(np.sin(np.radians(self.angle)) * self.speed)

    def is_outside_screen(self):
        # Check if the bullet is outside the screen
        return (
            self.rect.right < 0 or
            self.rect.left > ScreenConstants.WIDTH.value or
            self.rect.bottom < 0 or
            self.rect.top > ScreenConstants.HEIGHT.value
        )

    def draw(self, surface):
        # Draw the bullet as a circle
        pg.draw.circle(surface, self.color, self.rect.center, BulletConstants.RADIUS.value)


class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, EnemyConstants.WIDTH.value, EnemyConstants.HEIGHT.value, EnemyConstants.COLOR.value)
        self.speed = EnemyConstants.SPEED.value  # Movement speed

    def update(self, player):
        # Move toward the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed

        # Prevent moving outside the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > ScreenConstants.WIDTH.value:
            dx = ScreenConstants.WIDTH.value - self.rect.right
        if self.rect.top + dy < 0:
            dy = -self.rect.top
        if self.rect.bottom + dy > ScreenConstants.HEIGHT.value:
            dy = ScreenConstants.HEIGHT.value - self.rect.bottom

        self.move(dx, dy)

        bullets = player.gun.bullets
        # Check for collisions with bullets
        for bullet in bullets:
            distance = np.sqrt((self.rect.centerx - bullet.rect.centerx) ** 2 + (self.rect.centery - bullet.rect.centery) ** 2)
            if distance < EnemyConstants.WIDTH.value // 2 + BulletConstants.RADIUS.value:
                # Handle collision with bullet (e.g., remove enemy, remove bullet, etc.)
                print("Enemy hit by bullet!")
                bullets.remove(bullet)
                return False

        # Check for collisions with player
        if self.rect.colliderect(player.rect):
            # Handle collision with player (e.g., reduce health, end game, etc.)
            print("Enemy collided with player!")
            exit()

        return True

    def draw(self, surface):
        # Draw the enemy as a circle
        pg.draw.circle(surface, self.color, self.rect.center, EnemyConstants.WIDTH.value // 2)


class EnemyWave:
    def __init__(self, num_enemies):
        self.enemies = []
        for _ in range(num_enemies):
            # Start on random pos on top bottom left or right
            side = np.random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = np.random.randint(0, ScreenConstants.WIDTH.value)
                y = 0
            elif side == 'bottom':
                x = np.random.randint(0, ScreenConstants.WIDTH.value)
                y = ScreenConstants.HEIGHT.value - EnemyConstants.HEIGHT.value
            elif side == 'left':
                x = 0
                y = np.random.randint(0, ScreenConstants.HEIGHT.value)
            else:
                x = ScreenConstants.WIDTH.value - EnemyConstants.WIDTH.value
                y = np.random.randint(0, ScreenConstants.HEIGHT.value)
            enemy = Enemy(x, y)
            self.enemies.append(enemy)

    def update(self, player):
        for enemy in self.enemies:
            if not enemy.update(player):
                self.enemies.remove(enemy)

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)