import pandas as pd
import csv
from os import listdir

path = ".\\Twitch_data"

#header = ['stream_ID', 'current_views', 'time_created', 'game_name', 'broadcaster_id', 'broadcaster_name', 'delay_setting', 'follower_number', 'partner_status', 'broadcaster_language', 'total_views', 'language', 'sign_up_time', 'bitrate', 'source_resolution']
header = ['current_views', 'time_created', 'game_name', 'broadcaster_id', 'broadcaster_name', 'delay_setting', 'follower_number', 'partner_status', 'broadcaster_language', 'total_views', 'language', 'sign_up_time', 'bitrate', 'source_resolution', 'empty']

dfs = []

for file in listdir(path):
    #print(file)
    df = pd.read_csv(path + "\\" + file, sep='\t', header=None, names=header, quoting=csv.QUOTE_NONE, index_col=None)
    df1 = df[['game_name', 'broadcaster_id', 'broadcaster_name', 'follower_number', 'broadcaster_language']]
    dfs.append(df1)

df_all = pd.concat(dfs, ignore_index=True)

df_all.to_csv('twitch_data.tsv',sep='\t')
