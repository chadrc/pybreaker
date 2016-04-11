import sys
import pygame
from pygame.locals import *

__author__ = 'Chad Collins'

pygame.init()

FPS = 30
clock = pygame.time.Clock()

GameWidth = 800
GameHeight = 600

screen = pygame.display.set_mode((GameWidth, GameHeight))
pygame.display.set_caption('Python - A snake game')


class Color(object):
    @staticmethod
    def black():
        return 0, 0, 0

    @staticmethod
    def white():
        return 255, 255, 255

    @staticmethod
    def red():
        return 255, 0, 0

    @staticmethod
    def green():
        return 0, 255, 0

    @staticmethod
    def blue():
        return 0, 0, 255


def make_vector2(x, y, d=None):
    o = d
    if d is None:
        o = dict(x=x, y=y)
    else:
        o['x'] = x
        o['y'] = y
    return o


def make_rect(x, y, w, h, d=None):
    if d is None:
        o = dict(x=x, y=y, width=w, height=h)
    else:
        o = d
        o['x'] = x
        o['y'] = y
        o['width'] = w
        o['height'] = h
    return o


def make_circle(x, y, r, d=None):
    if d is None:
        o = dict(x=x, y=y, radius=r)
    else:
        o = d
        o['x'] = x
        o['y'] = y
        o['radius'] = r
    return o


def draw_rect(o):
    pygame.draw.rect(screen, Color.red(), (int(o['x']), int(o['y']), int(o['width']), int(o['height'])))


def draw_circle(o):
    pygame.draw.circle(screen, Color.blue(), (int(o['x']), int(o['y'])), int(o['radius']))


paddle = make_rect(GameWidth/2-50, GameHeight-50, 100, 25)
ball = make_circle(GameWidth/2, GameHeight/2, 10)

ball_direction = make_vector2(0, 1)
ball_speed = 50.0

input_timer = float(0)
previous_time = 0
delta_time = float(0)
frame_count = 0

# Game Loop
while True:
    frame_count += 1
    delta_time = (pygame.time.get_ticks() - previous_time) / float(1000)
    previous_time = pygame.time.get_ticks()

    screen.fill(Color.white())

    draw_rect(paddle)
    draw_circle(ball)

    ball['x'] += ball_direction['x'] * delta_time * ball_speed
    ball['y'] += ball_direction['y'] * delta_time * ball_speed

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)
