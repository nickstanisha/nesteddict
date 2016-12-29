[![Build Status](https://travis-ci.org/nickstanisha/nesteddict.svg?branch=master)](https://travis-ci.org/nickstanisha/nesteddict)

# nesteddict
A nested dictionary data structure for Python.

In order to avoid code like this
```python
if 'a' in dictionary:
    if 'b' in dictionar['a']
        dictionary['a']['b']['c'] = 3
    else:
        dictionary['a']['b'] = {'c': 3}
else:
    dictionary['a'] = {'b': {'c': 3}}
```

NestedDict enables the following syntax

```python
from nesteddict import NestedDict
d = NestedDict()
d['a', 'b', 'c'] = 3
```

A defaultdict coult be used to accomplish a similar goal, but only to
a finite depth specified at the time of construction

```python
>>> # Nested dictionary of depth 4
>>> d = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
```

NestedDict is able to handle nested dictinoaries of arbitrary depth. Additionally,
since NestedDict extends `dict`, it prints nicely to the console by default

```python
>>> my_default_dict
defaultdict(<function <lambda> at 0x10077f840>, {1: defaultdict(<function <lambda>.<locals>.<lambda> at 0x10185a400>, {2: 3})})
>>> my_nested_dict
{1: {2: 3}}
```

## Install
Clone this repository and run `python setup.py develop` to install.

## Notes
Tuples are automatically parsed into `NestedDict` paths when used with the `[]` operator. That means that there is no difference between `nesteddict[1, 2, 3] = 4` and `nesteddict[(1, 2, 3)] = 4`. In order to use tuples as keys, you must use one of the following approaches
```python
>>> d[(1, 2, 3), ] = 4
>>> d.set((1, 2, 3), 4)
```
`NestedDict` has three public methods that act as short circuits to the underlying `__getitem__`, `__setitem__` and `__delitem__` methods of the base class `dict`: `nesteddict.set`, `nesteddict.get` and `nesteddict.delete`. Use those functions any time you want to be positive that you are using the standard `dict` behavior.
