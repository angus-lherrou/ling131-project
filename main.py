"""main.py

Script to generate a heatmap for a user-determined show
in the compressed_ling131-project directory, and point
the user to the location of the map.

Author: Angus L'Herrou
"""

import os
import radiomap

if __name__ == '__main__':
    pwd = 'compressed_ling131-project'
    level = ['station', 'show']
    action = ['browse', 'query']
    i = 0
    q = False

    while not q:
        print(level[i].title()+'s:')
        for d in os.listdir(pwd):
            print('   ', d)
        print(f'Select a {level[i]} to {action[i]}:')
        if i == 0:
            pwd += '/'+input('> ')
        else:
            show = input('> ')
            path = f'{pwd}/{show}.pkl'
            if not os.path.exists(path):
                print("Bye")
                break
            outpath = radiomap.gen_map(path)
            print(f'Map is ready at {outpath}')
            q = True
        i += 1
