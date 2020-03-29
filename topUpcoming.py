#! /usr/bin/python3

import json, requests, pprint, os, time, math, webbrowser, re
from jikanpy import Jikan
jikan = Jikan()


# Loops through the retrieved Json values and pulls the 'top' dictionary item from the dictionary which contains a list of animes as it's value
def jsonToMenu():
    titles = []
    ranks = []
    start_dates = []
    for key,value  in top_anime.items():
         if key ==  'top':
            animes_data = value

# Loops through thelist items in the anime data list within
    for data in animes_data:
        for key, value in data.items():

# If the key matches the values that we want (rank, title, start_dates) then we'll grab those values
            if key == 'rank':
                ranks.append(value)
            elif key == 'title':
                titles.append(value)
            elif key == 'start_date':
                start_dates.append(value)

                for date in range(0,len(start_dates)):
                    if start_dates[date] is None:
                        start_dates[date] = '-'
#returns titles, ranks, and start dates
    return titles, ranks, start_dates

#Initates the main menu
def mainMenu(titles, ranks, start_dates):

    while True:
        #Clear terminal command for Windows, Unix and MAC
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Hello. Please select 1 to view upcoming anime.\n \n" )
#If the user's input isn't an integer then it raises an exception
        try:
            menu_option = int(input())
            break
        except ValueError:
            print("Error")
            time.sleep(1)
            print("Please enter a digit...")
            time.sleep(2)

    time.sleep(1)
    user_input = upcomingMenuPrint(titles, ranks, start_dates)
    return user_input

# Selects one of the upcoming anime titles
def titleSelect(titles, ranks, user_input):
    # Searches for the selected title on reddit using our search token
    def redditSearch(search_token):
        search_link = f'https://www.reddit.com/r/anime/search/?q={search_token}&restrict_sr=1'
        try:
            webbrowser.open(search_link)

        except ConnectionError:
            print(f'Could not connect to destination: {search_link}' )

    #Clear terminal command for Windows, Unix and MAC
    os.system('cls' if os.name == 'nt' else 'clear')


    while True:
        for rank in ranks:
            # If user input is a digit
            if user_input.isdigit():
                # If the user input matches a value in our ranks
                # I'll have to come back to this as this should be limited to 10
                if int(user_input) == rank:
                    search_string = titles[rank-1]
                    # If there's white space in the string then we're going to join the string using '%20' as the delimeter
                    # WHich is reddit's method of appending search string values
                    if ' ' in search_string:
                        search_array = search_string.split()
                        search_token = '%20'.join(search_array)
                        redditSearch(search_token)
                        break
                    else:
                        redditSearch(search_string)
                        break
                else:
                    continue
            # Go back if the user's selection is 'B'
            elif str(user_input).upper() == 'B':
                        mainMenu(titles, ranks, start_dates)

            else:
                continue

        break
        time.sleep(1)
        print('**************Invalid selection**************')
        time.sleep(5)
        upcomingMenuPrint(titles, ranks, start_dates)

def upcomingMenuPrint(titles, ranks, start_dates):
# assigns the max width of the columns for each value
    max_length_titles = max(titles, key = len)
    max_length_ranks = 2
    max_length_start_dates = max(start_dates, key = len)

    max_titles_col_length = len(max_length_titles)
    max_ranks_col_length = max_length_ranks
    max_start_dates_col_length = len(max_length_start_dates)
# Column title fields
    print('Rank'.ljust(max_ranks_col_length, '-')  + 'Title'.center(max_titles_col_length, ' ') +  'Start Date'.rjust(max_start_dates_col_length, ' ') + '\n')

    for count in range(0,20):
# Prints the values of the top Upcoming anime
        print(str(ranks[count]).center(10, ' ') + '''[''' + str(titles[count]).center(70, '+') + ''']'''  + str(start_dates[count]).rjust(20, ' ') + '\n' + '\n')

    time.sleep(.2)
    print('Please input a rank number from the list for more information regarding a chosen title...')
    time.sleep(.2)
    print("Press 'B' to go back...")
    user_input = input()
    return user_input


# Grabbing the top upcoming anime from the MAL API
try:

    top_anime = jikan.top(type='anime', page=1, subtype='upcoming')

except ConnectionError:
    print('Could not connect to the MAL API.')



titles, ranks, start_dates = jsonToMenu()
user_input = mainMenu(titles, ranks, start_dates)
titleSelect(titles, ranks, user_input)
