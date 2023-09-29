#!/usr/bin/env python3
from utils.plot_utils import create_animation_gif

points = [
    (0, 0),
    (0, 0),
    (1, 1),
    (2, 3),
    (2, 3.5),
    (2, 3.6),
    (2, 3.7),
    (1, 3.8),
]

create_animation_gif(
    file_path="obj_animation.gif",
    normalized_points=points,
    x_lim=[0 ,5],
    y_lim=[0 ,5],
    title='Moving object',
    y_label_name='y coords',
    x_label_name='x coords',
)
