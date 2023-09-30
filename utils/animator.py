#!/usr/bin/env python3
import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from utils import scaler
import math

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)

MIN_X = -120
MAX_X = 120

MIN_Y = -120
MAX_Y = 120

MIN_R = 0
MAX_R = 120

FONT_SIZE = 15
COLOR_CENTER = (127, 255, 212, 128)

RADIUS_CAR_CIRCLE_px = 2  # Toyota corolla
RADIUS_OBJ_CIRCLE_px = 1  # We assume this size of an object
ALARM_DIST = RADIUS_CAR_CIRCLE_px * 5


def play(normalized_data, frames_per_second, objects, object_colors):
    object_colors_mappings = {o:c for c, o in zip(object_colors, objects)}
    def scale_x(x):
        return scaler.scale_linearly(given_value=x, right_lim=[MIN_X, MAX_X], left_lim=[0, WIDTH])

    def scale_y(y):
        return scaler.scale_linearly(given_value=y, right_lim=[MIN_Y, MAX_Y], left_lim=[0, HEIGHT])

    def scale_r(r):
        return scaler.scale_linearly(given_value=r, right_lim=[0, MAX_R], left_lim=[0, HEIGHT])
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Pirates Animation")

    # Object properties
    clock = pygame.time.Clock()

    for idx, _ in enumerate(normalized_data[0]['pts']):
        for event in pygame.event.get():
            if event.type == 771:
                import time
                time.sleep(1)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        for data in normalized_data:
            ##
            # Color
            ##
            color = object_colors_mappings[data['name']]

            ##
            # Circles
            ##
            point = data['pts'][idx]
            object_x = scale_x(point['x'])
            object_y = scale_y(point['y'])
            pygame.draw.circle(screen, COLOR_CENTER, (scale_x(
                0), scale_y(0)), scale_r(RADIUS_CAR_CIRCLE_px))
            pygame.draw.circle(
                screen, color, (object_x, object_y), scale_r(RADIUS_OBJ_CIRCLE_px))

            ##
            # Legend
            ##
            rect_top = 120
            rect_top_fac = 50
            rect_x = 0
            text_x_1 = 60
            text_x_2 = 120
            text_x_3 = 250
            text_y_2_base = 80
            text_y_2_fac = 50
            text_y_3_base = 100
            text_y_3_fac = 50

            ##
            # General
            ##
            def create_text(text, coords, color=None):
                if color is None:
                    color = (0, 0, 0)
                font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
                text = font.render(text, True, color, (255, 255, 255))
                textRect = text.get_rect()
                textRect.x = coords[0]
                textRect.y = coords[1]
                screen.blit(text, textRect)
            create_text(f"timestamp={point['t']:.5} [s]", (text_x_1, 100))
            create_text(f"v_car={point['v']:.5} [m/s]",
                        (text_x_2, text_y_2_base+text_y_2_fac*1))
            create_text(f"yaw={point['yaw_rate']:.5}",
                        (text_x_2, text_y_2_base+text_y_2_fac*1+20))

            ##
            # Legend
            ##
            def draw_legend_item(rect_idx, rect_name, rect_color):
                pygame.draw.rect(screen, rect_color,
                                 pygame.Rect(rect_x, rect_top+rect_top_fac*rect_idx, rect_top_fac, rect_top_fac))
                create_text(rect_name, (text_x_1, text_y_2_base +
                            text_y_2_fac*(rect_idx + 1)))
                if data['name'] == rect_name:
                    text_color = (0, 0, 0)
                    dist = _calc_dist(0, 0, point['x'], point['y'])

                    if scale_r(dist) <= scale_r(ALARM_DIST) * 1.5 + scale_r(RADIUS_OBJ_CIRCLE_px) * 1.5:
                        text_color = (255, 0, 0)
                        create_text(f'TOO CLOSE!',
                                    (text_x_3, text_y_2_base +
                                     text_y_2_fac*(rect_idx + 1)),
                                    text_color)
                        if int(os.getenv('SOUND_ON', 0)) == 1:
                            _sound_the_horn()

                    # Radius
                    pygame.draw.circle(screen, COLOR_CENTER,
                                       (scale_x(0), scale_y(0)),
                                       scale_r(ALARM_DIST), width=1)

                    create_text(f'v={_calc_magnitude(point["vx"], point["vy"]):.5} [m/s]',
                                (text_x_2, text_y_2_base +
                                 text_y_2_fac*(rect_idx + 1)),
                                text_color)
                    create_text(f'd={dist:.5} [m]',
                                (text_x_2, text_y_3_base +
                                 text_y_3_fac*(rect_idx + 1)),
                                text_color)

            draw_legend_item(0, 'Our car', COLOR_CENTER)
            draw_legend_item(1, '1st', object_colors_mappings['1st'])
            draw_legend_item(2, '2nd', object_colors_mappings['2nd'])
            draw_legend_item(3, '3rd', object_colors_mappings['3rd'])
            draw_legend_item(4, '4th', object_colors_mappings['4th'])

        pygame.display.flip()
        clock.tick(frames_per_second)


def _calc_magnitude(left, right):
    return math.sqrt(left**2 + right**2)


def _calc_dist(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)


def _sound_the_horn():
    horn_sound = pygame.mixer.Sound("media/horn.wav")
    horn_sound.play()


def generate_colors(num_colors):
    r = _get_random_num(0, 255)
    g = _get_random_num(0, 255)
    b = _get_random_num(0, 255)
    return [(r, g, b) for _ in range(num_colors)]

def _get_random_num(start, end):
    return random.randint(start, end)