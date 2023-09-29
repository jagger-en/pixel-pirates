#!/usr/bin/env python3
import pandas
import argparse
from utils.normalize_data_for_time import normalize as ut_normalize
from utils.plot_utils import create_animation_gif

parser = argparse.ArgumentParser(
                    prog='Data animator',
                    description='Animates excel file data')
parser.add_argument('-f', '--input-file', required=True,
                    dest='input_file')
args = parser.parse_args()

##
## Load to dataframe
##
df = pandas.read_excel(args.input_file)


x_data = df['1stODist_X [m]']
y_data = df['1stODist_Y [m]']
t_data = df['Timestamp']

points = [i for i in zip(x_data, y_data, t_data)]



def time_func(item):
    return item[2]

def data_func(item):
    return item[:2]

def filler_func():
    return (None, None)



result = ut_normalize(points, 0.1, time_func, data_func, filler_func)
result = result[170:300]

normalized_points = [(p[0], p[1]) for p in result if p[0] and p[1]]


# for p in normalized_points:
#     print(p)

print('==> Creating animation GIF')
create_animation_gif(
    file_path="obj_animation.gif",
    normalized_points=normalized_points,
    x_lim=[60, 65],
    y_lim=[20, 0],
    title='Moving object',
    y_label_name='y coords',
    x_label_name='x coords',
    frames_per_second=2,
)
