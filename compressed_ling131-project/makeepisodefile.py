'''This script took files containing dictionaries representing audio chunks from a single show on a single station
and wrote them into separate files based on the day the chunk was aired. It also removed unnecessary meta-data, and 
wrote the entire day's worth of chunks from the show into one dictionary.
import json
import os

def extract_show(folder):
    files = os.listdir(folder)
    for file in files:
        if not os.path.isfile(folder + "/" + file):
            continue
        dates = set()
        try:
            os.mkdir(folder + "/" + file[:-5].replace(" ", "_"))
        except:
            pass
        with open(folder + "/" +file, 'rt') as f:
            lines = f.readlines()
        for line in lines:
            if line[-1] == "\n" and line != "\n":
                chunk_dict = json.loads(line[:-1])
            elif line == "\n":
                pass
            else:
                chunk_dict = json.loads(line)
            date = chunk_dict['audio_chunk_id'][:chunk_dict['audio_chunk_id'].index("/")]
            filepath = folder + "/" + file[:-5].replace(" ", "_") + "/" + date + ".json"
            if date not in dates:
                dates.add(date)
                with open(filepath, 'wt') as f:
                    new_dict = {}
                    new_dict['station'] = chunk_dict['callsign']
                    new_dict['city'] = chunk_dict['city']
                    new_dict['state'] = chunk_dict['state']
                    try:
                        new_dict['show_name'] = chunk_dict['show_name']
                    except:
                        new_dict['show_name'] = "no_show"
                    new_dict['year'] = date[:4]
                    new_dict['month'] = date[date.index('-') + 1:date.index('-') + 3]
                    new_dict['day'] = date[-2:]
                    new_dict['content'] = chunk_dict['content']
                    f.write(json.dumps(new_dict))
            else:
                with open(filepath, 'rt') as f:
                    old_dict = json.load(f)
                old_dict['content'] = old_dict['content'] + "\n" + chunk_dict['content']
                with open(filepath, 'wt') as f:
                    f.write(json.dumps(old_dict))
x = input("all folders? y/n: ")
if x == "y":
    folders = os.listdir()
    for folder in folders:
        if os.path.isdir(folder):
            extract_show(folder)
if x == "n":
    folder = input("which one folder? ")
    extract_show(folder)
