import pygame

from numpy import arccos, cos, sin, radians, sqrt, square, degrees

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ship:
    def __init__(self, x, y):
        # Position and Rotation
        self.x = x
        self.y = y
        self.rot: int = 90
        self.health = 100

        # Move-Vector attributes
        self.vel = 0
        self.move_dir = 0

        # Creating a surface for the ship
        self.surface = pygame.Surface((20, 30))
        self.poly_points = [(0, 30),
                            (10, 0),
                            (20, 30),
                            (10, 20)]
        pygame.draw.polygon(self.surface, WHITE, self.poly_points, 2)

        self.surface.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, win):
        rotated_img = pygame.transform.rotate(self.surface, self.rot-90)
        rotated_img.set_colorkey(BLACK)
        new_rect = rotated_img.get_rect(
            center=self.surface.get_rect(topleft=(self.x, self.y)).center)
        self.mask = pygame.mask.from_surface(rotated_img)
        win.blit(rotated_img, new_rect.topleft)

    def move(self):
        self.x += cos(radians(self.move_dir)) * self.vel
        self.y -= sin(radians(self.move_dir)) * self.vel

        win_height, win_width = pygame.display.get_window_size()
        margin = -30

        # Setting bounds
        if self.x < margin:
            self.x = win_height
        if self.x > win_height:
            self.x = margin
        if self.y < margin:
            self.y = win_width
        if self.y > win_width:
            self.y = margin

    def push(self, rate, max_vel=4):
        # Cartesian Coordinates
        new_x = self.vel*cos(radians(self.move_dir)) + \
            rate*cos(radians(self.rot))
        new_y = self.vel*sin(radians(self.move_dir)) + \
            rate*sin(radians(self.rot))

        # Polar Coordinates
        self.vel = sqrt(square(new_x) + square(new_y))
        self.move_dir = degrees(arccos((new_x / self.vel)))
        if new_y < 0:
            self.move_dir = -self.move_dir

        # Cap Velocity
        if self.vel >= max_vel:
            self.vel = max_vel

    def tilt_right(self, turn_rate):
        self.rot = (self.rot + turn_rate) % 360
