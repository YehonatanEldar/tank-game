import pygame as pg

class XboxController:
    def __init__(self, controller_index=0):
        pg.joystick.init()
        if pg.joystick.get_count() == 0:
            raise ValueError("No joystick devices detected. Please connect a controller.")
        
        if controller_index >= pg.joystick.get_count():
            raise ValueError(f"Invalid joystick device number: {controller_index}. Only {pg.joystick.get_count()} device(s) available.")
        
        self.joystick = pg.joystick.Joystick(controller_index)
        self.joystick.init()

    def get_axis(self, axis_index):
        """Get the value of a specific axis (e.g., thumbsticks)."""
        return self.joystick.get_axis(axis_index)

    def get_button(self, button_index):
        """Check if a specific button is pressed."""
        return self.joystick.get_button(button_index)

    def get_hat(self, hat_index):
        """Get the state of a specific hat (e.g., D-pad)."""
        return self.joystick.get_hat(hat_index)

    def get_name(self):
        """Get the name of the controller."""
        return self.joystick.get_name()