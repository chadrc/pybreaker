import sys
import math
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


def make_rect(x, y, w, h, color=Color.black(), d=None):
    if d is None:
        o = dict(x=x, y=y, width=w, height=h, color=color)
    else:
        o = d
        o['x'] = x
        o['y'] = y
        o['width'] = w
        o['height'] = h
        o['color'] = color
    return o


def make_circle(x, y, r, color=Color.black(), d=None):
    if d is None:
        o = dict(x=x, y=y, radius=r, color=color)
    else:
        o = d
        o['x'] = x
        o['y'] = y
        o['radius'] = r
        o['color'] = color
    return o


def draw_rect(o):
    pygame.draw.rect(screen, o['color'], (int(o['x']), int(o['y']), int(o['width']), int(o['height'])))


def draw_circle(o):
    pygame.draw.circle(screen, o['color'], (int(o['x']), int(o['y'])), int(o['radius']))


def rect_circle_are_touching(r, c):
    if c['x'] + c['radius'] > r['x'] and c['y'] + c['radius'] > r['y'] \
            and c['x'] - c['radius'] < r['x'] + r['width'] and c['y'] - c['radius'] < r['y'] + r['height']:
        if c['x'] < r['x']:
            normal = make_vector2(-1, 0)
        elif c['x'] > r['x'] + r['width']:
            normal = make_vector2(1, 0)
        elif c['y'] < r['y']:
            normal = make_vector2(0, -1)
        elif c['y'] > r['y'] + r['height']:
            normal = make_vector2(0, 1)
        else:
            normal = make_vector2(0, 0)
        return True, normal
    return False, None


def vector2_difference(v1, v2):
    return make_vector2(v1['x']-v2['x'], v1['y']-v2['y'])


def vector2_add(v1, v2):
    return make_vector2(v1['x']+v2['x'], v1['y']+v2['y'])


def vector2_magnitude(v):
    return math.sqrt(v['x']*v['x'] + v['y']*v['y'])


def vector2_normalize(v):
    magnitude = vector2_magnitude(v)
    if magnitude == 0:
        return make_vector2(0, 0)
    return make_vector2(v['x']/magnitude, v['y']/magnitude)


def hit_test_ball(b):
    global ball_direction
    hit = rect_circle_are_touching(b, ball)
    if hit[0]:
        ball_direction['x'] += ball_direction['x'] * hit[1]['x'] * 2 * -hit[1]['x']
        ball_direction['y'] += ball_direction['y'] * hit[1]['y'] * 2 * -hit[1]['y']
        ball_direction = vector2_normalize(ball_direction)
        return True
    return False


paddle = make_rect(GameWidth/2-50, GameHeight-50, 100, 25, Color.red())
ball = make_circle(GameWidth/2, GameHeight/2, 10, Color.blue())

paddle_speed = 200.0
paddle_direction = 0
ball_direction = make_vector2(0, 1)
ball_speed = 200.0

left_down = False
right_down = False

input_timer = float(0)
previous_time = 0
delta_time = float(0)
frame_count = 0

# Bounds
top_rect = make_rect(0, 0, GameWidth, 10)
left_rect = make_rect(0, 0, 10, GameHeight)
right_rect = make_rect(GameWidth - 10, 0, 10, GameHeight)

bound_rects = [top_rect, left_rect, right_rect]

hittable_list = []

hittable_columns = 5
hittable_rows = 5
hittable_width = 75
hittable_height = 25
hittable_margin = 10

start_y = 100
start_x = GameWidth/2 - (hittable_columns * (hittable_width + hittable_margin))/2

for i in range(hittable_columns):
    for j in range(hittable_rows):
        r = make_rect(start_x + i * (hittable_width + hittable_margin),
                      start_y + j * (hittable_height + hittable_margin),
                      hittable_width,
                      hittable_height,
                      Color.red())
        hittable_list.append(r)

# Game Loop
while True:
    frame_count += 1
    delta_time = (pygame.time.get_ticks() - previous_time) / float(1000)
    previous_time = pygame.time.get_ticks()

    screen.fill(Color.white())

    draw_rect(paddle)
    draw_circle(ball)

    for h in hittable_list:
        draw_rect(h)

    for b in bound_rects:
        draw_rect(b)

    paddle['x'] += paddle_direction * delta_time * paddle_speed

    ball['x'] += ball_direction['x'] * delta_time * ball_speed
    ball['y'] += ball_direction['y'] * delta_time * ball_speed

    for b in bound_rects:
        hit_test_ball(b)

    delete_list = []
    for h in hittable_list:
        if hit_test_ball(h):
            delete_list.append(h)

    for d in delete_list:
        hittable_list.remove(d)

    if hit_test_ball(paddle):
        ball_direction['x'] += paddle_direction
        ball_direction = vector2_normalize(ball_direction)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                paddle_direction = 1
                right_down = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                paddle_direction = -1
                left_down = True
        elif event.type == KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                paddle_direction = 0 if not left_down else -1
                right_down = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                paddle_direction = 0 if not right_down else 1
                left_down = False

    pygame.display.update()
    clock.tick(FPS)
