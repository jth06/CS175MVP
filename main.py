#!/usr/bin/env python3
import sys
import os

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
        print("2: See reccommendations")
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
            print(userDict)
    
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
        # print("Hello")
        # print(userDict)
        for key, value in userDict.items():
            print(key, file=userFile, end=" ")
            # print(key, end=" ")
            for val in value:
                print(val, file=userFile, end=" ")
                # print(val, end=" ")
            print(file=userFile)


if __name__ == "__main__":
    main()