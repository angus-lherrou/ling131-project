'''
find_all.py

Script to run functions from module to get locations
in a given episode text. 
Retrieve max 5 episodes per show.
'''

import os
import re
import json
import finalfindlocs as fl


#modify these to match corpus in and out paths
INPATH = "compressed_ling131-project"
OUTPATH = "located_data"


#traverse the directory and retrieve episode files
def traverse_dir():
    counter = 0
    for folder in os.listdir(INPATH):
        if not os.path.exists(os.path.join(OUTPATH, folder)):
            os.mkdir(os.path.join(OUTPATH, folder))
        for subfolder in os.listdir(os.path.join(INPATH,folder)):
            time.sleep(5)
            if os.path.isdir(os.path.join(INPATH, folder, subfolder)):
                print (subfolder)
                savedir = os.path.join(OUTPATH, folder, subfolder)
                if not os.path.exists(savedir):
                    os.mkdir(savedir)
                infolder = os.path.join(INPATH, folder, subfolder)
                episode_count = 0
                for filename in os.listdir(infolder):
                    if episode_count < 5:
                        get_file(infolder, filename)
                        episode_count += 1
         
    return
             

#Process file with fl.get_data method
def get_file(infolder, filename):
    infile = os.path.join(infolder, filename)
    if filename.endswith('.gz'):
        continue
    t0 = time.time()
    #store return val (1=success, 0=failure) to track Geonames Exceed errot                   
    x = fl.get_data(infile, savedir)
    if x == 0:
        return
    with open('read.txt', 'a') as f:
        f.write(os.path.join(infolder, filename) + ":" + str(t1-t0) + ":\n")      
    return


if not os.path.exists(OUTPATH):
    os.mkdir(OUTPATH)

traverse_dir()
