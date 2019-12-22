"""main.py

Script to generate a heatmap for a user-determined show
in the compressed_ling131-project directory, and point
the user to the location of the map.

Author: Angus L'Herrou
"""

import os
import radiomap
import count_locations as cl
import create_dataframe as cdf

if __name__ == '__main__':
    directory = 'compressed_ling131-project'
    level = ['station', 'show']
    while True:
        print('Stations:')
        for d in os.listdir(directory):
            if os.path.isdir(directory+'/'+d):
                print('   ', d)
        print('Select a station to query:')
        station = input('> ').upper()
        directory = f'{directory}/{station}'
        while not os.path.isdir(directory):
            print(f"No station called {station}! Try again:")
            station = input('> ').upper()
            directory = f'{directory}/{station}'

        cl.counts_by_station(f'data/{station}')

        map_df = cdf.make_station_df(f'data/{station}')
        out_path = radiomap.gen_map(map_df)
        print(f'Map is ready at {out_path}')
        print()

        answer = ''
        print("Query a show in this station? (Y/n)")
        while answer.lower() not in {'y', 'n', 'yes', 'no'}:
            response = input('> ')
            answer = response if response else 'y'
        if answer.lower().startswith('y'):
            while True:
                print(f'Shows in {station}:')
                show_list = []
                for i, show_dir in enumerate([d for d in os.listdir(directory)
                                       if os.path.isdir(directory + '/' + d)]):
                    print(f'{i:>4}  {show_dir}')
                    show_list.append(show_dir)
                print()
                print(f'Select a show index in {station} to query:')
                show = show_list[int(input('> '))]

                cl.counts_by_show(f'data/{station}/{show}/{show}.json')

                show_map_df = cdf.make_show_df(f'data/{station}/{show}/{show}.json')
                out_path = radiomap.gen_map(show_map_df)
                print(f'Map is ready at {out_path}')
                print()
                answer = ''
                print("Query another show? (Y/n)")
                while answer.lower() not in {'y', 'n', 'yes', 'no'}:
                    response = input('> ')
                    answer = response if response else 'y'
                if answer.lower().startswith('n'):
                    break
        answer = ''
        print("Query another station? (Y/n)")
        while answer.lower() not in {'y', 'n', 'yes', 'no'}:
            response = input('> ')
            answer = response if response else 'y'
        if answer.lower().startswith('n'):
            break
