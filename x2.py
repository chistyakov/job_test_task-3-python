#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from io import StringIO

def my_code(connectivity_matrix_dict, first_node):
    print("")

class TestMyCode(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_acceptance_from_task_1(self, mock_stdout):
        data = {
            1: [2, 3],
            2: [4],
        }
        my_code(data, 1)
        self.assertEqual(mock_stdout.getvalue(), """\
1
2
4
3
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_acceptance_from_task_1(self, mock_stdout):
        data = {
            1: [2, 3],
            2: [3, 4],
            4: [1],
        }
        my_code(data, 1)
        self.assertEqual(mock_stdout.getvalue(), """\
1
2
3
4
""")


if __name__ == "__main__":
    unittest.main()
