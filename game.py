import os
import pygame
import random

from numpy import arccos, arctan, cos, sin, radians, sqrt, square, degrees
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_SPACE

pygame.font.init()

WIN_HEIGHT, WIN_WIDTH = 700, 700
WIN = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Directions
UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)

# Parameters
PUSH_RATE = 0.05
PLAYER_MAX_VEL = 4
ASTEROID_VEL = 2
ASTEROID_ROT_VEL = 2
BULLET_VEL = 5

# Assets
LOGO = pygame.image.load(os.path.join("assets", "icon.png"))
ASTEROID_IMG1 = pygame.image.load(os.path.join("assets", "Asteroid_1.png"))
ASTEROID_IMG2 = pygame.image.load(os.path.join("assets", "Asteroid_2.png"))
ASTEROID_IMG3 = pygame.image.load(os.path.join("assets", "Asteroid_3.png"))


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

        # Setting bounds
        if self.x < -30:
            self.x = WIN_HEIGHT
        if self.x > WIN_HEIGHT:
            self.x = -30
        if self.y < -30:
            self.y = WIN_WIDTH
        if self.y > WIN_WIDTH:
            self.y = -30

    def push(self, rate):
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
        if self.vel >= PLAYER_MAX_VEL:
            self.vel = PLAYER_MAX_VEL

    def tilt_right(self, turn_rate):
        self.rot = (self.rot + turn_rate) % 360


class Bullet:
    def __init__(self, ship: Ship) -> None:
        self.x = ship.x + ship.surface.get_rect().centerx
        self.y = ship.y + ship.surface.get_rect().centery
        self.dir = ship.rot
        self.vel = BULLET_VEL

        self.surface = pygame.Surface((2, 2))
        self.surface.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, win):
        win.blit(self.surface, (self.x, self.y))

    def move(self):
        self.x += cos(radians(self.dir)) * self.vel
        self.y -= sin(radians(self.dir)) * self.vel

    def is_offscreen(self) -> bool:
        return self.x < 0 or self.x > WIN_WIDTH or self.y < 0 or self.y > WIN_HEIGHT


class Asteroid:
    def __init__(self, x, y, rank) -> None:
        self.rank = rank
        self.x = x
        self.y = y
        self.rot = 0
        self.rot_vel = ASTEROID_ROT_VEL * (random.random()-0.5)
        self.move_vel = ASTEROID_VEL * (random.random() + 0.1)

        # Calculate Direction to Middle of Screen
        x_offset = (WIN_WIDTH // 2) - self.x
        y_offset = (WIN_HEIGHT // 2) - self.y
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
        if ((-150) < self.x < WIN_WIDTH+150) and ((-150) < self.y < WIN_HEIGHT+150):
            return False
        else:
            return True


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # (x, y)
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None


def spawn_asteroid(asteroids: list):
    rand_x = random.randrange(-100, WIN_WIDTH + 30)

    if 0 < rand_x < WIN_WIDTH:
        rand_y = random.randrange(-100, WIN_HEIGHT + 30, WIN_HEIGHT + 129)
    else:
        rand_y = random.randrange(-100, WIN_HEIGHT + 30)

    asteroids.append(
        Asteroid(rand_x, rand_y, random.choice([1, 1, 1, 2, 2, 3])))

def main():
    pygame.display.init()
    pygame.display.set_icon(LOGO)
    pygame.display.set_caption("Asteroids")

    fps = 60

    # Fonts
    font = pygame.font.SysFont("comicsans", 50)
    big_font = pygame.font.SysFont("comicsans", 70)

    # Objects
    ship = Ship(350, 350)
    bullets = []
    asteroids = []

    score = 0

    def draw_window(win):
        # Scene
        win.fill(BLACK)
        for asteroid in asteroids:
            asteroid.draw(win)
        for bullet in bullets:
            bullet.draw(win)
        ship.draw(win)

        # Healthbar
        rect_width = (WIN_WIDTH - 20) * ship.health / 100
        pygame.draw.rect(win, (255, 255, 255), (10, 10, rect_width, 10))

        # Score
        score_label = font.render(f"Score: {score}", 1, WHITE)
        win.blit(score_label, (10, 20))

        if len(bullets) != 0:
            win.blit(bullets[0].mask.to_surface(), (10, 50))

        pygame.display.flip()

    def game_over(win):
        win.fill(BLACK)
        game_over_label = big_font.render("GAME OVER", 1, RED)
        win.blit(game_over_label, (WIN_WIDTH//2 - game_over_label.get_width()//2,
                                   WIN_HEIGHT//2 - game_over_label.get_height()//2))
        pygame.display.flip()

    clock = pygame.time.Clock()
    run = True
    alive = True
    shoot_delay_count = 0
    shoot_enable = False
    asteroid_spawn_delay_count = 0
    asteroid_spawn_delay = 50

    while run:
        clock.tick(fps)

        # Exit Rule
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if alive:
            # Movement for all Objects
            ship.move()
            for asteroid in asteroids:
                asteroid.move()
            for bullet in bullets:
                bullet.move()

            # Counters
            shoot_delay_count += 1
            asteroid_spawn_delay_count += 1

            # Asteroids spawning
            if not asteroid_spawn_delay_count % asteroid_spawn_delay:
                spawn_asteroid(asteroids)
                asteroid_spawn_delay = random.randrange(100, 200, 2)
                asteroid_spawn_delay_count = 0

            # Offscreen Removal
            for bullet in bullets:
                if bullet.is_offscreen():
                    bullets.remove(bullet)

            for asteroid in asteroids:
                if asteroid.is_offscreen():
                    asteroids.remove(asteroid)

            # Collision Detection
            for asteroid in asteroids[:]:
                for bullet in bullets:
                    if collide(bullet, asteroid):
                        bullets.remove(bullet)
                        if asteroid.rank == 3:
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 2))
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 2))
                            score += 50
                        if asteroid.rank == 2:
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 1))
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 1))
                            score += 25
                        if asteroid.rank == 1:
                            score += 10
                        asteroids.remove(asteroid)

                if collide(asteroid, ship):
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)
                    ship.health -= 10

            # Shot Rate
            if not (shoot_delay_count % 30):
                shoot_enable = True

            # Lose Condition
            if ship.health <= 0:
                alive = False

            # Keyboard input
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                ship.push(PUSH_RATE)
            if keys[K_LEFT]:
                ship.tilt_right(5)
            if keys[K_RIGHT]:
                ship.tilt_right(-5)
            if keys[K_SPACE]:
                if shoot_enable == True:
                    bullets.append(Bullet(ship))
                    shoot_enable = False
                    shoot_delay_count = 0
            # if keys[K_DOWN]:
            #     fps = 10
            else:
                fps = 60

            draw_window(WIN)
        else:
            game_over(WIN)


if __name__ == "__main__":
    main()
