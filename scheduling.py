#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import csv

from matplotlib import pyplot as plt

sns.set()

df = pd.read_csv(".\\twitch_data_time.tsv", sep='\t', quoting=csv.QUOTE_NONE)

df['datetime'] = pd.to_datetime(df['time_created'], format='%Y-%m-%dT%H:%M:%SZ')
#df['week'] = df['datetime'].dt.to_period('W')

def streams_views_hourly(df, language=None):
    pd.options.mode.chained_assignment = None
    if language is not None:
        print('Filtering with language tag: ' + language)
        df = df[df['broadcaster_language'] == language]
    df['hour'] = df['datetime'].dt.hour
    pd.options.mode.chained_assignment = 'warn'
    ax = df.groupby('hour')['current_views'].mean().plot(kind='bar',width=1,title='Times of Streams' ,figsize=(20,10))
    ax.set(xlabel='Hour of Day',ylabel='Views (Mean)')
    plt.show()

languages = (df['broadcaster_language'].value_counts().to_dict())

def menu(): 
    print("Please choose an option.")
    print("1) Show stream views by hour.")
    print("2) Show streams views by hour, filtered by language.")
    print("3) Show language tags.")

    option = int(input())

    if (option == 1):
        streams_views_hourly(df)
    elif (option == 2):
        valid = False
        while not valid:
            print("Please enter the language tag you wish to filter by: ", end=" ")
            language = str(input()).lower()
            if language in languages:
                valid = True
        streams_views_hourly(df, language)
    elif (option == 3):
        print('Language : # of Channels')
        for language in languages:
            print(language + '\t : ' + str(languages[language]))
						
if __name__ == "__main__":
    menu()
