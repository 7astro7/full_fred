
[![PyPI](https://img.shields.io/pypi/v/full_fred)](https://pypi.org/project/full_fred/)
![PyPI Downloads](https://img.shields.io/pypi/dm/full_fred)
![GitHub issues](https://img.shields.io/github/issues/7astro7/full_fred)
![Unit Tests](https://github.com/7astro7/full_fred/actions/workflows/unittests.yml/badge.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)



# full_fred
`full_fred` is a Python interface to 
[FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/) that
prioritizes user preference, flexibility, and speed. `full_fred`'s API translates to Python
[every type of request FRED supports](https://fred.stlouisfed.org/docs/api/fred/):
each query for Categories, Releases, Series, Sources, and Tags 
found within FRED's web service has a method associated with it in `full_fred`.
`full_fred` minimizes redundant queries for the sake of users and FRED's servers. 
After a request for data is made to FRED web service the retrieved data 
is stored in a dictionary, accessible and fungible

## Installation
    pip install full-fred

## Testing
```full_fred``` requires ```pytest```. Tests can be run with ```FRED_API_KEY``` environment variable set and:

```python
pytest
```

## Usage

### API Key 
Queries to FRED web service require an API key. FRED has [free API keys available with an account (also free)](https://research.stlouisfed.org/useraccount/apikey)

You can tell ```full_fred``` about an api key in 2 secure ways:
1. fred.api_key_file can be set by passing it to the constructor
```python
In [4]: from full_fred.fred import Fred

In [5]: fred = Fred('example_key.txt')

In [6]: fred.get_api_key_file()
Out[6]: 'example_key.txt'
```
This will set it too
```python
In [3]: fred.set_api_key_file('example_key.txt')
Out[3]: True
```
If the file assigned to ```api_key_file``` can't be found, ```full_fred``` will say so immediately if api_key_file is set using 
the surefire ```fred.set_api_key_file()```  

2. FRED_API_KEY Environment Variable

```full_fred``` will automatically detect your api key if it's assigned to an environment variable named ```FRED_API_KEY```.
To check that FRED_API_KEY environment variable is detected, you can use 

```python
In [7]: fred.env_api_key_found()
Out[7]: True
```

```full_fred``` does not store your api key in an attribute for the sake of security: to send queries to FRED's databases, ```full_fred``` uses the value of 
FRED_API_KEY environment variable or the first line of fred.api_key_file

### Fetching data

A pandas DataFrame stores observations when a request for data values is made

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
```
The fetched data is stored in fred.series_stack (see __Accessing fetched data__ section for more on retrieving queried data)

```python
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
most general to most specific start with the root category 0. 
A search along the lines of the following can help to pinpoint different 
category_ids:

```python
In [4]: fred.get_child_categories(0)
Out[4]: 
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
  {'id': 32213, 'name': 'Greenbook Projections', 'parent_id': 0},
  {'id': 3008, 'name': 'U.S. Regional Data', 'parent_id': 0},
  {'id': 33060, 'name': 'Academic Data', 'parent_id': 0}]}

In [5]: fred.category_stack['get_child_categories']
Out[5]: 
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
  {'id': 32213, 'name': 'Greenbook Projections', 'parent_id': 0},
  {'id': 3008, 'name': 'U.S. Regional Data', 'parent_id': 0},
  {'id': 33060, 'name': 'Academic Data', 'parent_id': 0}]}
```

The [whole gamut of requests on FRED web service](https://fred.stlouisfed.org/docs/api/fred/) is implemented. The example below 
is one among many other methods in the API, listed in the next section

```python
In [1]: from full_fred.fred import Fred

In [2]: fred = Fred()

In [3]: fred.get_series_vintagedates('FYFSD', limit = 15)
Out[3]: 
{'realtime_start': '1776-07-04',
 'realtime_end': '9999-12-31',
 'order_by': 'vintage_date',
 'sort_order': 'asc',
 'count': 46,
 'offset': 0,
 'limit': 15,
 'vintage_dates': [
    '1998-02-02',
    '1998-10-26',
    '1999-02-01',
    '1999-10-25',
    '2000-02-07',
    '2000-10-20',
    '2001-04-09',
    '2001-10-24',
    '2002-02-04',
    '2002-10-23',
    '2003-02-03',
    '2003-10-15',
    '2004-02-02',
    '2004-10-12',
    '2005-02-23']}

In [4]: fred.series_stack['get_series_vintagedates']
Out[4]: 
{'realtime_start': '1776-07-04',
 'realtime_end': '9999-12-31',
 'order_by': 'vintage_date',
 'sort_order': 'asc',
 'count': 46,
 'offset': 0,
 'limit': 15,
 'vintage_dates': [
    '1998-02-02',
    '1998-10-26',
    '1999-02-01',
    '1999-10-25',
    '2000-02-07',
    '2000-10-20',
    '2001-04-09',
    '2001-10-24',
    '2002-02-04',
    '2002-10-23',
    '2003-02-03',
    '2003-10-15',
    '2004-02-02',
    '2004-10-12',
    '2005-02-23']}
```

### Accessing fetched data

There are 5 stacks: 

```fred.category_stack```
```fred.release_stack```
```fred.series_stack```
```fred.source_stack```
```fred.tag_stack```

After a method is called the returned data is stored using the method name for its key

Methods that store data in category stack:
```python
fred.category_stack["get_a_category"]
fred.category_stack["get_child_categories"]
fred.category_stack["get_related_categories"]
fred.category_stack["get_series_in_a_category"]
fred.category_stack["get_tags_for_a_category"]
fred.category_stack["get_related_tags_for_a_category"]
```

Methods that store data in release stack:
```python
fred.release_stack["get_a_release"]
fred.release_stack["get_tags_for_a_release"]
fred.release_stack["get_series_on_a_release"]
fred.release_stack["get_sources_for_a_release"]
fred.release_stack["get_related_tags_for_release"]
fred.release_stack["get_release_dates_all_releases"]
fred.release_stack["get_release_tables"]
fred.release_stack["get_release_dates"]
fred.release_stack["get_all_releases"]
```

Methods that store data in series stack:
```python
fred.series_stack["get_a_series"]
fred.series_stack["get_categories_of_series"]
fred.series_stack["get_series_df"]
fred.series_stack["get_release_for_a_series"]
fred.series_stack["search_for_series"]
fred.series_stack["get_tags_for_series_search"]
fred.series_stack["get_related_tags_for_series_search"]
fred.series_stack["get_tags_for_a_series"]
fred.series_stack["get_series_updates"]
fred.series_stack["get_series_vintagedates"]
```

Methods that store data in source stack:
```python
fred.source_stack["get_all_sources"]
fred.source_stack["get_releases_for_a_source"]
fred.source_stack["get_a_source"]
```

Methods that store data in tag stack:
```python
fred.tag_stack["get_all_tags"]
fred.tag_stack["get_related_tags_for_a_tag"]
fred.tag_stack["get_series_matching_tags"]
```

### full_fred realtime period and observation start/end defaults
By default ```fred.realtime_start``` and ```fred.realtime_end``` are set to None. 
realtime_start and realtime_end arguments override ```fred.realtime_start``` and ```fred.realtime_end```.

```fred.observation_start``` and ```fred.observation_end``` are also None by default. 
observation_start and observation_end arguments override ```fred.observation_start``` and ```fred.observation_end```.

## Contributing
The ```full_fred``` project welcomes feature requests, bug reports, bug fixes, documentation improvements, contributions of all kinds.
```full_fred``` aims to be responsive in integrating patches and listening to your feedback to be a community-driven API.
This project is also new and while ```full_fred``` is still young there's great opportunity to contribute elements that may have disproportionate
impact in the long run

## License
Apache v2.0
