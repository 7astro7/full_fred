
# Under construction

## full_fred
`full_fred` is a Python interface to 
[FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/) that
prioritizes user preference, flexibility, and speed. `full_fred`'s API translates to Python
[every type of request FRED supports](https://fred.stlouisfed.org/docs/api/fred/):
each query for Categories, Releases, Series, Sources, and Tags 
found within FRED's web service has a method associated with it in `full_fred`.
`full_fred` minimizes redundant queries for the sake of users and FRED's servers. 
After a request for data is made to FRED web service the retrieved data 
is saved in a dictionary, accessible and fungible. 

## Installation
    pip install full_fred

FRED has [free API keys available immediately](https://research.stlouisfed.org/useraccount/apikey)

## Testing

## API

expand: search_for_series -> get_tags_for_series_search -> get_related_tags_for_series_search

api key can be set in 2 secure ways:
api key file
environment variable

full_fred doesn't save api_key for the sake of security

```python
api_key_found()
```

```python
from full_fred import Fred
fred = Fred()
fred.get_all_sources()
```

```python
fred.get_series_df('GDPPOT')
    realtime_start realtime_end        date               value
0       2021-04-03   2021-04-03  1949-01-01         2103.179936
1       2021-04-03   2021-04-03  1949-04-01  2130.7327210000003
2       2021-04-03   2021-04-03  1949-07-01  2159.4478710000003
3       2021-04-03   2021-04-03  1949-10-01         2186.907265
4       2021-04-03   2021-04-03  1950-01-01          2216.07306
..             ...          ...         ...                 ...
327     2021-04-03   2021-04-03  2030-10-01            23219.35
328     2021-04-03   2021-04-03  2031-01-01            23318.31
329     2021-04-03   2021-04-03  2031-04-01            23417.38
330     2021-04-03   2021-04-03  2031-07-01            23516.38
331     2021-04-03   2021-04-03  2031-10-01            23615.28

[332 rows x 4 columns]

fred.series_stack['get_series_df']
{'realtime_start': '2021-04-03',
 'realtime_end': '2021-04-03',
 'observation_start': '1600-01-01',
 'observation_end': '9999-12-31',
 'units': 'lin',
 'output_type': 1,
 'file_type': 'json',
 'order_by': 'observation_date',
 'sort_order': 'asc',
 'count': 332,
 'offset': 0,
 'limit': 100000,
 'series_id': 'GDPPOT',
 'df':     
realtime_start      realtime_end        date               value
 0       2021-04-03   2021-04-03  1949-01-01         2103.179936
 1       2021-04-03   2021-04-03  1949-04-01  2130.7327210000003
 2       2021-04-03   2021-04-03  1949-07-01  2159.4478710000003
 3       2021-04-03   2021-04-03  1949-10-01         2186.907265
 4       2021-04-03   2021-04-03  1950-01-01          2216.07306
 ..             ...          ...         ...                 ...
 327     2021-04-03   2021-04-03  2030-10-01            23219.35
 328     2021-04-03   2021-04-03  2031-01-01            23318.31
 329     2021-04-03   2021-04-03  2031-04-01            23417.38
 330     2021-04-03   2021-04-03  2031-07-01            23516.38
 331     2021-04-03   2021-04-03  2031-10-01            23615.28
 
 [332 rows x 4 columns]}
```

To find a specific category_id or to search FRED categories from
most general to most specific you can start with 0, the root category. 
A search along the lines of the following can help to pinpoint different 
category_ids:

```python
fred.get_child_categories(0)
{'categories': [{'id': 32991,
   'name': 'Money, Banking, & Finance',
   'parent_id': 0},
  {'id': 10,
   'name': 'Population, Employment, & Labor Markets',
   'parent_id': 0},
  {'id': 32992, 'name': 'National Accounts', 'parent_id': 0},
  {'id': 1, 'name': 'Production & Business Activity', 'parent_id': 0},
  {'id': 32455, 'name': 'Prices', 'parent_id': 0},
  {'id': 32263, 'name': 'International Data', 'parent_id': 0},
  {'id': 3008, 'name': 'U.S. Regional Data', 'parent_id': 0},
  {'id': 33060, 'name': 'Academic Data', 'parent_id': 0}]}
```

full_fred realtime period defaults:
realtime start is set to earliest available '1776-07-04'
realtime end is set to latest available '9999-12-31'
to use defaults set by FRED web service realtime period for each query, 
you can set realtime_start attribute and realtime_end attribute to None
```python
fred.realtime_start = None
fred.realtime_end = None
```

reference get_series_df example 
more generally, note use of stacks 
    - limited redundancy
    - metadata included

## Contributing
The full_fred project welcomes feature requests, bug submissions, contributions of all kinds.
full_fred aims to be responsive in integrating patches, 

## License
GPLv3
