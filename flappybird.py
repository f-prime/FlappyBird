#!/usr/bin/env python
"""FlappyBird game in python."""

import sys
import random

import pygame


QUIT = pygame.QUIT  # pylint: disable=no-member
KEYDOWN = pygame.KEYDOWN  # pylint: disable=no-member
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN  # pylint: disable=no-member


class Config(object):
    """Represents config class."""

    def __init__(self):
        self.gap = 0
        self.wall_x = 0
        self.jump = 0
        self.jump_speed = 0
        self.gravity = 0
        self.dead = None
        self.sprite = 0
        self.offset = 0

    def load(self):
        """Load config. (may change to file or some kind db)."""
        self.gap = 130
        self.wall_x = 400
        self.jump = 17
        self.jump_speed = 10
        self.gravity = 5
        self.sprite = 0


class Bird(object):
    """Bird object"""
    def __init__(self, rectangle, bird_y=0):
        self.rect = rectangle
        self.coord_y = bird_y


class FlappyBirdGame(object):
    """FlappyBird Game class."""

    def __init__(self):
        self.config = Config()
        self.config.load()
        self.jump = self.config.jump
        self.jump_speed = self.config.jump_speed
        self.gravity = self.config.gravity
        self.wall_x = self.config.wall_x
        self.sprite = self.config.sprite
        self._random_offset()

        self.counter = 0
        self.dead = False

        self.screen = pygame.display.set_mode((400, 708))
        self.bird = Bird(pygame.Rect(65, 50, 50, 50), bird_y=350)
        self.background = pygame.image.load("assets/background.png").convert()
        self.bird_sprites = [pygame.image.load("assets/1.png").convert_alpha(),
                             pygame.image.load("assets/2.png").convert_alpha(),
                             pygame.image.load("assets/dead.png")]
        self.wall_up = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wall_down = pygame.image.load("assets/top.png").convert_alpha()

    def _random_offset(self):
        """Change random offset."""
        self.offset = random.randint(-110, 110)

    def _update_walls(self):
        """Move walls from left side to right side."""
        self.wall_x -= 2
        if self.wall_x < -80:
            self.wall_x = self.config.wall_x
            self.counter += 1
            self._random_offset()

    def _update_bird(self):
        """Move bird."""
        if self.jump:
            self.jump_speed -= 1
            self.bird.coord_y -= self.jump_speed
            self.jump -= 1
        else:
            self.bird.coord_y += self.gravity
            self.gravity += 0.2
        self.bird.rect[1] = self.bird.coord_y
        up_rectangle = pygame.Rect(self.wall_x,
                                   self.config.gap - self.offset
                                   + 10 + 360,
                                   self.wall_up.get_width() - 10,
                                   self.wall_up.get_height())
        down_rectangle = pygame.Rect(self.wall_x,
                                     0 - self.config.gap - self.offset
                                     - 10,
                                     self.wall_down.get_width() - 10,
                                     self.wall_down.get_height())
        if up_rectangle.colliderect(self.bird):
            self.dead = True
        if down_rectangle.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird.rect[1] < 720:
            self.bird.rect[1] = 50
            self.bird.coord_y = 50
            self.dead = False
            self.counter = 0
            self.wall_x = self.config.wall_x
            self._random_offset()
            self.gravity = self.config.gravity

    def run_game_instance(self):
        """Main game process."""
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if self.dead:
                    continue
                if event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                    self.jump = self.config.jump
                    self.gravity = 5
                    self.jump_speed = self.config.jump_speed

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wall_up,
                             (self.wall_x, 360 + self.config.gap
                              - self.offset))
            self.screen.blit(self.wall_down,
                             (self.wall_x, 0 - self.config.gap
                              - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.bird_sprites[self.sprite],
                             (70, self.bird.coord_y))
            if not self.dead:
                self.sprite = 0
            self._update_walls()
            self._update_bird()
            pygame.display.update()

    @staticmethod
    def start_game():
        """Start game."""
        game = FlappyBirdGame()
        game.run_game_instance()


if __name__ == "__main__":
    FlappyBirdGame.start_game()
