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


def make_vector2(x, y):
    """ Create a dictionary with 'x' and 'y' entries.

    :param x: (int) x component of the vector.
    :param y: (int) y component of the vector.
    :return: A dictionary with 'x' and 'y' entries.
    """

    return dict(x=x, y=y)


def make_rect(x, y, w, h, color=Color.black()):
    """ Create a dictionary with the necessary information to draw a rect with pygame.

    :param x: X position of the rect.
    :param y: Y position of the rect.
    :param w: Width of the rect.
    :param h: Height of the rect.
    :param color: Color of the rect.
    :return: A dictionary with 'x', 'y', 'width', 'height' and 'color' entries.
    """

    return dict(x=x, y=y, width=w, height=h, color=color)


def make_circle(x, y, r, color=Color.black()):
    """ Create a dictionary with the necessary information to draw a circle with pygame.

    :param x: X position of the circle.
    :param y: Y position of the circle.
    :param r: Radius of the circle.
    :param color: Color of the circle.
    :return: A dictionary with 'x', 'y', 'radius' and 'color' entries.
    """

    return dict(x=x, y=y, radius=r, color=color)


def draw_rect(o):
    """ Draw a rect on screen.

    Uses the given dictionary to draw a rect with pygame.

    :param o: A dictionary with 'x', 'y', 'width', 'height' and 'color' entries.
    """

    pygame.draw.rect(screen, o['color'], (int(o['x']), int(o['y']), int(o['width']), int(o['height'])))


def draw_circle(o):
    """ Draw a circle on screen.

    Uses the given dictionary to draw a rect with pygame.

    :param o: A dictionary with 'x', 'y', 'radius' and 'color' entries.
    """

    pygame.draw.circle(screen, o['color'], (int(o['x']), int(o['y'])), int(o['radius']))


def rect_circle_are_touching(r, c):
    """ Test if a rect and circle are touching.

    :param r: Dictionary with rect values.
    :param c: Dictionary with circle values.
    :return: A boolean value whether or not the rect and circle are touching and a vector2 dictionary representing
    the normal of the collision.
    """

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
    """ Subtract two vector dictionaries.

    :param v1: (dict) Base vector.
    :param v2: (dict) Subtract vector.
    :return: A new vector dictionary of the subtracted vectors.
    """

    return make_vector2(v1['x']-v2['x'], v1['y']-v2['y'])


def vector2_add(v1, v2):
    """ Add two vector dictionaries.

    :param v1: (dict) Base vector.
    :param v2: (dict) Add vector.
    :return: A new vector dictionary of the added vectors.
    """

    return make_vector2(v1['x']+v2['x'], v1['y']+v2['y'])


def vector2_magnitude(v):
    """ Calculate the magnitude of the vector dictionary.

    :param v: (dict) Vector dictionary.
    :return: (float) The magnitude of the vector.
    """

    return math.sqrt(v['x']*v['x'] + v['y']*v['y'])


def vector2_normalize(v):
    """ Normalize a dictionary vector.

    :param v: (dict) Vector dictionary.
    :return: Normalized vector of the given one.
    """

    magnitude = vector2_magnitude(v)
    if magnitude == 0:
        return make_vector2(0, 0)
    return make_vector2(v['x']/magnitude, v['y']/magnitude)


def hit_test_ball(b):
    """ Check if a rect is hitting a ball.

    :param b: Rect to check for intersection.
    :return: True if ball collides with rect, False otherwise.
    """

    global ball_direction
    hit = rect_circle_are_touching(b, ball)
    if hit[0]:
        ball_direction['x'] += ball_direction['x'] * hit[1]['x'] * 2 * -hit[1]['x']
        ball_direction['y'] += ball_direction['y'] * hit[1]['y'] * 2 * -hit[1]['y']
        ball_direction = vector2_normalize(ball_direction)
        return True
    return False


def damage_hittable_block(b):
    """ Damage a block.

    Determines blocks health by its color. Block health goes red->blue->green. After green block is dead.

    :param b: Block to damage.
    :return: True if block is dead, False otherwise.
    """

    if b['color'] == Color.red():
        b['color'] = Color.blue()
    elif b['color'] == Color.blue():
        b['color'] = Color.green()
    elif b['color'] == Color.green():
        return True
    return False


def render_text(s, x, y, clr=Color.white()):
    """ Render text on screen.

    :param s: (string) The text to draw.
    :param x: (int) Center x of the rendered text.
    :param y: (int) Center y of the rendered text.
    :param clr: (tuple) Color of the rendered text.
    """

    r_text = main_font.render(s, True, clr)
    r_text_rect = r_text.get_rect()
    r_text_rect.centerx = x
    r_text_rect.centery = y
    screen.blit(r_text, r_text_rect)


def generate_blocks():
    """ Generate a list of drawable blocks

    Generates a grid of drawable blocks for the breaker game.

    :return: (list) The generated blocks in dictionary form.
    """

    list = []

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
            list.append(r)

    return list


