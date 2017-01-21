from __future__ import absolute_import
from nesteddict import paths, NestedDict
import pytest


class TestNestedKeys:
    def test_shallow(self):
        d = {'a': 1, 'b': 'hello', 'c': (3, 2, 1), (1, 2, 3): 9}
        assert(set(paths(d)) == set([('a',), ('b',), ('c',), ((1, 2, 3),)]))

        d = NestedDict({'a': 1, 'b': 'hello', 'c': (3, 2, 1), (1, 2, 3): 9})
        assert (set(paths(d)) == set([('a',), ('b',), ('c',), ((1, 2, 3),)]))

        d = NestedDict()
        d[1] = 4
        d['hello'] = (3, 2, 1)
        d[(1, 2, 3), ] = 'hello'
        assert(set(paths(d)) == set([(1,), ('hello',), ((1, 2, 3),)]))

    def test_nested(self):
        d = {1: {2: {3: {4: 5, 5: 'hello'}}}, 2: {(3, 2, 1): (1, 2, 3), 4: 16}}
        assert(set(paths(d)) == set([(1, 2, 3, 4), (1, 2, 3, 5), (2, (3, 2, 1)), (2, 4)]))

        assert(set(paths(NestedDict(d))) == set([(1, 2, 3, 4), (1, 2, 3, 5), (2, (3, 2, 1)), (2, 4)]))

        d = NestedDict()
        d[1, 2, 3, 4] = 5
        d[1, 2, 3, 5] = 'hello'
        d[2, (3, 2, 1)] = (1, 2, 3)
        d[2, 4] = 16
        assert (set(paths(d)) == set([(1, 2, 3, 4), (1, 2, 3, 5), (2, (3, 2, 1)), (2, 4)]))

    def test_raises(self):
        with pytest.raises(TypeError, message="Expecting TypeError"):
            i = paths(123)