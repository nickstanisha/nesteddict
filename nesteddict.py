""" A nested hash-map/dictionary object for Python """

import collections
try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = "0.1"
__all__ = ['NestedDict', 'leaf_values', 'paths', 'to_nested_dict']


def _dfs_generator(dictionary):
    if not isinstance(dictionary, (dict, NestedDict)):
        raise TypeError("Unsupported type '{}'".format(type(dictionary).__name__))

    stack = [(val, [key]) for key, val in dictionary.items()]
    while stack:
        d, path = stack.pop()
        if isinstance(d, (dict, NestedDict)):
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


def paths(dictionary):
    """ Return tuples representing paths to the bottom of a dict

        Returns
        -------
        out : list[tuple]
            A list of tuples representing paths retrieved in depth-first order from the dict

        Examples
        --------
        >>> d = {1: {2: {3: 4, 4: 5}}, 2: {3: {4: 5}}}
        >>> print(paths(d))
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


class NestedDict(collections.MutableMapping):
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
        self._dict = dict()
        if args and isinstance(args[0], (dict, NestedDict)):
            for val, key in _dfs_generator(args[0]):
                self[key] = val
        else:
            # Args must be a single argument -- an iterable of pairs.
            if args:
                args = [(x, NestedDict(y) if isinstance(y, dict) else y) for (x, y) in args[0]]
            kwargs = {k: NestedDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
            self._dict = dict(args, **kwargs)

    @staticmethod
    def _split_path(key):
        if isinstance(key, collections.Sequence) and not isinstance(key, basestring):
            return key[0], key[1:]
        else:
            return key, []

    def __getitem__(self, path):
        cur_key, downstream = self._split_path(path)
        if downstream:
            return self._dict[cur_key][downstream]
        else:
            return self._dict[cur_key]

    def __setitem__(self, path, value):
        cur_key, downstream = self._split_path(path)
        if downstream:
            if cur_key not in self._dict or not isinstance(self._dict[cur_key], NestedDict):
                self._dict[cur_key] = NestedDict()
            self._dict[cur_key][downstream] = value
        else:
            self._dict[cur_key] = NestedDict(value) if isinstance(value, dict) else value

    def __delitem__(self, path):
        if isinstance(path, collections.Sequence) and not isinstance(path, basestring):
            upstream, cur_key = path[:-1], path[-1]
            d = self[upstream] if upstream else self
            del d._dict[cur_key]
        else:
            del self._dict[path]

    def __iter__(self):
        for i in self._dict:
            yield (i, )
        # return iter(self._dict)

    def __contains__(self, path):
        try:
            self.__getitem__(path)
            return True
        except (KeyError, TypeError):
            return False

    def __repr__(self):
        return self._dict.__repr__()

    def __str__(self):
        return self._dict.__str__()

    def __eq__(self, other):
        if isinstance(other, NestedDict):
            return self._dict.__eq__(other._dict)
        else:
            return self._dict.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self._dict)

    def copy(self):
        """ Analogous to `dict.copy`, returns a new NestedDict matching `self`. Since
            NestedDicts are deep by nature, this functions as a "deepcopy"
        """
        return NestedDict(self)

    def delete(self, key):
        """ A short-circuit to `dict.__delitem__`, will not parse tuples into a path before applying changes

            Examples
            --------
            >>> # The following are equivalent
            >>> d = NestedDict()
            >>> del d[(1, 2, 3),]
            >>> d.delete((1, 2, 3))
        """
        del self._dict[key]

    @classmethod
    def fromkeys(cls, seq, value=None):
        """ Create a new NestedDict with keys from `seq` and values set to `value` """
        value = NestedDict(value) if isinstance(value, dict) else value
        return NestedDict([(k, value) for k in seq])

    def get_path(self, path, default=None):
        """ Get a path from a `NestedDict` (analogous to `dict.get` except keys get analyzed as paths """
        try:
            return self[path]
        except (KeyError, TypeError):
            return default

    def get(self, key, default=None):
        """ A short-circuit to `dict.get`, will not parse tuples into a path before applying changes

            Examples
            --------
            >>> v = d[(1, 2, 3),]  # will raise if the key (1, 2, 3) does not exist in d
            >>> v = d.get((1, 2, 3))  # will return `None` if the key (1, 2, 3) does not exist in d
        """
        return self._dict.get(key, default)

    def keys(self):
        return self._dict.keys()

    def items(self):
        return self._dict.items()

    def leaf_values(self):
        """ Return the values at the bottom of a nested dict (Analogous to `dict.values`)

            Returns
            -------
            out : list
                A list of leaf values retrieved in depth-first order from the NestedDict
        """
        return [val for val, path in _dfs_generator(self)]

    def paths(self):
        """ Return tuples representing paths to the bottom of a nested dict (Analogous to `dict.keys`)

            Returns
            -------
            out : list[tuple]
                A list of tuples representing paths retrieved in depth-first order from the NestedDict
        """
        return [path for val, path in _dfs_generator(self)]

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
        self._dict[key] = value

    def to_dict(self):
        """ Returns a dictionary from a NestedDict object """
        return dict((k, v.to_dict() if isinstance(v, NestedDict) else v) for k, v in self.items())

    def update(self, obj):
        """ Works like `dict.update` except only the leaf values of the supplied dictionary are
            used to update `self`

            Examples
            --------
            >>> print(d)
            {1: {2: {3: {4: 5, 5: 6}}}, 2: {3: 5, 4: 16}}
            >>> print(e)
            {1: {2: {3: {5: 7}}}, 2: {5: 1}}
            >>> d.update(e)
            >>> print(d)
            {1: {2: {3: {4: 5, 5: 7}}}, 2: {3: 5, 4: 16, 5: 1}}
        """
        for val, path in _dfs_generator(obj):
            self[path] = val
