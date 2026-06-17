import pygame

class Node:
    def __init__(self, x, y, colour, text):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour

        self.width = 100
        self.height = 50
        self.bonds = []
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)

        self.active = False

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box.topleft = (x, y)

    def set_text(self, text):
        self.text = text