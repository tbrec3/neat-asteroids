import os
import pygame
import random

from classes.ship import Ship
from classes.bullet import Bullet
from classes.asteroid import Asteroid, spawn_asteroid

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

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # (x, y)
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

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
                spawn_asteroid(asteroids, ASTEROID_ROT_VEL, ASTEROID_VEL)
                asteroid_spawn_delay = random.randrange(100, 200, 2)
                asteroid_spawn_delay_count = 0

            # Offscreen Removal
            for bullet in bullets[:]:
                if bullet.is_offscreen():
                    bullets.remove(bullet)

            for asteroid in asteroids[:]:
                if asteroid.is_offscreen():
                    asteroids.remove(asteroid)

            # Collision Detection
            for asteroid in asteroids[:]:
                for bullet in bullets[:]:
                    if collide(bullet, asteroid):
                        bullets.remove(bullet)
                        if asteroid.rank == 3:
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 2, ASTEROID_ROT_VEL, ASTEROID_VEL))
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 2, ASTEROID_ROT_VEL, ASTEROID_VEL))
                            score += 50
                        if asteroid.rank == 2:
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 1, ASTEROID_ROT_VEL, ASTEROID_VEL))
                            asteroids.append(
                                Asteroid(asteroid.x, asteroid.y, 1, ASTEROID_ROT_VEL, ASTEROID_VEL))
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
                    bullets.append(Bullet(ship, BULLET_VEL))
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
