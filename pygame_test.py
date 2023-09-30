#!/usr/bin/env python3
import pygame
import sys
import time
import json
from utils import pixelize

WIDTH = 800
HEIGHT = 600
FPS = 20

WHITE = (255, 255, 255)
GREEN = (50, 200, 50)


MIN_X = -120
MAX_X = 120

MIN_Y = -120
MAX_Y = 120


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
                color = (0, 255, 0)

            if data['name'] == '2nd':
                color = (255, 0, 0)

            if data['name'] == '3rd':
                color = (255, 0, 255)

            if data['name'] == '4th':
                color = (0, 0, 0)
            pygame.draw.circle(screen, (0, 0, 255), (scale_x(0), scale_y(0)), 20)
            pygame.draw.circle(screen, color, (object_x, object_y), 12)

            ##
            ## Timestamp text
            ##
            timestamp = f"timestamp={point['t']:.5}"
            font = pygame.font.Font('freesansbold.ttf', 25)
            text = font.render(timestamp, True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (WIDTH / 4, HEIGHT / 4)
            screen.blit(text, textRect)

        pygame.display.flip()
        clock.tick(FPS)


def load_data():
    with open('cleaned/normalized.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())

normalized_data = load_data()

play(normalized_data)
