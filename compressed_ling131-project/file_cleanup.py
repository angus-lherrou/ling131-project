import os

folders = os.listdir()
for file in folders:
    if os.path.isdir(file):
        shows = os.listdir(file)
        for show in shows:
            if os.path.isfile(file + "/" + show) and not show.startswith("."):
                os.remove(file+"/" + show)
