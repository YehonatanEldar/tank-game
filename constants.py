from enum import Enum


class PlayerConstants(Enum):
    SPEED = 5
    COLOR = (34, 139, 34)  # Green color for the player
    WIDTH = 50
    HEIGHT = 75  # Height of the player rectangle


class GunConstants(Enum):
    LENGTH = 55  # Length of the gun
    COLOR = (105, 105, 105)  # Gray color for the gun
    WIDTH = 10  # Width of the gun rectangle


class BulletConstants(Enum):
    RADIUS = 3  # Radius of the bullet
    COLOR = (255, 215, 0)  # Yellow color for the bullet
    SPEED = 10  # Speed of the bullet


class ControllerConstants(Enum):
    SHOOT_BUTTON_ID = 5  # Button ID for shooting


class EnemyConstants(Enum):
    SPEED = 2
    COLOR = (255, 0, 0)  # Red color for enemies
    WIDTH = 40
    HEIGHT = 40

class ObstaclesConstants(Enum):
    COLOR = (210, 180, 140)  # Gray color for obstacles
    WIDTH = 60  # Width of the obstacle rectangle
    HEIGHT = 60  # Height of the obstacle rectangle


class EnemyWaveConstants(Enum):
    SIZE = 5  # Number of enemies per wave
    SPAWN_INTERVAL = 3000  # Time in milliseconds between enemy spawns


class ScreenConstants(Enum):
    WIDTH = 1600
    HEIGHT = 900