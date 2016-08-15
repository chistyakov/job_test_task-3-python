#!/usr/bin/env python3

from io import StringIO
import unittest
from unittest.mock import patch


def my_code(d):
    print("")


class TestMyCode(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_one_level_dict(self, mock_stdout):
        my_code({
            'first': 'first_value',
            'second': 'second_value'
        })
        self.assertEqual(mock_stdout.getvalue(), """\
first:
    first_value
second:
    second_value
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_two_level_dict(self, mock_stdout):
        my_code({
            '1': {
                'child': '1/child/value'
            },
            '2': '2/value'
        })
        self.assertEqual(mock_stdout.getvalue(), """\
1:
    child:
        1/child/value
2:
    2/value
""")


if __name__ == "__main__":
    unittest.main()