# Game Setup and Global variables
main_font = pygame.font.SysFont(None, 40)
ball_radius = 10
ball_start_pos = make_vector2(GameWidth/2, GameHeight/2)
paddle_start_pos = make_vector2(GameWidth/2-50, GameHeight-50)
paddle = make_rect(paddle_start_pos['x'], paddle_start_pos['y'], 100, 25, Color.red())
ball = make_circle(ball_start_pos['x'], ball_start_pos['y'], ball_radius, Color.blue())

paddle_speed = 200.0
paddle_direction = 0
ball_direction = make_vector2(0, 0)
ball_speed = 200.0

left_down = False
right_down = False

input_timer = float(0)
previous_time = 0
delta_time = float(0)

# Bounds
top_rect = make_rect(0, 0, GameWidth, 30)
left_rect = make_rect(0, 0, 30, GameHeight)
right_rect = make_rect(GameWidth - 30, 0, 30, GameHeight)

bound_rects = [top_rect, left_rect, right_rect]

ball_count = 3

hittable_list = generate_blocks()

round_time = 0.0

# Game Loop
while True:
    delta_time = (pygame.time.get_ticks() - previous_time) / float(1000)
    previous_time = pygame.time.get_ticks()

    screen.fill(Color.white())

    if not (ball_count <= 0 or len(hittable_list) == 0):
        round_time += delta_time

    draw_rect(paddle)
    draw_circle(ball)

    for h in hittable_list:
        draw_rect(h)

    for b in bound_rects:
        draw_rect(b)

    # Round time calculations and UI
    seconds = int(round_time)
    min = seconds/60
    seconds %= 60
    seconds_str = str(seconds)
    if seconds < 10:
        seconds_str = '0' + seconds_str
    render_text(str(min) + ':' + seconds_str, GameWidth - 100, 18, Color.white())

    # Remaining balls UI
    ball_ui_x = 45
    ball_ui_y = 15
    ball_diameter = ball_radius * 2
    for b in range(ball_count):
        pygame.draw.circle(screen, Color.white(), (ball_ui_x + b * (ball_diameter + 7), ball_ui_y), ball_radius+2)
        pygame.draw.circle(screen, Color.blue(), (ball_ui_x + b * (ball_diameter + 7), ball_ui_y), ball_radius)

    # Game Over UI
    if ball_count <= 0:
        render_text("Game Over", GameWidth/2, GameHeight/2, Color.black())
        render_text("Press 'r' to restart", GameWidth/2, GameHeight/2 + 50, Color.black())

    # Victory UI
    if len(hittable_list) == 0:
        render_text("You Won!", GameWidth/2, GameHeight/2, Color.black())
        render_text("Press 'r' to restart", GameWidth/2, GameHeight/2 + 50, Color.black())

    # Instruction UI
    if ball_direction['x'] == 0 and ball_direction['y'] == 0:
        render_text("Press 'space' to launch the ball", GameWidth/2, GameHeight/2 + 50, Color.black())

    new_paddle_x = paddle['x'] + paddle_direction * delta_time * paddle_speed
    if 30 < new_paddle_x and new_paddle_x + paddle['width'] < GameWidth-30:
        paddle['x'] = new_paddle_x

    # Move Ball
    ball['x'] += ball_direction['x'] * delta_time * ball_speed
    ball['y'] += ball_direction['y'] * delta_time * ball_speed

    # Check if ball is of screen
    if ball['y'] >= GameHeight or ball['y'] < 0 or ball['x'] > GameWidth or ball['x'] < 0:
        ball_count -= 1
        if ball_count > 0:
            ball['x'] = ball_start_pos['x']
            ball['y'] = ball_start_pos['y']
            ball_direction = make_vector2(0, 0)

    # Check for ball collision with walls
    for b in bound_rects:
        hit_test_ball(b)

    # Check for ball collision with block
    # Damage block and delete after three hits
    delete_list = []
    for h in hittable_list:
        if hit_test_ball(h) and damage_hittable_block(h):
            delete_list.append(h)

    for d in delete_list:
        hittable_list.remove(d)

    # Check for ball collision with paddle
    if hit_test_ball(paddle):
        ball_direction['x'] += paddle_direction
        ball_direction = vector2_normalize(ball_direction)
        ball['x'] += ball_direction['x'] * delta_time * ball_speed
        ball['y'] += ball_direction['y'] * delta_time * ball_speed

    # Event Check
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Move paddle right
                paddle_direction = 1
                right_down = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Move paddle left
                paddle_direction = -1
                left_down = True
        elif event.type == KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Stop moving paddle right; if left down move left
                paddle_direction = 0 if not left_down else -1
                right_down = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Stop moving paddle left; if right down move right
                paddle_direction = 0 if not right_down else 1
                left_down = False
            elif event.key == pygame.K_SPACE and ball_direction['x'] == 0 and ball_direction['y'] == 0:
                # Launch ball
                ball_direction['y'] = 1
            elif event.key == pygame.K_r:  # and (ball_count <= 0 or len(hittable_list) == 0):
                # Reset all game values
                ball_count = 3
                ball['x'] = ball_start_pos['x']
                ball['y'] = ball_start_pos['y']
                ball_direction = make_vector2(0, 0)
                paddle['x'] = paddle_start_pos['x']
                paddle['y'] = paddle_start_pos['y']
                hittable_list = generate_blocks()
                round_time = 0

    pygame.display.update()
    clock.tick(FPS)
