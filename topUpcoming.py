#! /usr/bin/python3

import json, requests, pprint, os, time, math
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

    while 1:
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
    upcomingMenuPrint(titles, ranks, start_dates)
def upcomingMenuPrint(titles, ranks, start_dates):
# assigns the max length of the columns for each value
    max_length_titles = max(titles, key = len)
    max_length_ranks = 2
    max_length_start_dates = max(start_dates, key = len)

    max_titles_col_length = len(max_length_titles)
    max_ranks_col_length = max_length_ranks
    max_start_dates_col_length = len(max_length_start_dates)

    if int(max_titles_col_length) % 2 != 0 :
        max_titles_col_length = max_titles_col_length + 1

    if int(max_start_dates_col_length) % 2  != 0 :
        max_start_dates_col_length = max_start_dates_col_length + 1

    max_titles_col_length = max_titles_col_length + 2
    max_ranks_col_length = max_ranks_col_length + 2
    max_start_dates_col_length = max_start_dates_col_length + 2


    print('Rank'.ljust(max_ranks_col_length, '-')  + 'Title'.center(max_titles_col_length, ' ') + '\t'+ 'Start Date'.rjust(max_start_dates_col_length, ' ') + '\n')

    for count in range(0,10):

        title_justify = int(max_titles_col_length -len(titles[count])/2)
        ranks_justify = 8
        title_justify = title_justify+ranks_justify
        start_dates_justify = int(max_start_dates_col_length -len(start_dates[count])/2)
        start_dates_justify = (max_titles_col_length - title_justify) + start_dates_justify
        # titles_col_width = (max_length_titles - len(titles[count])) + 1
        # titles_col_width = (max_length_ranks - len(ranks[count])) + 1
        # titles_col_width = (max_length_start_dates - len(start_dates[count])) + 1
        print(str(ranks[count]).center(ranks_justify, ' ') + '''[''' + str(titles[count]).center(title_justify, '+') + ''']'''  + str(start_dates[count]).rjust(start_dates_justify, ' ') + '\n')


    # return len(max_length)


# Grabbing the top upcoming anime from the MAL API
try:

    top_anime = jikan.top(type='anime', page=1, subtype='upcoming')

except ConnectionError:
    print('Could not connect to the MAL API.')



titles, ranks, start_dates = jsonToMenu()
print(start_dates)
mainMenu(titles, ranks, start_dates)
