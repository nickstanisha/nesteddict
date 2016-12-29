from __future__ import absolute_import
from nesteddict import leaf_values, NestedDict
import pytest


class TestLeafValues:
    def test_shallow(self):
        d = {'a': 1, 'b': 'hello', 'c': (3, 2, 1), (1, 2, 3): 9}
        assert(set(leaf_values(d)) == {1, 'hello', (3, 2, 1), 9})

        d = NestedDict({'a': 1, 'b': 'hello', 'c': (3, 2, 1), (1, 2, 3): 9})
        assert(set(leaf_values(d)) == {1, 'hello', (3, 2, 1), 9})

        d = NestedDict()
        d[1] = 4
        d[2] = (3, 2, 1)
        d[4] = 'hello'
        assert(set(leaf_values(d)) == {4, (3, 2, 1), 'hello'})

    def test_nested(self):
        d = {1: {2: {3: {4: 5, 5: 'hello'}}}, 2: {(3, 2, 1): (1, 2, 3), 4: 16}}
        assert(set(leaf_values(d)) == {5, 'hello', (1, 2, 3), 16})

        assert(set(leaf_values(NestedDict(d))) == {5, 'hello', (1, 2, 3), 16})

        d = NestedDict()
        d[1, 2, 3, 4] = 5
        d[1, 2, 3, 5] = 'hello'
        d[2, (3, 2, 1)] = (1, 2, 3)
        d[2, 4] = 16
        assert (set(leaf_values(d)) == {5, 'hello', (1, 2, 3), 16})

    def test_raises(self):
        with pytest.raises(TypeError, message="Expecting TypeError"):
            i = leaf_values(123)
