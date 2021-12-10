import pygame
import random


class Crazy_Plane(pygame.sprite.Sprite):
    # gets a starting point (x,y) and sprite picture
    # plane loc is relative to the grid (0-9)
    def __init__(self, plane_sprite, plane_list):
        super(self.__class__, self).__init__()
        self._x, self._y = 0, 0
        while plane_list.count((self._x, self._y)) > 0 or (
                self._x >= 10) or self._x < 0 or self._y >= 10 or self._y < 0:
            self._x = random.randint(0, 10)
            self._y = random.randint(0, 10)
        self.plane_sprite = pygame.image.load(plane_sprite).convert()
        self.plane_sprite.set_colorkey((69, 69, 69))

    # return current loc of plane relative to screen
    def get_loc(self):
        return self._x * 150, self._y * 100

    # gets x, y
    # updates plan loc
    def update_loc(self, x, y):
        self._x = x
        self._y = y

    # randomizes x and y movement
    # updates loc accordingly
    def move(self):
        x_plus, y_plus = 0, 0
        while (x_plus == 0 and y_plus == 0) or (self._x <= 0 and x_plus == -1) or (self._y <= 0 and y_plus == -1) or (
                self._x >= 9 and x_plus == 1) or (self._y >= 9 and y_plus == 1):  # if plane tries to stay in place
            #                                                                     # or move out of bounds
            x_plus, y_plus = random.randint(-1, 1), random.randint(-1, 1)         # randomize movement

        # update loc
        self._x += x_plus
        self._y += y_plus
