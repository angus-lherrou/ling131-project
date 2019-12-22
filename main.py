"""main.py

Script to generate a heatmap for a user-determined show
in the compressed_ling131-project directory, and point
the user to the location of the map.

Author: Angus L'Herrou
"""

import os
import radiomap

if __name__ == '__main__':
    directory = 'compressed_ling131-project'
    level = ['station', 'show']

    while True:
        print('Stations:')
        for d in os.listdir(directory):
            print('   ', d)
        print('Select a station to query:')
        station = input('> ').upper()
        directory = f'{directory}/{station}'
        while not os.path.isdir(directory):
            print(f"No station called {station}! Try again:")
            station = input('> ').upper()
            directory = f'{directory}/{station}'

        # TODO: print statistics about the current station

        answer = ''
        print("Query a show in this station? (Y/n)")
        while answer.lower() not in {'y', 'n', 'yes', 'no'}:
            response = input('> ')
            answer = response if response else 'y'
        if answer.lower().startswith('y'):
            while True:
                print(f'Shows in {station}:')
                for d in os.listdir(directory):
                    print('   ', d)
                print()
                print(f'Select a show in {station} to query:')
                show = input('> ')

                # TODO: print statistics about the current station

                path = f'{directory}/{show}/{show}.pkl'
                if not os.path.exists(path):
                    # TODO: generate pickle
                    raise Exception(f'No pickle at {path}!')
                out_path = radiomap.gen_map(path)
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
