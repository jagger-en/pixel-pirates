#!/usr/bin/env python3
def clean_df(df, object_names):
    '''
    Prepares dataframe for further usage.
    Specific columns are divided by given constants.
    '''
    ##
    # DIVIDE COLUMNS BY 128, 256, 256
    ##
    FACTOR_OBJ_DIST_X_Y = 128  # [m]
    OBJ_DIST_COLUMNS = [f'{n}ObjectDistance_X' for n in object_names] + \
                       [f'{n}ObjectDistance_Y' for n in object_names]

    for obj_dist_col in OBJ_DIST_COLUMNS:
        df[obj_dist_col] = df[obj_dist_col].div(FACTOR_OBJ_DIST_X_Y)

    FACTOR_VEHICLE_SPEED = 256  # [m/s]
    df['VehicleSpeed'] = df['VehicleSpeed'].div(FACTOR_VEHICLE_SPEED)

    FACTOR_OBJECT_SPEEDS_X_Y = 256  # [m/s]
    OBJ_SPEED_COLUMNS = [f'{n}ObjectSpeed_X' for n in object_names] + \
                        [f'{n}ObjectSpeed_Y' for n in object_names]


    for obj_dist_col in OBJ_SPEED_COLUMNS:
        df[obj_dist_col] = df[obj_dist_col].div(FACTOR_OBJECT_SPEEDS_X_Y)

    return df
