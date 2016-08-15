#!/usr/bin/env python3

from itertools import chain
import unittest


class Component:
    def __init__(self, *algorithm_list):
        self.algorithm_list = algorithm_list

    def __call__(self, source_object):
        result = []
        queue = [source_object]
        while queue:
            result.extend(queue)
            queue = list(chain.from_iterable(
                algorithm(item)
                for item in queue
                for algorithm in self.algorithm_list
            ))
        return result

    def my_method(self, source_class):
        return dict()


class Apple:
    pass


class Orange:
    def __init__(self, number):
        self.number = number


class Lemon:
    pass


class FirstAlgorithm:
    SPECIFICATION = {
        Orange: [Apple],
        Lemon: [Orange, Apple]
    }

    def __call__(self, source_object):
        if isinstance(source_object, Orange):
            return [
		Apple()
		for _ in range(source_object.number)
            ]

        if isinstance(source_object, Lemon):
            return [Orange(3), Apple()]
        return []


class EmptyAlgorithm:
    SPECIFICATION = {}

    def __call__(self, source_object):
        return []



class TestMyMethod(unittest.TestCase):
    def test_acceptance_from_task(self):
        component = Component(FirstAlgorithm(), EmptyAlgorithm())

        actual_result = component.my_method(Lemon)
        expected_result = {
            'Potential': [
                '/Lemon',
                '/Lemon/Orange',
                '/Lemon/Apple',
                '/Lemon/Orange/Apple'
            ],
            'Algorithm': {
                'FirstAlgorithm' : {
                    '/Lemon' : ['/Lemon/Orange', '/Lemon/Apple'],
                    },
                '/Lemon/Orange': ['/Lemon/Orange/Apple'],
                'EmptyAlgorithm': {}
                }
            }
        self.assertEqual(actual_result, expected_result)


def main():
    component = Component(FirstAlgorithm(), EmptyAlgorithm())

    result = component(Lemon())

    unittest.main()


if __name__ == "__main__":
    main()
