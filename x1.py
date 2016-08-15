#!/usr/bin/env python3

from io import StringIO
import unittest
from unittest.mock import patch
from collections import OrderedDict, Mapping


INDENTATION_LENGTH = 4


def my_code(obj, current_indentation=0):
    for key in sorted(obj):
        value = obj[key]
        print_with_indentation(key + ":", current_indentation)
        if isinstance(value, Mapping):
            my_code(value, current_indentation+INDENTATION_LENGTH)
        else:
            print_with_indentation(
                str(value),
                current_indentation + INDENTATION_LENGTH
            )

def print_with_indentation(s, indentation):
    print("{0}{1}".format(" " * indentation, s))



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

    @patch('sys.stdout', new_callable=StringIO)
    def test_ordered_dict(self, mock_stdout):
        my_code(OrderedDict([
            ('a', 1),
            ('b', 2),
            ('c', {'x': 'fff'}),
            ('d', OrderedDict([
                ('e', 4), ('f', {'g': 5})
            ])
            )
        ]))
        self.assertEqual(mock_stdout.getvalue(), """\
a:
    1
b:
    2
c:
    x:
        fff
d:
    e:
        4
    f:
        g:
            5
""")



if __name__ == "__main__":
    unittest.main()
