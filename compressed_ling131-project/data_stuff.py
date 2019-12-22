from adapted_main_a4 import Text
import nltk
import os
import pickle
import gzip
import json
from collections import defaultdict
if not os.path.isfile("pickledtokencts"):
    if os.path.isfile("pickledtokencts"):
        with open("pickledtokencts", "rb") as f:
            counts_rawtokens_telephone_female = pickle.load(f)
    else:
        shows = os.listdir("WBUR_shownames")
        counts_rawtokens_telephone_female = defaultdict(list)
        for file in shows:
            dummy = Text("WBUR_shownames/" + file )
            counts_rawtokens_telephone_female[file] = [len(dummy)]

        with open("pickledtokencts", "wb") as f:
            pickle.dump(counts_rawtokens_telephone_female, f)

    shows_female_tkncounts = defaultdict(int)
    shows_telephone_tkncounts = defaultdict(int)
    shows_ungendered_tkcounts = defaultdict(int)
    f = gzip.open("WBUR.json.gz", "rt")

    lines = f.readlines()
    fucked = []
    for line in lines:
        try:
            entry = json.loads(line[:-1])
        except:
            fucked.append(line)
            print(line)
            continue
        try:
            show = entry['show_name']
        except:
            show = 'no_show'
        try:
            content = entry['content']
        except:
            print("No content")
            continue
        try:
            tele = entry['studio_or_telephone']
        except:
            tele = 'not'
        try:
            gender = entry["guessed_gender"]
        except:
            gender = "no gender"
        if tele == 'T':
            shows_telephone_tkncounts[show] = shows_telephone_tkncounts[show] + len(content.split(" "))
        if gender == 'F':
            shows_female_tkncounts[show] = shows_female_tkncounts[show] + len(content.split(" "))
    for key in counts_rawtokens_telephone_female.keys():
        counts_rawtokens_telephone_female[key].append(shows_telephone_tkncounts[key[:-10]])
        counts_rawtokens_telephone_female[key].append(shows_female_tkncounts[key[:-10]])
        counts_rawtokens_telephone_female[key].append(shows_ungendered_tkcounts[key[:-10]])
    with open("pickledtokencts", "wb") as f:
        pickle.dump(counts_rawtokens_telephone_female, f)
    diction = counts_rawtokens_telephone_female
else:
    with open("pickledtokencts", "rb") as f:
        diction = pickle.load(f)
sum_telephone = 0
sum_tokens = 0
sum_female = 0
for key in  diction.keys():
    sum_telephone += diction[key][1]
    sum_tokens += diction[key][0]
    sum_female += diction[key][2]
print("Total Oct WBUR Tokens")
print(sum_tokens)
print("\"Female\" Voice Token %")
print(sum_female/float(sum_tokens)*100)
print("Phone-in Token %")
print(sum_telephone/float(sum_tokens)*100)
for key in diction.keys():
    print(diction[key][:-10], file=output)
    print(key + ": \n\ttotal tokens ", file=output)
    print(diction[key][0], file=output)
    print("\n\ttelephone tokens ", file=output)
    print(diction[key][1]/float(diction[key][0]) *100, file=output)
    print("\n\tfemale tokens ", file=output)
    print(diction[key][2]/float(diction[key][0]) *100, file=output)
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
objects = [show[:-10] for show in diction.keys()]
object = [show for show in diction.keys()]
y_pos = np.arange(len(object))
performance = [diction[show][2]/float(diction[show][0]) *100 for show in object]

plt.bar(y_pos, performance, align='center', alpha=1)
plt.xticks(y_pos, objects)
plt.xticks(rotation='vertical')
plt.ylabel('Female Tokens')
plt.title('Show')

plt.show()

with open("pickledLocLabelTuples.pkl", "rb") as f:
    tuplelist = pickle.load(f)
for x in tuplelist:
    print(x)
