""" A nested hash-map/dictionary object for Python """

import collections
try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = "0.1"
__all__ = ['NestedDict', 'leaf_values', 'nested_keys', 'to_nested_dict']


def _dfs_generator(dictionary):
    if not isinstance(dictionary, dict):
        raise TypeError("Unsupported type '{}'".format(type(dictionary).__name__))

    stack = [(val, [key]) for key, val in dictionary.items()]
    while stack:
        d, path = stack.pop()
        if isinstance(d, dict):
            stack.extend([(val, path + [key]) for key, val in d.items()])
        else:
            yield d, tuple(path)


def to_nested_dict(dictionary):
    """ Casts a given `dict` as a `NestedDict` (does not change the contents of the original `dict`)

        Returns
        -------
        d : NestedDict
            The contents of the original `dict`, in a `NestedDict` object
    """
    d = NestedDict()
    for val, key in _dfs_generator(dictionary):
        d[key] = val
    return d


def nested_keys(dictionary):
    """ Return tuples representing paths to the bottom of a dict

        Returns
        -------
        out : list[tuple]
            A list of tuples representing paths retrieved in depth-first order from the dict

        Examples
        --------
        >>> d = {1: {2: {3: 4, 4: 5}}, 2: {3: {4: 5}}}
        >>> print(nested_keys(d))
        [(2, 3, 4), (1, 2, 4), (1, 2, 3)]
    """
    return [path for val, path in _dfs_generator(dictionary)]


def leaf_values(dictionary):
    """ Returns the values at the bottom of a dictionary

        Returns
        -------
        out : list
            A list of the bottom-most values in a dictionary, retrieved in depth-first order

        Examples
        --------
        >>> d = {1: {2: {3: 4, 4: 5}}, 2: {3: {4: 5}}}
        >>> print(leaf_values(d))
        [5, 5, 4]
    """
    return [val for val, path in _dfs_generator(dictionary)]


class NestedDict(dict):
    """ An object representing a dictionary of dictionaries of dictionaries ...

        In order to avoid code like this

        >>> if 'a' in dictionary:
        ...     if 'b' in dictionary['a']
        ...         dictionary['a']['b']['c'] = 3
        ...     else:
        ...         dictionary['a']['b'] = {'c': 3}
        ... else:
        ...     dictionary['a'] = {'b': {'c': 3}}

        NestedDict enables the following syntax

        >>> nested_dictionary['a', 'b', 'c'] = 3

        A defaultdict coult be used to accomplish a similar goal, but only to
        a finite depth specified at the time of construction

        >>> # Nested dictionary of depth 4
        >>> d = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

        NestedDict is able to handle nested dictinoaries of arbitrary depth. Additionally,
        since NestedDict extends `dict`, it prints nicely to the console by default

        >>> my_default_dict
        defaultdict(<function <lambda> at 0x10077f840>, {1: defaultdict(<function <lambda>.<locals>.<lambda> at 0x10185a400>, {2: 3})})
        >>> my_nested_dict
        {1: {2: 3}}
    """
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], dict) and not isinstance(args[0], NestedDict):
            for val, key in _dfs_generator(args[0]):
                self[key] = val
        else:
            super(NestedDict, self).__init__(*args, **kwargs)

    @staticmethod
    def _split_key(key):
        if isinstance(key, collections.Sequence) and not isinstance(key, basestring):
            return key[0], key[1:]
        else:
            return key, []

    def __getitem__(self, key):
        cur_key, downstream = self._split_key(key)
        if downstream:
            return super(NestedDict, self).__getitem__(cur_key)[downstream]
        else:
            return super(NestedDict, self).__getitem__(cur_key)

    def __setitem__(self, key, value):
        cur_key, downstream = self._split_key(key)
        if downstream:
            if cur_key not in self or not isinstance(super(NestedDict, self).__getitem__(cur_key), NestedDict):
                super(NestedDict, self).__setitem__(cur_key, NestedDict())
            super(NestedDict, self).__getitem__(cur_key)[downstream] = value
        else:
            if isinstance(value, dict) and not isinstance(value, NestedDict):
                super(NestedDict, self).__setitem__(cur_key, NestedDict(value))
            else:
                super(NestedDict, self).__setitem__(cur_key, value)

    def __delitem__(self, key):
        if isinstance(key, collections.Sequence) and not isinstance(key, basestring):
            upstream, cur_key = key[:-1], key[-1]
            d = self[upstream] if upstream else self
            super(NestedDict, d).__delitem__(cur_key)
        else:
            super(NestedDict, self).__delitem__(key)

    def get_nested(self, key, default=None):
        """ Get a path from a `NestedDict` (analogous to `dict.get` except keys get analyzed as paths """
        try:
            return self[key]
        except (KeyError, TypeError):
            return default

    def get(self, key, default=None):
        """ A short-circuit to `dict.get`, will not parse tuples into a path before applying changes

            Examples
            --------
            >>> v = d[(1, 2, 3),]  # will raise if the key (1, 2, 3) does not exist in d
            >>> v = d.get((1, 2, 3))  # will return `None` if the key (1, 2, 3) does not exist in d
        """
        try:
            return super(NestedDict, self).__getitem__(key)
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """ A short-circuit to `dict.__setitem__`, will not parse tuples into a path before applying changes

            Examples
            --------
            >>> # The following are equivalent
            >>> d = NestedDict()
            >>> d[(1, 2, 3),] = 4
            >>> d[[(1, 2, 3)]] = 4
            >>> d.set((1, 2, 3), 4)
        """
        return super(NestedDict, self).__setitem__(key, value)

    def delete(self, key):
        """ A short-circuit to `dict.__delitem__`, will not parse tuples into a path before applying changes

            Examples
            --------
            >>> # The following are equivalent
            >>> d = NestedDict()
            >>> del d[(1, 2, 3),]
            >>> d.delete((1, 2, 3))
        """
        return super(NestedDict, self).__delitem__(key)

    def leaf_values(self):
        """ Return the values at the bottom of a nested dict (Analogous to `dict.values`)

            Returns
            -------
            out : list
                A list of leaf values retrieved in depth-first order from the NestedDict
        """
        return [val for val, path in _dfs_generator(self)]

    def nested_keys(self):
        """ Return tuples representing paths to the bottom of a nested dict (Analogous to `dict.keys`)

            Returns
            -------
            out : list[tuple]
                A list of tuples representing paths retrieved in depth-first order from the NestedDict
        """
        return [path for val, path in _dfs_generator(self)]

    def nested_update(self, obj):
        """ Works like `dict.update` except only the leaf values of the supplied dictionary are
            used to update `self`

            Examples
            --------
            >>> print(d)
            {1: {2: {3: {4: 5, 5: 6}}}, 2: {3: 5, 4: 16}}
            >>> print(e)
            {1: {2: {3: {5: 7}}}, 2: {5: 1}}
            >>> d.nested_update(e)
            >>> print(d)
            {1: {2: {3: {4: 5, 5: 7}}}, 2: {3: 5, 4: 16, 5: 1}}
        """
        for val, path in _dfs_generator(obj):
            self[path] = val
