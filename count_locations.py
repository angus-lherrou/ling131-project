import os
import json
import pandas as pd

if os.path.exists('show_counts.json'):
	with open('show_counts.json','r') as in_dict:
		show_dict = json.load(in_dict)

else:
	show_dict = {}


if os.path.exists('station_counts.json'):
	with open('station_counts.json','r') as in_dict:
		station_dict = json.load(in_dict)

else:
	station_dict = {}

def counts_by_show(ep_data):

	total_locs = len(ep_data['locations'])

	in_state = len(ep_data['in_state'])
	out_state = len(ep_data['out_state'])

	in_country = len(ep_data['in_country'])
	out_country = len(ep_data['out_country'])

	show = ep_data['show_name']

	if show not in show_dict.keys():
		show_dict[show] = [0] * 9

	#total loc mentions
	show_dict[show][0] += total_locs
	#in state mentions
	show_dict[show][1] += in_state
	#percent in state
	show_dict[show][2] = round(100 * (in_state/total_locs),2)
	#out of state mentions
	show_dict[show][3] += out_state
	#percent out of state
	show_dict[show][4] = round(100 * (out_state/total_locs),2)
	#in U.S. mentions
	show_dict[show][5] += in_country
	#percent in U.S.
	show_dict[show][6] = round(100 * (in_country/total_locs),2)
	#out of U.S. mentions
	show_dict[show][7] += out_country
	#percent out of U.S.
	show_dict[show][8] = round(100 * (out_country/total_locs),2)



def counts_by_station(ep_data):


	total_locs = len(ep_data['locations'])

	in_state = len(ep_data['in_state'])
	out_state = len(ep_data['out_state'])

	in_country = len(ep_data['in_country'])
	out_country = len(ep_data['out_country'])

	sta = ep_data['station']

	if sta not in station_dict.keys():
		station_dict[sta] = [0] * 9

	#total loc mentions
	station_dict[sta][0] += total_locs
	#in state mentions
	station_dict[sta][1] += in_state
	#percent in state
	station_dict[sta][2] = round(100 * (in_state/total_locs),2)
	#out of state mentions
	station_dict[sta][3] += out_state
	#percent out of state
	station_dict[sta][4] = round(100 * (out_state/total_locs),2)
	#in U.S. mentions
	station_dict[sta][5] += in_country
	#percent in U.S.
	station_dict[sta][6] = round(100 * (in_country/total_locs),2)
	#out of U.S. mentions
	station_dict[sta][7] += out_country
	#percent out of U.S.
	station_dict[sta][8] = round(100 * (out_country/total_locs),2)



def print_counts(counts):
	df = pd.DataFrame.from_dict(counts, 
			orient='index',
			columns=['Total Count','In State','In State %','Out of State','Out of State %','In US','In US %','Out of US','Out of US %'])
	print(df)

def print_show(show_name):
	show_line = {show_name: show_dict[show_name]}
	df = pd.DataFrame.from_dict(show_line, 
			orient='index',
			columns=['Total Count','In State','In State %','Out of State','Out of State %','In US','In US %','Out of US','Out of US %'])
	print(df)

def print_station(sta_name):
	sta_line = {sta_name: station_dict[sta_name]}
	df = pd.DataFrame.from_dict(sta_line, 
		orient='index',
		columns=['Total Count','In State','In State %','Out of State','Out of State %','In US','In US %','Out of US','Out of US %'])
	print(df)

def main():


	direct = 'data/KCSJ/'

	for file in os.listdir(direct):
		if file.endswith('.json'):
			with open(direct + file, 'r') as in_file:
				show_data = json.load(in_file)
			for episode in show_data:
				show_counts = counts_by_show(episode)
				station_counts = counts_by_station(episode)



	with open('show_counts.json','w') as shows_out:
		json.dump(show_dict, shows_out)

	with open('station_counts.json','w') as stations_out:
		json.dump(station_dict, stations_out)

	print_counts(show_dict)
	print_counts(station_dict)

	print_show('Allied Wealth and Visiting Angels')
	print_station('KCSJ')


main()
