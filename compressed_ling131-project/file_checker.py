'''This script was just used to make sure that no extra files were lingering in the wrong places of the corpus during 
our restructuring of the data.'''
import os

folders = os.listdir()
for folder in folders:
    if os.path.isdir(folder):
        shows = os.listdir(folder)
        for show in shows:
            if os.path.isfile(folder + "/"+ show):
                if show[:show.index(".")] != show[:-5] and os.path.isdir(folder + "/" + show[:show.index(".")]):
                    print(folder + "/" + show)
