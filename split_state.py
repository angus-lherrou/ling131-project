#Dominique O'Donnell
'''
Script splits corpus by state, takes first 20 docs from each state.
Add cityname to new doc file name and write to 'state' path

Purpose: 
A quick way to peek at a subset of the data without untarring it on 
your machine.
'''

import gzip
import re
import os
from collections import defaultdict

in_file = 'radiotalk.json.gz'
in_meta = False
text = ''
states = defaultdict(int)

with gzip.open(in_file,'rt') as f:
    counter = 0
    for line in f:
        counter += 1
        state = re.search('.*?\"state\": \"(.*?)\"', line)
        city = re.search('.*?\"city\": \"(.*?)\"', line)
        name = re.search('.*?\"signature\": \"(.*?)\"', line)
        doc_city = city.group(1)
        doc_state = state.group(1)
        try:
            doc_name = name.group(1)
        except:
            doc_name = str(counter)
        if states[doc_state] >= 20:
            continue
        states[doc_state] += 1
        save_dir = os.path.join(os.path.dirname(in_file), doc_state)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        f = open(os.path.join(save_dir, doc_name + '_' + doc_city), 'wt')
        f.write(line)
        f.close()

 
