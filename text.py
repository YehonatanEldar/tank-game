import pygame as pg

class DynamicText:
    def __init__(self, get_text_func, font, color, position):
        """
        Initializes the DynamicText object.

        :param get_text_func: A function that returns the current string to display.
        :param font: A pygame font object for rendering the text.
        :param color: A tuple representing the color of the text (e.g., (255, 255, 255)).
        :param position: A tuple representing the position (x, y) to render the text.
        """
        self.get_text_func = get_text_func
        self.font = font
        self.color = color
        self.position = position

    def draw(self, screen):
        """
        Draws the dynamic text on the screen.

        :param screen: The pygame surface to draw the text on.
        """
        # Get the current text from the function
        current_text = self.get_text_func()

        # Render the text
        text_surface = self.font.render(current_text, True, self.color)

        # Blit the text surface onto the screen at the specified position
        screen.blit(text_surface, self.position)