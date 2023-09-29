#!/usr/bin/env python3
import unittest
from normalize_data_for_time import normalize


class TestNormalizationOfDataForTime(unittest.TestCase):

    def test_various_values(self):
        items = [
            (1, 1, 0.5),
            (2, 2, 0.701),
            (3, 3, 1.022),
            (4, 4, 1.088),
            (5, 5, 1.107),
        ]

        def time_func(item):
            return item[2]

        def filler_func():
            return (None, None, None)

        result = normalize(items, 0.1, time_func, filler_func)

        expected = [
            (1,    1,    0.5,   [0.5, 0.6]),
            (None, None, None,  [0.6, 0.7]),
            (2,    2,    0.701, [0.7, 0.7999999999999999]),
            (None, None, None,  [0.7999999999999999, 0.8999999999999999]),
            (None, None, None,  [0.8999999999999999, 0.9999999999999999]),
            (3,    3,    1.022, [0.9999999999999999, 1.0999999999999999]),
            (4,    4,    1.088, [0.9999999999999999, 1.0999999999999999]),
            (5,    5,    1.107, [1.0999999999999999, 1.2]),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
