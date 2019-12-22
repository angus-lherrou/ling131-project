import os
import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def counts_by_show(direct):
	show_dict = {}
	total_locs = 0
	in_state = 0
	out_state = 0
	in_country = 0
	out_country = 0

	with open(direct) as in_file:
		show_data = json.load(in_file)

	show_name = show_data[0]['show_name']

	for episode in show_data:

		total_locs += len(episode['locations'])

		in_state += len(episode['in_state'])
		out_state += len(episode['out_state'])

		in_country += len(episode['in_country'])
		out_country += len(episode['out_country'])

	show_dict[show_name] = [0] * 9

	#total loc mentions
	show_dict[show_name][0] += total_locs
	#in state mentions
	show_dict[show_name][1] += in_state
	#percent in state
	show_dict[show_name][2] = round(100 * (in_state/total_locs),2)
	#out of state mentions
	show_dict[show_name][3] += out_state
	#percent out of state
	show_dict[show_name][4] = round(100 * (out_state/total_locs),2)
	#in U.S. mentions
	show_dict[show_name][5] += in_country
	#percent in U.S.
	show_dict[show_name][6] = round(100 * (in_country/total_locs),2)
	#out of U.S. mentions
	show_dict[show_name][7] += out_country
	#percent out of U.S.
	show_dict[show_name][8] = round(100 * (out_country/total_locs),2)

	df = pd.DataFrame.from_dict(show_dict,
		orient='index',
		columns=['Total Count','In State','In State %','Out of State','Out of State %','In US','In US %','Out of US','Out of US %'])
	print(df)


def counts_by_station(direct):
	station_dict = {}
	total_locs = 0
	in_state = 0
	out_state = 0
	in_country = 0
	out_country = 0
	dirlist = [d for d in os.listdir(direct) if d.endswith('.json')]
	with open(direct + '/' + dirlist[0], 'r') as in_file:
		first_file = json.load(in_file)
	first_ep = first_file[0]
	ep_station = first_ep['station']

	for file in dirlist:
		with open(direct + '/' + file, 'r') as in_file:
			show_data = json.load(in_file)
		for episode in show_data:
			total_locs += len(episode['locations'])

			in_state += len(episode['in_state'])
			out_state += len(episode['out_state'])

			in_country += len(episode['in_country'])
			out_country += len(episode['out_country'])

	station_dict[ep_station] = [0] * 9

	#total loc mentions
	station_dict[ep_station][0] += total_locs
	#in state mentions
	station_dict[ep_station][1] += in_state
	#percent in state
	station_dict[ep_station][2] = round(100 * (in_state/total_locs),2)
	#out of state mentions
	station_dict[ep_station][3] += out_state
	#percent out of state
	station_dict[ep_station][4] = round(100 * (out_state/total_locs),2)
	#in U.S. mentions
	station_dict[ep_station][5] += in_country
	#percent in U.S.
	station_dict[ep_station][6] = round(100 * (in_country/total_locs),2)
	#out of U.S. mentions
	station_dict[ep_station][7] += out_country
	#percent out of U.S.
	station_dict[ep_station][8] = round(100 * (out_country/total_locs),2)

	df = pd.DataFrame.from_dict(station_dict,
		orient='index',
		columns=['Total Count','In State','In State %','Out of State','Out of State %','In US','In US %','Out of US','Out of US %'])
	print(df)
