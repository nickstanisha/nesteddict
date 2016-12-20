""" A nested hash-map/dictionary object for Python """

import collections
try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = 0.1


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
            if cur_key not in self or not isinstance(self[cur_key], NestedDict):
                super(NestedDict, self).__setitem__(cur_key, NestedDict())
            self[cur_key][downstream] = value
        else:
            super(NestedDict, self).__setitem__(cur_key, value)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except (KeyError, TypeError):
            return default
