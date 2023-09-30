#!/usr/bin/env python3
def scale_linearly(given_value, left_lim, right_lim):
    m = (left_lim[1] - left_lim[0]) / (right_lim[1] - right_lim[0])
    mapped_value = given_value * m + (left_lim[0] - m * right_lim[0])
    return mapped_value
