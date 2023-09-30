#!/usr/bin/env python3
def clean_df(df):
    '''
    Prepares dataframe for further usage.
    Specific columns are divided by given constants.
    '''
    def replace_common(text):
        return text.replace('Object', 'O') \
            .replace('First', '1st') \
            .replace('Second', '2nd') \
            .replace('Third', '3rd') \
            .replace('Fourth', '4th')

    ##
    # DIVIDE COLUMNS BY 128, 256, 256
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
    return df
