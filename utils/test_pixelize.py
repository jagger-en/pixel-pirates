#!/usr/bin/env python3
import unittest
from pixelize import scale

class TestPixelizer(unittest.TestCase):

    def test_scaling(self):

        test_data = [
            # m     px    m         px
            (20,    0,    [20, 60], [0, 1980]),
            (21,    49.5, [20, 60], [0, 1980]),
            (22,    99,   [20, 60], [0, 1980]),
            (60,    1980,   [20, 60], [0, 1980]),
        ]

        for given_value, expected_mapped_value, right_lim, left_lim in test_data:
            mapped_value = scale(given_value, left_lim, right_lim)
            self.assertEqual(mapped_value, expected_mapped_value)



if __name__ == "__main__":
    unittest.main()
