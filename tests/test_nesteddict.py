from __future__ import absolute_import
from nesteddict import NestedDict
import pytest


class TestNestedDict:
    def test_init(self):
        d = NestedDict()
        assert(isinstance(d, NestedDict))

    def test_kwargs_init(self):
        d = NestedDict(a=[2, 3, 4], b=24, c='hello')
        assert(d == {'a': [2, 3, 4], 'b': 24, 'c': 'hello'})

    def test_iter_init(self):
        d = NestedDict([(1, 2), (3, 4), ('hello', 'goodbye')])
        assert(d == {1: 2, 3: 4, 'hello': 'goodbye'})

        d = NestedDict([(1, 2), (3, {4: 5})])
        assert(isinstance(d[3], NestedDict))

    def test_dict_coverage(self):
        nested_pubs = set(i for i in dir(NestedDict()) if not i.startswith('_'))
        assert all(i in nested_pubs for i in dir(dict()) if not i.startswith('_'))

    def test_dict_init(self):
        d = NestedDict({1: {2: {3: {4: {5: 6}}}}})
        assert(d[1, 2, 3, 4, 5] == 6)
        assert(isinstance(d, NestedDict))
        assert(all(isinstance(d[i], NestedDict) for i in [(1,), (1, 2), (1, 2, 3), (1, 2, 3, 4)]))

    def test_dict_init_tuples(self):
        d = NestedDict({(1, 2, 3): 4, (5, 6, 7): 8})
        assert(d[(1, 2, 3), ] == 4)
        assert(d.get((1, 2, 3)) == 4)
        with pytest.raises(KeyError, message="Expecting KeyError"):
            i = d[(1, 2, 3)]

        d = NestedDict({(1, 2, 3): {(4, 3, 2): 1, 'hello': 'goodbye'}, 'a': {('a', 'b', 'c'): 2}})
        assert(d == {(1, 2, 3): {(4, 3, 2): 1, 'hello': 'goodbye'}, 'a': {('a', 'b', 'c'): 2}})

    def test_setter(self):
        d = NestedDict()
        d[1, 'a', 34] = [1, 2]
        assert(d == {1: {'a': {34: [1, 2]}}})

        d[1, 'a', 34].extend([4, 3])
        assert(d == {1: {'a': {34: [1, 2, 4, 3]}}})

        d[1, 'a'] = 'hello'
        assert(d == {1: {'a': 'hello'}})

    def test_empty_no_unintentional_set(self):
        d = NestedDict()
        item = d.get('a')
        assert(d == {})

        item = d.get((1, 2, 3))
        assert(d == {})

        item = d.get_path((1, 2, 3))
        assert(d == {})

    def test_nonempty_no_unintentional_set(self):
        d = NestedDict()
        d[1, 2, 3] = 'hello'
        d[1, 2, 4] = 'goodbye'
        item = d.get(2)
        assert(d == {1: {2: {3: 'hello', 4: 'goodbye'}}})
        item = d.get((1, 2, 5, 6))
        assert(d == {1: {2: {3: 'hello', 4: 'goodbye'}}})
        item = d.get_path((1, 2, 5))
        assert(d == {1: {2: {3: 'hello', 4: 'goodbye'}}})

    def test_shallow_setter(self):
        d = NestedDict()
        d[1] = 'a'
        assert(d == {1: 'a'})

    def test_getter(self):
        d = NestedDict()
        d['a', 'b', 'c'] = 'hello'
        d['a', 'b', 'd'] = 'goodbye'

        assert(d['a', 'b', 'c'] == 'hello')
        assert(d['a', 'b'] == {'c': 'hello', 'd': 'goodbye'})

    def test_shallow_get(self):
        d = NestedDict()
        d[1, 2, 3] = 4
        d[(1, 2, 3),] = 5

        assert(d.get(1) == {2: {3: 4}})
        assert(d.get(2) is None)
        assert(d.get(2, 'arbitrary') == 'arbitrary')

    def test_shallow_get_tuples(self):
        d = NestedDict()
        d[1, 2, 3] = 4
        d[(1, 2, 3),] = 5

        assert(d.get((1, 2, 3)) == 5)
        assert(d.get(1) == {2: {3: 4}})
        assert(d.get((1, 2, 4), 'arbitrary') == 'arbitrary')

    def test_nested_get(self):
        d = NestedDict()
        d[1, 2, 3] = 4
        assert(d.get_path([1, 3]) is None)
        assert(d.get_path([1, 3], 'arbitrary') == 'arbitrary')
        assert(d.get_path([1, 2, 3]) == 4)

    def test_get_errors(self):
        d = NestedDict()
        d['a', 'b', 'c'] = 23
        with pytest.raises(KeyError, message="Expecting KeyError"):
            val = d['a', 'c']

        with pytest.raises(KeyError, message="Expecting KeyError"):
            val = d['b']

        with pytest.raises(TypeError, message="Expecting TypeError"):
            val = d['a', 'b', 'c', 'd']

    def test_update(self):
        """ This maintains `dict`s functionality, only merging the
            top-level keys.
        """
        d, e, = NestedDict(), NestedDict()
        d[1, 2, 3] = [1, 2]
        d[2, 'k'] = 16
        e[1, 2, 4] = [3, 4]
        e[3] = 'hello'
        d.update(e)
        assert(d == {1: {2: {4: [3, 4]}}, 2: {'k': 16}, 3: 'hello'})

    def test_set(self):
        d = NestedDict()
        d.set((1, 2, 3), 4)

        assert(d[(1, 2, 3), ] == 4)
        assert(d.get((1, 2, 3)) == 4)

        with pytest.raises(KeyError, message="Unintentional assignment in `set`"):
            item = d[1, 2, 3]

    def test_delete(self):
        d = NestedDict({(1, 2, 3): 4, 1: {2: {3: 4}}})
        d.delete((1, 2, 3))
        assert(d == {1: {2: {3: 4}}})

    def test_leaf_values(self):
        d = NestedDict()
        d[1] = 4
        d[2] = (3, 2, 1)
        d[4] = 'hello'
        assert (set(d.leaf_values()) == {4, (3, 2, 1), 'hello'})

    def test_leaf_values_nested(self):
        d = NestedDict()
        d[1, 2, 3, 4] = 5
        d[1, 2, 3, 5] = 'hello'
        d[2, (3, 2, 1)] = (1, 2, 3)
        d[2, 4] = 16
        assert (set(d.leaf_values()) == {5, 'hello', (1, 2, 3), 16})

    def test_paths(self):
        d = NestedDict()
        d[1] = 4
        d['hello'] = (3, 2, 1)
        d[(1, 2, 3), ] = 'hello'
        assert (set(d.paths()) == {(1,), ('hello',), ((1, 2, 3),)})

        d = NestedDict()
        d[1, 2, 3, 4] = 5
        d[1, 2, 3, 5] = 'hello'
        d[2, (3, 2, 1)] = (1, 2, 3)
        d[2, 4] = 16
        assert (set(d.paths()) == {(1, 2, 3, 4), (1, 2, 3, 5), (2, (3, 2, 1)), (2, 4)})

    def test_update(self):
        d = NestedDict({1: {2: {3: {4: 5, 5: 6}}}, 2: {3: 5, 4: 16}})
        e = {1: {2: {3: {5: 7}}}, 2: {5: 1}}
        d.update(e)
        assert(d == {1: {2: {3: {4: 5, 5: 7}}}, 2: {3: 5, 4: 16, 5: 1}})

        d = NestedDict({1: {2: {3: {4: 5, 5: 6}}}, 2: {3: 5, 4: 16}})
        e = NestedDict({1: {2: {3: {5: 7}}}, 2: {5: 1}})
        d.update(e)
        assert(d == {1: {2: {3: {4: 5, 5: 7}}}, 2: {3: 5, 4: 16, 5: 1}})

    def test_update_complex_keys(self):
        d = NestedDict({(1, 2, 3): {(4, 3, 2): 1, 'hello': 'goodbye'}, 'a': {('a', 'b', 'c'): 2}})
        e = {1: 2, (1, 2, 3): 4, 'hello': {'good': 'bye', 'bon': 'voyage'}}
        d.update(e)

        assert(d == {1: 2, (1, 2, 3): 4, 'hello': {'good': 'bye', 'bon': 'voyage'}, 'a': {('a', 'b', 'c'): 2}})

    def test_del(self):
        d = NestedDict({(1, 2, 3): {(4, 3, 2): 1, 'hello': 'goodbye'}, 'a': {('a', 'b', 'c'): 2}})
        del d[(1, 2, 3), 'hello']
        assert(d == {(1, 2, 3): {(4, 3, 2): 1}, 'a': {('a', 'b', 'c'): 2}})

        del d['a']
        assert(d == {(1, 2, 3): {(4, 3, 2): 1}})

        with pytest.raises(KeyError, message="Expected KeyError"):
            del d[1, 2, 3]
            assert (d == {(1, 2, 3): {(4, 3, 2): 1}})
