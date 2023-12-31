#!/usr/bin/env python3
import math
from utils import scaler
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

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
COLOR_CENTER = (128, 128, 128, 128)
COLOR_TRIANGLE = (207, 181, 122, 128)

RADIUS_CAR_CIRCLE_m = 2  # Toyota corolla
RADIUS_OBJ_CIRCLE_m = 1  # We assume this size of an object
ALARM_DIST = RADIUS_CAR_CIRCLE_m * 5

BIG_STATE = {'TRIANGLE_CIRCLES': [
    (11, -6, {'status': 'ok', 'offender': ''}),
    (8, -6, {'status': 'ok', 'offender': ''}),
    (11, -3, {'status': 'ok', 'offender': ''}),
    (8, -3, {'status': 'ok', 'offender': ''}),
    (5, -3, {'status': 'ok', 'offender': ''}),
    (11, 0, {'status': 'ok', 'offender': ''}),
    (8, 0, {'status': 'ok', 'offender': ''}),
    (5, 0, {'status': 'ok', 'offender': ''}),
    (11, 3, {'status': 'ok', 'offender': ''}),
    (8, 3, {'status': 'ok', 'offender': ''}),
    (5, 3, {'status': 'ok', 'offender': ''}),
    (11, 6, {'status': 'ok', 'offender': ''}),
    (8, 6, {'status': 'ok', 'offender': ''}),
]}


def play(normalized_data, frames_per_second, object_names, object_colors):
    object_colors_mappings = {o: c for c,
                              o in zip(object_colors, object_names)}

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
                0), scale_y(0)), scale_r(RADIUS_CAR_CIRCLE_m))
            pygame.draw.circle(
                screen, color, (object_x, object_y), scale_r(RADIUS_OBJ_CIRCLE_m))

            ##
            # Legend
            ##
            rect_top = 120
            rect_top_fac = 50
            rect_x = 0
            text_x_1 = 60
            text_x_2 = 120
            text_x_25 = 250
            text_x_3 = 700
            text_x_4 = 750
            text_y_1_base = 40
            text_y_1_fac = 30
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

                    create_text(f'v={_calc_magnitude(point["vx"], point["vy"]):.5} [m/s]',
                                (text_x_2, text_y_2_base +
                                 text_y_2_fac*(rect_idx + 1)),
                                text_color)
                    create_text(f'd={dist:.5} [m]',
                                (text_x_2, text_y_3_base +
                                 text_y_3_fac*(rect_idx + 1)),
                                text_color)

                    matches = [tc for tc in BIG_STATE["TRIANGLE_CIRCLES"] if tc[2]['offender'] == rect_name]
                    num_reds = len(matches)
                    if num_reds >= 5:
                        text_color = (255, 0, 0)
                        create_text(f'Decelerating because of {rect_name}!',
                                    (text_x_25, text_y_1_base),
                                    (255, 0, 0))
                    create_text(f'reds={num_reds}/{len(BIG_STATE["TRIANGLE_CIRCLES"])}',
                                (text_x_25, text_y_3_base +
                                    text_y_3_fac*(rect_idx + 1)),
                                text_color)

            ##
            # Triangle circles at the front of the camera
            ##
            RADIUS_TRIANGLE_CIRCLE_m = 1
            def draw_triangle_circle(rect_idx, x, y):
                triangle_circle_color = COLOR_TRIANGLE
                dist = _calc_dist(x, y, point['x'], point['y'])

                text_color = (0, 0, 0)
                if dist <= RADIUS_TRIANGLE_CIRCLE_m * 1.5 + RADIUS_OBJ_CIRCLE_m * 1.5:
                    triangle_circle_color = (255, 0, 0, 128)

                    text_color = (255, 0, 0)
                    create_text(f'!',
                                (text_x_4, text_y_1_base +
                                    text_y_1_fac*(rect_idx + 1)),
                                text_color)

                    if int(os.getenv('SOUND_ON', 0)) == 1:
                        _sound_the_horn()

                    create_text(f'slot #{rect_idx}', (text_x_3, text_y_1_base +
                                text_y_1_fac*(rect_idx + 1)), text_color)


                    # Find corresponding triangle circle item and update status
                    triangle_circles_new = []
                    for tc in BIG_STATE['TRIANGLE_CIRCLES']:
                        if tc[1] == y and tc[0] == x:
                            tc[2]['status'] = 'red'
                            tc[2]['offender'] = data['name']
                        triangle_circles_new.append(tc)
                    BIG_STATE['TRIANGLE_CIRCLES'] = triangle_circles_new

                center = (scale_x(x + 0.1), scale_y(y))
                radius = scale_r(RADIUS_TRIANGLE_CIRCLE_m)
                _draw_circle_alpha(screen, triangle_circle_color, center, radius)

            _iterate_lights(draw_triangle_circle)

            draw_legend_item(0, 'Our car', COLOR_CENTER)
            _iterate_legend(draw_legend_item, object_names,
                           object_colors_mappings)

        pygame.display.flip()
        clock.tick(frames_per_second)


def _draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def _iterate_lights(draw_triangle_circle):
    for idx, triangle_circle in enumerate(BIG_STATE['TRIANGLE_CIRCLES']):
        x = triangle_circle[0]
        y = triangle_circle[1]
        draw_triangle_circle(idx + 1, x, y)


def _iterate_legend(func, object_names, object_colors_mappings):
    for idx, obj_name in enumerate(object_names):
        func(idx + 1, obj_name, object_colors_mappings[obj_name])


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
