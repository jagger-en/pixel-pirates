#!/usr/bin/env python3
import pygame
import sys
import time
import json
from utils import pixelize
import math

WIDTH = 800
HEIGHT = 600
FPS = 10

WHITE = (255, 255, 255)
GREEN = (50, 200, 50)


MIN_X = -120
MAX_X = 120

MIN_Y = -120
MAX_Y = 120

FONT_SIZE = 15
COLOR_CENTER = (0, 0, 0)
COLOR_1ST = (1, 168, 255)
COLOR_2ND = (9, 230, 71)
COLOR_3RD = (230, 144, 9)
COLOR_4TH = (254, 24, 10)


def calc_magnitude(left, right):
    return math.sqrt(left**2 + right**2)

def play(normalized_data):
    def scale_x(x):
        return pixelize.scale(given_value=x, right_lim=[MIN_X, MAX_X], left_lim=[0, WIDTH])

    def scale_y(y):
        return pixelize.scale(given_value=y, right_lim=[MIN_Y, MAX_Y], left_lim=[0, HEIGHT])
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualization")

    # Object properties
    clock = pygame.time.Clock()

    for idx, _ in enumerate(normalized_data[0]['pts']):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        for data in normalized_data:
            ##
            # Color
            ##
            if data['name'] == '1st':
                color = COLOR_1ST
            if data['name'] == '2nd':
                color = COLOR_2ND
            if data['name'] == '3rd':
                color = COLOR_3RD
            if data['name'] == '4th':
                color = COLOR_4TH

            ##
            # Circles
            ##
            point = data['pts'][idx]
            object_x = scale_x(point['x'])
            object_y = scale_y(point['y'])
            pygame.draw.circle(screen, COLOR_CENTER,
                               (scale_x(0), scale_y(0)), 20)
            pygame.draw.circle(screen, color, (object_x, object_y), 12)

            ##
            # Legend
            ##
            rect_top = 120
            rect_top_fac = 50
            text_x_1 = 110
            text_x_2 = 200
            text_y_2_base = 80
            text_y_2_fac = 50

            ##
            # General
            ##
            def create_text(text, coords):
                font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
                text = font.render(text, True, (0, 0, 0), (255, 255, 255))
                textRect = text.get_rect()
                textRect.x = coords[0]
                textRect.y = coords[1]
                screen.blit(text, textRect)
            create_text(f"timestamp={point['t']:.5} [s]", (text_x_1, 100))
            create_text(f"v_car={point['v']:.5} [m/s]", (text_x_2, text_y_2_base+text_y_2_fac*1))
            create_text(f"yaw={point['yaw_rate']:.5}", (text_x_2, text_y_2_base+text_y_2_fac*1+20))

            ##
            # Legend
            ##
            def draw_legend_item(rect_idx, rect_name, rect_color):
                pygame.draw.rect(screen, rect_color,
                                pygame.Rect(rect_top_fac, rect_top+rect_top_fac*rect_idx, rect_top_fac, rect_top_fac))
                create_text(rect_name, (text_x_1, text_y_2_base+text_y_2_fac*(rect_idx + 1)))
                if data['name'] == rect_name:
                    create_text(f'v={calc_magnitude(point["vx"], point["vy"]):.5} [m/s]',
                                (text_x_2, text_y_2_base+text_y_2_fac*(rect_idx + 1)))

            draw_legend_item(0, 'Our car', COLOR_CENTER)
            draw_legend_item(1, '1st', COLOR_1ST)
            draw_legend_item(2, '2nd', COLOR_2ND)
            draw_legend_item(3, '3rd', COLOR_3RD)
            draw_legend_item(4, '4th', COLOR_4TH)

        pygame.display.flip()
        clock.tick(FPS)


def load_data():
    with open('cleaned/normalized.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


normalized_data = load_data()

play(normalized_data)
