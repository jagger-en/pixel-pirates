#!/usr/bin/env python3
def normalize_df(df, delta, object_names):
    normalized_points_list = []
    for object in object_names:
        x_data = df[f'{object}ObjectDistance_X']
        y_data = df[f'{object}ObjectDistance_Y']
        t_data = df['Timestamp']
        v_data = df['VehicleSpeed']
        vx_data = df[f'{object}ObjectSpeed_X']
        vy_data = df[f'{object}ObjectSpeed_Y']
        yaw_rate = df[f'YawRate']
        pts = _get_normalized_points(x_data, y_data, t_data,
                                     v_data, vx_data, vy_data, yaw_rate, delta)

        print(f'==> [{object}]: {len(t_data)} timestamps,',
              f'{len(pts)} normalized points')
        normalized_points_list.append({'name': object, 'pts': pts})
    return normalized_points_list


def _get_normalized_points(x_data, y_data, t_data, v_data,
                           vx_data, vy_data, yaw_rate, delta):

    points = [i for i in zip(x_data, y_data, t_data, v_data,
                             vx_data, vy_data, yaw_rate)]

    def time_func(item):
        return item[2]

    result = normalize_based_on_timestamp(points, delta, time_func)
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


def normalize_based_on_timestamp(items, delta, time_func):
    times = [time_func(item) for item in items]
    times.sort()
    earliest = times[0]
    latest = times[-1]

    normalized_times = []
    counter = earliest
    while counter < latest:
        normalized_times.append(counter)
        counter = counter + delta

    result = []
    for normalized_time in normalized_times:
        left = normalized_time
        right = normalized_time + delta
        matches = [i for i in items
                   if left <= time_func(i) and
                   right >= time_func(i)
                   ]

        if matches:
            for match in matches:
                result.append((*match,
                               [left, right]))
                prev = match
        else:
            result.append((*prev,
                           [left, right]))
    return result
