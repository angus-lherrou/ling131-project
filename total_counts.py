"""This script runs through all shows and stations in the data folder, and returns a csv
of counts and percentages of location mentions, relative to the location of the station."""

import os
import json
import pandas as pd


def counts_by_station(direct):

	sta_count_dict = {}

	sta_list = [d for d in os.listdir(direct) if os.path.isdir(direct + '/' + d)]

	#for each station, count tokens, loc mentions, and percentages
	for station in sta_list:
		sta_path = direct + '/' + station
		sta_count_dict[station] = [0] * 16

		show_list = [show for show in os.listdir(sta_path) if os.path.isdir(sta_path + '/' + show)]

		show_dir = [(sta_path + '/' + show + '/' + show + '.json') for show in show_list 
					if os.path.isfile(sta_path + '/' + show + '/' + show + '.json')]
		
		#get station location from first episode
		with open(show_dir[0],'r') as show:
			first = json.load(show)
		first_ep = first[0]
		sta_count_dict[station][0] = first_ep['ep_coords'][0]


		for show in show_dir:
			with open(show,'r') as in_show:
				show_data = json.load(in_show)
			for episode in show_data:

				#find token count, add to dict
				token_count = len(episode['content'].split())
				sta_count_dict[station][1] += token_count

				#find num of location mentions, add to dict
				total_locs = len(episode['locations'])
				sta_count_dict[station][2] += total_locs

				#update the percentage of tokens that are locs
				loc_percent = round(100 * (sta_count_dict[station][2]/sta_count_dict[station][1]),2)
				sta_count_dict[station][3] = loc_percent

				#find number of in-state locations
				in_state = len(episode['in_state'])
				sta_count_dict[station][4] += in_state

				#find % of locs in-state
				in_state_loc = round(100 * (sta_count_dict[station][4]/sta_count_dict[station][2]),2)
				sta_count_dict[station][5] = in_state_loc

				#find % of tokens in-state locs
				in_state_tok = round(100 * (sta_count_dict[station][4]/sta_count_dict[station][1]),2)
				sta_count_dict[station][6] = in_state_tok

				#find number of out-of-state locations
				out_state = len(episode['out_state'])
				sta_count_dict[station][7] += out_state

				#find % of locs out-of-state
				out_state_loc = round(100 * (sta_count_dict[station][7]/sta_count_dict[station][2]),2)
				sta_count_dict[station][8] = out_state_loc

				#find % of tokens out-of-state locs
				out_state_tok = round(100 * (sta_count_dict[station][7]/sta_count_dict[station][1]),2)
				sta_count_dict[station][9] = out_state_tok

				#find number of in-country locations
				in_country = len(episode['in_country'])
				sta_count_dict[station][10] += in_country

				#find % of locs in-country
				in_country_loc = round(100 * (sta_count_dict[station][10]/sta_count_dict[station][2]),2)
				sta_count_dict[station][11] = in_country_loc

				#find % of tokens in-country locs
				in_country_tok = round(100 * (sta_count_dict[station][10]/sta_count_dict[station][1]),2)
				sta_count_dict[station][12] = in_country_tok

				#find number of out-of-country locations
				out_country = len(episode['out_country'])
				sta_count_dict[station][13] += out_country

				#find % of locs out-of-country
				out_country_loc = round(100 * (sta_count_dict[station][13]/sta_count_dict[station][2]),2)
				sta_count_dict[station][14] = out_country_loc

				#find % of tokens out-of-country locs
				out_country_tok = round(100 * (sta_count_dict[station][13]/sta_count_dict[station][1]),2)
				sta_count_dict[station][15] = out_country_tok


	df = pd.DataFrame.from_dict(sta_count_dict, 
			orient='index',
			columns=['Station Location','Token Count','Location Count','Location %','In State','In State % Loc','In State % Tok','Out of State','Out of State % Loc','Out of State % Tok','In US','In US % Loc','In US % Tok','Out of US','Out of US % Loc','Out of US % Tok'])
	
	return df

def main():

	direct = 'data'
	df = counts_by_station(direct)

	df.to_csv('all_station_counts.csv')

main()
