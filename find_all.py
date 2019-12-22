import os
import re
import json
import gzip
import time
import finalfindlocs as fl



INPATH = "compressed_ling131-project"
OUTPATH = "located_data"



def get_text(inpath, outpath):
    fl.get_data(inpath, outpath)
    return 

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
                for filename in os.listdir(infolder):
                    infile = os.path.join(infolder, filename)
                    if filename.endswith('.gz'):
                        continue
                    t0 = time.time()                   
                    x = fl.get_data(infile, savedir)
                    if x == 0:
                        return
                    t1 = time.time()
                    counter += 1
                    print(counter)
                    with open('read.txt', 'a') as f:
                        f.write(os.path.join(infolder, filename) + ":" + str(t1-t0) + ":\n")
    return
                   
if not os.path.exists(OUTPATH):
    os.mkdir(OUTPATH)


traverse_dir()
