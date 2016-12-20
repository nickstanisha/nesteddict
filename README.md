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
nested_dictionary['a', 'b', 'c'] = 3
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

## Uses

One of the envisioned use-cases of this data structure is specifying
[Elasticsearch queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html)
as dicts.

```python
>>> from nesteddict import NestedDict
>>> import json
>>> query = NestedDict()
>>> query['query', 'bool', 'must', 'match', 'title'] = 'A book title'
>>> query['query', 'bool', 'filter', 'term', 'status'] = 'published'
>>> print(json.dumps(query, indent=4, sort_keys=True))
{
    "query": {
        "bool": {
            "filter": {
                "term": {
                    "status": "published"
                }
            },
            "must": {
                "match": {
                    "title": "A book title"
                }
            }
        }
    }
}
```
