#!/usr/bin/env python3

##
## Usage:
## ./clean_data.py -f ./data/DevelopmentData.xlsx -o ./data/DevelopmentData_cleaned.xlsx
##

import pandas
import argparse

parser = argparse.ArgumentParser(
                    prog='Data cleaner',
                    description='Cleans excel file data')
parser.add_argument('-f', '--input-file', required=True,
                    dest='input_file')
parser.add_argument('-o', '--output-file', required=True,
                    dest='output_file')
args = parser.parse_args()

##
## Load to dataframe
##
df = pandas.read_excel(args.input_file)


def replace_common(text):
    return text.replace('Object', 'O') \
               .replace('First', '1st') \
               .replace('Second', '2nd') \
               .replace('Third', '3rd') \
               .replace('Fourth', '4th')

##
## DIVIDE COLUMNS BY 128, 256, 256
##
FACTOR_OBJ_DIST_X_Y = 128  # [m]
OBJ_DIST_COLUMNS = ['FirstObjectDistance_X', 'FirstObjectDistance_Y',
                    'SecondObjectDistance_X', 'SecondObjectDistance_Y',
                    'ThirdObjectDistance_X', 'ThirdObjectDistance_Y',
                    'FourthObjectDistance_X', 'FourthObjectDistance_Y']
def cleanup_obj_dist_col(text):
    return replace_common(text.replace('Distance', 'Dist'))
for obj_dist_col in OBJ_DIST_COLUMNS:
    df[obj_dist_col] = df[obj_dist_col].div(FACTOR_OBJ_DIST_X_Y)
    df.rename(columns={obj_dist_col: cleanup_obj_dist_col(f'{obj_dist_col} [m]')},
              inplace=True)

FACTOR_VEHICLE_SPEED = 256  # [m/s]
df['VehicleSpeed'] = df['VehicleSpeed'].div(FACTOR_VEHICLE_SPEED)
df.rename(columns={'VehicleSpeed': f'VehicleSpeed [m/s]'},
          inplace=True)

FACTOR_OBJECT_SPEEDS_X_Y = 256  # [m/s]
OBJ_SPEED_COLUMNS = ['FirstObjectSpeed_X', 'FirstObjectSpeed_Y',
                    'SecondObjectSpeed_X', 'SecondObjectSpeed_Y',
                    'ThirdObjectSpeed_X', 'ThirdObjectSpeed_Y',
                    'FourthObjectSpeed_X', 'FourthObjectSpeed_Y']
def cleanup_obj_speed_col(text):
    return replace_common(text.replace('Speed', 'Sp'))
for obj_dist_col in OBJ_SPEED_COLUMNS:
    df[obj_dist_col] = df[obj_dist_col].div(FACTOR_OBJECT_SPEEDS_X_Y)
    df.rename(columns={obj_dist_col: cleanup_obj_speed_col(f'{obj_dist_col} [m/s]')},
              inplace=True)

##
## Export
##
df.to_excel(args.output_file)
print(f'Written cleaned data to {args.output_file}')
