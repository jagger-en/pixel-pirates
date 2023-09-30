#!/usr/bin/env python3
import json
import pandas
import argparse
from utils.normalize_data_for_time import normalize as ut_normalize

parser = argparse.ArgumentParser(
    prog='Data animator',
    description='Animates excel file data')
parser.add_argument('-f', '--input-file', required=True,
                    dest='input_file')
parser.add_argument('-o', '--output-file', required=True,
                    dest='output_file')
parser.add_argument('-d', '--delta', required=True,
                    dest='delta')
args = parser.parse_args()


def get_normalized_points(x_data, y_data, t_data, v_data,
                          vx_data, vy_data, yaw_rate):

    points = [i for i in zip(x_data, y_data, t_data, v_data,
                             vx_data, vy_data, yaw_rate)]

    def time_func(item):
        return item[2]

    def filler_func():
        return (None, None, None, None, None, None, None)

    result = ut_normalize(points, float(args.delta), time_func,
                          filler_func)
    # Reformat for json output
    normalized_points = [
        {
            'x': pt[0],
            'y': pt[1],
            't': pt[2],
            'v': pt[3],
            'vx': pt[4],
            'vy': pt[5],
            'yaw_rate': pt[6],
            't_bucket': pt[7]
        } for pt in result
    ]
    return normalized_points


##
# Load to dataframe
##
df = pandas.read_excel(args.input_file)

normalized_points_list = []
for object in ['1st', '2nd', '3rd', '4th']:
    x_data = df[f'{object}ODist_X [m]']
    y_data = df[f'{object}ODist_Y [m]']
    t_data = df['Timestamp']
    v_data = df['VehicleSpeed [m/s]']
    vx_data = df[f'{object}OSp_X [m/s]']
    vy_data = df[f'{object}OSp_Y [m/s]']
    yaw_rate = df[f'YawRate']
    pts = get_normalized_points(x_data, y_data, t_data,
                                v_data, vx_data, vy_data, yaw_rate)

    print(f'==> [{object}]: {len(t_data)} timestamps,',
          f'{len(pts)} normalized points')
    normalized_points_list.append({'name': object, 'pts': pts})


with open(args.output_file, 'w', encoding='utf-8') as f:
    contents = json.dumps(normalized_points_list, indent=4)
    f.write(contents)

print(f'==> Normalized data written to {args.output_file}.')
