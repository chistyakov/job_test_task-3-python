#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from io import StringIO

def my_code(connectivity_matrix_dict, first_node):
    visited_nodes = []
    def visit_not_visited_neighbours(node):
        visited_nodes.append(node)
        for neighbour in connectivity_matrix_dict.get(node, []):
            if neighbour not in visited_nodes:
                visit_not_visited_neighbours(neighbour)

    visit_not_visited_neighbours(first_node)
    print("\n".join(str(n) for n in visited_nodes))

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
    def test_acceptance_from_task_2(self, mock_stdout):
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

    @patch('sys.stdout', new_callable=StringIO)
    def test_first_node_does_not_have_neighbours(self, mock_stdout):
        data = {
            1: [2, 3],
            2: [3, 4],
            4: [1],
        }
        my_code(data, 5)
        self.assertEqual(mock_stdout.getvalue(), """\
5
""")


if __name__ == "__main__":
    unittest.main()
