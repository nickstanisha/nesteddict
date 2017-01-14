from __future__ import absolute_import
from nesteddict import to_nested_dict, NestedDict
import pytest


class TestToNestedDict:
    def test_raises(self):
        with pytest.raises(TypeError, message="Expecting TypeError"):
            d = to_nested_dict([1, 2, 3])

        with pytest.raises(TypeError, message="Expecting TypeError"):
            d = to_nested_dict('{1: 2, 3: 4}')

        with pytest.raises(TypeError, message="Expecting TypeError"):
            d = to_nested_dict(4)

    def test_nested_types(self):
        d = to_nested_dict({1: {2: {3: {4: 5, 5: 6}}}, 2: {3: 5, 4: 16}})
        assert(isinstance(d, NestedDict))
        assert(isinstance(d[1, 2, 3], NestedDict))
        assert(isinstance(d[2], NestedDict))
        assert(all(hasattr(d, att) for att in
                   ['nested_update', 'leaf_values', 'paths', 'set', 'delete']))