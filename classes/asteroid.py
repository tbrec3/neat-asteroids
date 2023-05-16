import os
import pygame
import random
from numpy import arctan, cos, sin

ASTEROID_IMG1 = pygame.image.load(os.path.join("assets", "Asteroid_1.png"))
ASTEROID_IMG2 = pygame.image.load(os.path.join("assets", "Asteroid_2.png"))
ASTEROID_IMG3 = pygame.image.load(os.path.join("assets", "Asteroid_3.png"))

class Asteroid:
    def __init__(self, x, y, rank, rot_vel, move_vel) -> None:
        self.rank = rank
        self.x = x
        self.y = y
        self.rot = 0
        self.rot_vel = rot_vel * (random.random()-0.5)
        self.move_vel = move_vel * (random.random() + 0.1)

        # Calculate Direction to Middle of Screen
        win_width, win_height = pygame.display.get_window_size()
        x_offset = (win_width  // 2) - self.x
        y_offset = (win_height // 2) - self.y
        if x_offset != 0:
            self.move_dir = -arctan(y_offset / x_offset) + \
                (random.random()-0.5)*1.5
        else:
            self.move_dir = 0

        if rank == 1:
            self.img = ASTEROID_IMG1
        elif rank == 2:
            self.img = ASTEROID_IMG2
        elif rank == 3:
            self.img = ASTEROID_IMG3

        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        rotated_img = pygame.transform.rotate(self.img, self.rot)
        new_rect = rotated_img.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        self.mask = pygame.mask.from_surface(rotated_img)
        win.blit(rotated_img, new_rect.topleft)

    def move(self):
        self.x += cos(self.move_dir) * self.move_vel
        self.y -= sin(self.move_dir) * self.move_vel

        self.rot += self.rot_vel

    def is_offscreen(self) -> bool:
        win_width, win_height = pygame.display.get_window_size()
        if ((-150) < self.x < win_width + 150) and ((-150) < self.y < win_height + 150):
            return False
        else:
            return True

def spawn_asteroid(asteroids: list, rot_vel, move_vel):
    win_width, win_height = pygame.display.get_window_size()
    rand_x = random.randrange(-100, win_width + 30)

    if 0 < rand_x < win_width:
        rand_y = random.randrange(-100, win_height + 30, win_height + 129)
    else:
        rand_y = random.randrange(-100, win_height + 30)

    asteroids.append(
        Asteroid(rand_x, rand_y, random.choice([1, 1, 1, 2, 2, 3]), rot_vel, move_vel))