#!/usr/bin/env python3

from itertools import chain, repeat, filterfalse
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
        queue = [(source_class(), ())]
        result = defaultdict(dict)
        while queue:

            queue = list(chain.from_iterable(
                result[algorithm.__class__.__name__].setdefault(
                    parents + (item.__class__, ), []).extend(
                        i.__class__ for i in algorithm(item)) or
                zip(algorithm(item),
                    repeat(parents + (item.__class__, )))
                for item, parents in queue
                for algorithm in self.algorithm_list
            ))

        #return {k: result[k] for k in result}
        return {k: Component._used_abilites_tuples_to_dict(result[k])
                for k in result}

    @staticmethod
    def _used_abilites_tuples_to_dict(dict_with_tuples):
        result = defaultdict(list)
        for parent_classpath_tuples in dict_with_tuples:
            new_key = "/" + "/".join(str(c.__name__)
                                     for c in parent_classpath_tuples)

            for child_class in unique_everseen(dict_with_tuples[parent_classpath_tuples]):
                result[new_key].append("{0}/{1}".format(
                    new_key, child_class.__name__))

        return {k: result[k] for k in result}



#https://docs.python.org/dev/library/itertools.html#itertools-recipes
def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element



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
