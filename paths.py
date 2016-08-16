#!/usr/bin/env python3

from itertools import chain, repeat
import unittest
from collections import defaultdict


class Component:
    def __init__(self, *algorithm_list):
        self.algorithm_list = algorithm_list

    #hangs on cycles
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
        potential_paths_list = self._get_potential_paths_list(source_class)
        abilities_per_algorithm_dict = self._get_used_abilites(source_class)

        return {
            'Potential': potential_paths_list,
            'Algorithm': abilities_per_algorithm_dict
        }

    #hangs on cycles
    def _get_potential_paths_list(self, source_class):
        result = []
        queue = [(source_class, ())]
        while queue:
            result.extend(queue)
            queue = list(chain.from_iterable(
                zip(algorithm.SPECIFICATION.get(item, []),
                    repeat(parents + (item, )))
                for item, parents in queue
                for algorithm in self.algorithm_list
            ))
        return ['/' + '/'.join(str(c.__name__) for c in parents + (tail, ))
                for tail, parents in result]

    #hangs on cycles
    def _get_used_abilites(self, source_class):
        result = []
        queue = [(source_class, ())]
        d = defaultdict(dict)
        while queue:
            result.extend(queue)

            queue = list(chain.from_iterable(
                d[algorithm.__class__.__name__].setdefault(
                    parents + (item, ), []).extend(
                        algorithm.SPECIFICATION.get(item, [])) or
                zip(algorithm.SPECIFICATION.get(item, []),
                    repeat(parents + (item, )))
                for item, parents in queue
                for algorithm in self.algorithm_list
            ))

        #return {k: d[k] for k in d}
        return {k: Component._used_abilites_tuples_to_dict(d[k]) for k in d}

    @staticmethod
    def _used_abilites_tuples_to_dict(dict_with_tuples):
        result = defaultdict(list)
        for parent_classpath_tuples in dict_with_tuples:
            new_key = "/" + "/".join(str(c.__name__) for c in parent_classpath_tuples)

            for child_class in dict_with_tuples[parent_classpath_tuples]:
                result[new_key].append("{0}/{1}".format(new_key, child_class.__name__))

        return {k: result[k] for k in result}



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
                    '/Lemon/Orange': ['/Lemon/Orange/Apple'],
                },
                'EmptyAlgorithm': {}
                }
            }
        self.assertEqual(actual_result, expected_result)


def main():
    component = Component(FirstAlgorithm(), EmptyAlgorithm())

    result = component.my_method(Lemon)

    unittest.main()


if __name__ == "__main__":
    main()
