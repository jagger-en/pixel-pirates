#!/usr/bin/env python3


def normalize(items, delta, time_func, filler_func):
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
        else:
            result.append((*filler_func(),
                           [left, right]))
    return result
