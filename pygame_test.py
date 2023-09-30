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


COLOR_CENTER = (0, 0, 0)
COLOR_1ST = (1, 168, 255)
COLOR_2ND = (9, 230, 71)
COLOR_3RD = (230, 144, 9)
COLOR_4TH = (254, 24, 10)


def calc_magnitude(x, y):
    return math.sqrt(x**2 + y**2)

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
            # for point in data['pts']:
            point = data['pts'][idx]
            object_x = scale_x(point['x'])
            object_y = scale_y(point['y'])
            if data['name'] == '1st':
                color = COLOR_1ST

            if data['name'] == '2nd':
                color = COLOR_2ND

            if data['name'] == '3rd':
                color = COLOR_3RD

            if data['name'] == '4th':
                color = COLOR_4TH
            pygame.draw.circle(screen, COLOR_CENTER,
                               (scale_x(0), scale_y(0)), 20)
            pygame.draw.circle(screen, color, (object_x, object_y), 12)

            ##
            # Timestamp text
            ##
            def create_text(text, font_size, coords):
                font = pygame.font.Font('freesansbold.ttf', font_size)
                text = font.render(text, True, (0, 0, 0), (255, 255, 255))
                textRect = text.get_rect()
                textRect.x = coords[0]
                textRect.y = coords[1]
                screen.blit(text, textRect)

            timestamp = f"timestamp={point['t']:.5} [s]"
            create_text(timestamp, 20, (100, 100))

            velocity_of_vehicle = f"v={point['v']:.5} [m/s]"
            create_text(velocity_of_vehicle, 15, (200, 80+50*1))

            yaw_rate = f"yaw={point['yaw_rate']:.5}"
            create_text(yaw_rate, 15, (200, 80+50*1+20))

            ##
            # Legend
            ##
            pygame.draw.rect(screen, COLOR_CENTER,
                             pygame.Rect(50, 120, 50, 50))
            create_text('Our car', 20, (100, 80+50*1))

            pygame.draw.rect(screen, COLOR_1ST,
                             pygame.Rect(50, 120+50*1, 50, 50))
            create_text('1ST', 20, (100, 80+50*2))
            if data['name'] == '1st':
                create_text(f'v={calc_magnitude(point["vx"], point["vy"]):.5} [m/s]', 15, (200, 80+50*2))

            pygame.draw.rect(screen, COLOR_2ND,
                             pygame.Rect(50, 120+50*2, 50, 50))
            create_text('2ND', 20, (100, 80+50*3))
            if data['name'] == '2nd':
                create_text(f'v={calc_magnitude(point["vx"], point["vy"]):.5} [m/s]', 15, (200, 80+50*3))

            pygame.draw.rect(screen, COLOR_3RD,
                             pygame.Rect(50, 120+50*3, 50, 50))
            create_text('3RD', 20, (100, 80+50*4))
            if data['name'] == '3rd':
                create_text(f'v={calc_magnitude(point["vx"], point["vy"]):.5} [m/s]', 15, (200, 80+50*4))

            pygame.draw.rect(screen, COLOR_4TH,
                             pygame.Rect(50, 120+50*4, 50, 50))
            create_text('4TH', 20, (100, 80+50*5))
            if data['name'] == '4th':
                create_text(f'v={calc_magnitude(point["vx"], point["vy"]):.5} [m/s]', 15, (200, 80+50*5))

        pygame.display.flip()
        clock.tick(FPS)


def load_data():
    with open('cleaned/normalized.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


normalized_data = load_data()

play(normalized_data)
