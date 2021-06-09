#!/usr/bin/env python3
import sys
import os
import pandas as pd
import copy

def main():
    userFile = open("users.txt", 'r')
    line = None
    userDict = {}

    # populate userDict to get usernames and list of streamers they watch
    if not os.path.getsize("users.txt") == 0:
        for line in userFile:
            userDict[line.split()[0]] = []
            for i in line.split():
                if not (i == line.split()[0]):
                    userDict[line.split()[0]].append(i)
            userDict[line.split()[0]] = sorted(userDict[line.split()[0]])

    # Input username
    print("Please enter your name:", end=" ")
    userName = str(input())
    newUser = True

    # Checks if the given username exists in our .txt file
    if(userName in userDict):
        newUser = False
    option = None

    # Case for a returning user
    if(not newUser):
        print("Welcome back", end=" ")
        print(userName)
        print("What would you like to do today?")
        print("1: Add more streamers")
        print("2: See recommendations")
        option = int(input())
        
        if(option == 1):
            print("Add the streamers you would like to add below:")
            streamLine = str(input()).lower()
            streamList = streamLine.split()
            userStreamerList = userDict[userName]
            set_1 = set(streamList)
            set_2 = set(userStreamerList)

            list2_items_not_in_list1 = list(set_2- set_1)
            combined_list = streamList + list2_items_not_in_list1
            # print(combined_list)
            userDict[userName] = sorted(combined_list)
            # print(userDict)
        elif(option == 2):
            # print("Based on the streamers you watch, here are some other streamers we think you would enjoy:")
            streamerDF = pd.read_csv('twitch_data.tsv', sep='\t')
            # dict1 = dict(zip(streamerDF['game_name'], streamerDF['broadcaster_name']))
            # g = streamerDF.groupby('game_name')
            # print(g)
            # g['broadcaster_name'].tolist()
            # dict1 = g['broadcaster_name'].to_list().to_dict()
            dict1 = streamerDF.groupby('game_name')['broadcaster_name'].apply(list).to_dict()
            # print(dict1)
            streamerDict = {}
            # print(dict1)
            for i in dict1.keys():
                sdKeys = list(streamerDict.keys())
                # print(sdKeys)
                # print(i)
                if not str(i) in streamerDict:
                    streamerDict[str(i)] = []
                    streamerDict[str(i)].append(dict1[i])
                else:
                    # print(i)
                    if not dict1[i] in streamerDict[str(i)]:
                        streamerDict[str(i)].append(dict1[i])

            # for i in streamerDict:
            #     res = []
            #     for j in streamerDict[i]:
            #         if j not in res:
            #             print(j)
            #             res.append(j)
            #     streamerDict[i] = res
            # print(streamerDict)
            strmrInDF = userDict[userName].copy()
            currUserSDict = {}
            # print(userDict[userName])
            for strmr in userDict[userName]:

                # print(type(streamerDF['broadcaster_name']))
                # print(streamerDF.broadcaster_name)
                # print(strmr, end=" in outer for loop\n")
                InDS = False
                isInDS = streamerDF.broadcaster_name.isin([strmr])
                for index, value in isInDS.items():
                    if value:
                        InDS = True
                        break

                # print(type(streamerDF.broadcaster_name))
                if InDS:
                    # print(type(streamerDF['broadcaster_name']))
                    # print(strmr, end=' in InDS\n')
                    strmrRow = streamerDF.loc[streamerDF['broadcaster_name'] == strmr]
                    strmrGame = strmrRow['game_name'].array
                    # print(strmrGame)
                    # print
                    if strmrGame[0] in currUserSDict:
                        currUserSDict[strmrGame[0]].append(strmr)
                    else:
                        currUserSDict[strmrGame[0]] = []
                        currUserSDict[strmrGame[0]].append(strmr)
                else:
                    # print(strmr, end=" being removed\n")
                    strmrInDF.remove(strmr)
            
            mostPopGames = {}
            # print(currUserSDict)
            for gameKey in currUserSDict:
                # mostPopGames[len(currUserSDict[gameKey])/len(strmrInDF)] = gameKey
                mostPopGames[gameKey] = len(currUserSDict[gameKey])/len(strmrInDF)

            userMWGames = list(mostPopGames.values())
            # print(userMWGames)
            # userMWGames = userMWGames.sort(reverse=True)
            userMWGames.sort(reverse=True)
            # print(mostPopGames)
            # print(userMWGames)
            mpGames = []
            for mwGame in userMWGames:
                mpgKeys = list(mostPopGames.keys())
                for i in mpgKeys:
                    # print(i)
                    # print(mwGame)
                    if mostPopGames[i] == mwGame:
                        mpGames.append(i)
                        # break
            iterNum = 0
            for gameKey in mpGames:
                if len(userMWGames) == iterNum:
                    break
                # print("Since you watch", end=" ")
                print("Since", end=" ")
                print(userMWGames[iterNum], end=" ")
                print("of the streamers you watch, such as", end=" ")
                for strmr in currUserSDict[gameKey]:
                    print(strmr, end=", ")
                print("play", end=" ")
                print(gameKey, end=" ")
                print("we recommend that you check out these streamers:")
                for strmr in streamerDict[gameKey]:
                    # print(streamerDict[gameKey])
                    iterNum2 = 0
                    for i in strmr:
                        if iterNum2 >= 10:
                            break
                        if not i in currUserSDict[gameKey]:
                            print(i, end=' ')
                        iterNum2 += 1
                print()
                iterNum += 1


            

            


    # Case where a new user has been entered
    else:
        print("Hello", end=" ")
        print(userName, end=". ")
        print("Please enter the steamers you watch, by their username:")
        streamLine = str(input()).lower()
        streamList = streamLine.split()
        userDict[userName] = sorted(streamList)
        print("Thank you, if you want to see your recommendations, rerun the program")

    # Write contents of userDict to .txt file
    userFile.close()
    userFile = open('users.txt', 'w')
    with open('users.txt', 'w') as userFile:
        for key, value in userDict.items():
            print(key, file=userFile, end=" ")
            for val in value:
                print(val, file=userFile, end=" ")
                # print(val, end=" ")
            print(file=userFile)


if __name__ == "__main__":
    main()