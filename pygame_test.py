import pygame
import sys
import pandas as pd

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualization")

# Load object speed data from CSV
df = pd.read_csv('Dev_data.csv')
speed_data = df[['1stODist_X [m]', '1stODist_Y [m]', 'Timestamp']].values.tolist()

# Object properties
object_x, object_y = WIDTH // 2, HEIGHT // 2
current_speed_index = 0
object_speed_x, object_speed_y, timestamp = speed_data[current_speed_index]

# Game loop
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks() / 1000.0  # Convert milliseconds to seconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # elapsed_time (since game started)
    elapsed_time = (pygame.time.get_ticks() / 1000.0) - start_time

    # Object speed update??
    while current_speed_index < len(speed_data) - 1 and elapsed_time >= timestamp:
        current_speed_index += 1
        object_speed_x, object_speed_y, timestamp = speed_data[current_speed_index]

    # Update object position based on speed
    object_x += object_speed_x
    object_y += object_speed_y

    # Wrap object around the screen if it goes off the edges
    if object_x > WIDTH:
        object_x = 0
    if object_x < 0:
        object_x = WIDTH
    if object_y > HEIGHT:
        object_y = 0
    if object_y < 0:
        object_y = HEIGHT

    screen.fill(WHITE)
    pygame.draw.circle(screen, (0, 0, 255), (int(object_x), int(object_y)), 20)
    pygame.display.flip()
    clock.tick(FPS)
