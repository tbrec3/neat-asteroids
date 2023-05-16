import pygame
from numpy import cos, sin, radians
from .ship import Ship

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Bullet:
    def __init__(self, ship: Ship, vel) -> None:
        self.x = ship.x + ship.surface.get_rect().centerx
        self.y = ship.y + ship.surface.get_rect().centery
        self.dir = ship.rot
        self.vel = vel

        self.surface = pygame.Surface((2, 2))
        self.surface.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, win):
        win.blit(self.surface, (self.x, self.y))

    def move(self):
        self.x += cos(radians(self.dir)) * self.vel
        self.y -= sin(radians(self.dir)) * self.vel

    def is_offscreen(self) -> bool:
        # Get window size for boundaries
        win_width, win_height = pygame.display.get_window_size()

        return self.x < 0 or self.x > win_width or self.y < 0 or self.y > win_height

