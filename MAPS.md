# How to generate a map

Construct a Pandas DataFrame for a given location (city, state, radio station, etc) from a dict as follows:

```python
import pandas as pd

data = {'location': [<location name>, <lat>, <lon>],
        '0': [<mention 1 name>, <lat>, <lon>],
        '1': [<mention 2 name>, <lat>, <lon>],
        '2': [<mention 3 name>, <lat>, <lon>], ...}

dataframe = pd.DataFrame.from_dict(data,
                       orient='index',
                       columns=['title', 'latitude', 'longitude'])

```

Generate the map in `maps/` by calling the following method from radiomap.py:

```python
import radiomap

radiomap.gen_map(dataframe)
```

This will generate a file called `<location name>.png` in `maps/`.

