#! /usr/bin/python3

import json, requests, pprint, os, time, math, webbrowser, re, pyautogui
from jikanpy import Jikan
from random import randint
jikan = Jikan()

def jsonToGenreMenu(genre_id):

    genre_id = int(genre_id)
    try:
        # Grabbing the top upcoming anime from the MAL API
        anime_genre = jikan.genre(type='anime', genre_id=genre_id)
        return anime_genre

    except ConnectionError:
        print('Could not connect to the MAL API at: https://api.jikan.moe/v3')

    except ValueError:
        print('Expected an integer between one and two digits')

    # pprint.pprint(anime_genre)

# Loops through the retrieved Json values and pulls the 'top' dictionary item from the dictionary which contains a list of animes as it's value
def jsonToUpcomingMenu():
    try:
        # Grabbing the top upcoming anime from the MAL API
        top_anime = jikan.top(type='anime', page=1, subtype='upcoming')

    except ConnectionError:
        print('Could not connect to the MAL API at: https://api.jikan.moe/v3')

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
def mainMenu():
    main_loop = True
    while main_loop:
        #Clear terminal command for Windows, Unix and MAC
        os.system('cls' if os.name == 'nt' else 'clear')
        print('[1]View Top Upcoming Anime.'.center(20) + '\n ' )
        print('[2]Select Random Anime To Watch.'.center(20) + '\n ' )
#If the user's input isn't an integer then it raises an exception
        menu_option = input('->')
        try:
            if int(menu_option) == 1:

                titles, ranks, start_dates = jsonToUpcomingMenu()
                upcomingMenu(titles, ranks, start_dates)
                main_loop = False
            elif int(menu_option) == 2:
                randMenu()
                main_loop = False

            else:
                time.sleep(1)
                print('**************Invalid selection**************')
                time.sleep(1)
                continue

        except ValueError:
            print('**************Invalid selection**************')
            time.sleep(.2)
            print('ValueError')
            print("Please enter a valid option...")
            time.sleep(2)

def randMenu():
    print('How would you like to randomly select an anime?')
    print('[1] Genre')
    print('\n' + '\n' + "Press 'B' to go back")
    user_input = input('->')

    try:
        if int(user_input()) == 1:
            genreMenu()
    elif user_input.upper = 'B':
        mainMenu()

    except ValueError:
        print('**************Invalid selection**************')
        time.sleep(1)
        print('Input a valid selection')

# Selects one of the upcoming anime titles
def upcomingTitleSelect(titles, ranks, user_input):
    # Searches for the selected title on reddit using our search token
    def redditSearch(search_token):
        search_link = f'https://www.reddit.com/r/anime/search/?q={search_token}&restrict_sr=1'
        try:
            webbrowser.open(search_link)

        except ConnectionError:
            print(f'Could not connect to destination: {search_link}' )

# Searches for the selected title on Youtube using our search token
    def youtubeSearch(search_token):
        search_link = f'https://www.youtube.com/results?search_query={search_token}'
        try:
            webbrowser.open_new_tab(search_link)

        except ConnectionError:
            print(f'Could not connect to destination: {search_link}' )


# Searches for the selected title on Wikipedia using our search token
    def wikipediaSearch(search_token):
        search_link = f'https://en.wikipedia.org/wiki/{search_token}'
        try:
            webbrowser.open_new_tab(search_link)
        except ConnectionError:
            print(f'Could not connect to destination: {search_link}' )


    #Clear terminal command for Windows, Unix and MAC
    os.system('cls' if os.name == 'nt' else 'clear')

    search_loop = True
    while search_loop:
        for rank in ranks:
            # If user input is a digit
            if user_input.isdigit():
                # If the user input matches a value in our ranks
                # I'll have to come back to this as this should be limited to 10
                if int(user_input) == rank:
                    search_string = titles[rank-1]
                    # If there's white space in the string then we're going to join the string using '%20' as the delimeter
                    # Which is reddit's method of appending search string values
                    if ' ' in search_string:
                        search_array = search_string.split()
                        reddit_search_token = '%20'.join(search_array)
                        wikipedia_search_token = '_'.join(search_array)
                        youtube_search_token = '+'.join(search_array)

                        redditSearch(reddit_search_token)
                        wikipediaSearch(wikipedia_search_token)
                        youtubeSearch(youtube_search_token)

                        search_loop = False
                    else:
                        redditSearch(search_string)
                        wikipediaSearch(search_string)
                        youtubeSearch(search_string)
                        search_loop = False
                else:
                    continue
            # Go back if the user's selection is 'B'
            elif str(user_input).upper() == 'B':
                        mainMenu()

            else:
                continue

        search_loop = False
        time.sleep(1)
        print('**************Invalid selection**************')
        time.sleep(5)
        upcomingMenu(titles, ranks, start_dates)

def genreMenu():

    genre_dict = {'1': 'Action', '2':'Adventure', '3':'Cars', '4':'Comedy', '5':'Dementia', '6':'Demons', '7': 'Mystery', '8':'Drama', '9':'Ecchi',
        '10':'Fantasy', '11':'Game', '12':'Hentai', '13':'Historical', '14':'Horror', '15':'Kids', '16':'Magic', '17':'Martial Arts',
        '18':'Mecha', '19':'Music', '20':'Parody', '21':'Samurai', '22':'Romance', '23': 'School', '24':'Sci Fi', '25': 'Shoujo',
        '26':'Shoujo Ai', '27':'Shounen', '28':'Shounen Ai', '29': 'Space', '30':'Sports', '31':'Super Power', '32':'Vampire', '33':'Yaoi',
        '34':'Yuri', '35':'Harem', '36':'Slice Of Life', '37':'Supernatural', '38':'Military', '39':'Police', '40':'Psychological', '41':'Thriller',
        '42':'Seinen', '43':'Josei'}
    def genrePrintMenu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Genres to choose from include:')
        for number, genre in genre_dict.items():
            print(f'[{number}]:-> {genre}')

    def chooseGenre():

        genre_loop = True
        while genre_loop:
    #Clear screen
            # os.system('cls' if os.name == 'nt' else 'clear')
            user_input = input('->')
            for number, genre in genre_dict.items():
                try:
                    if user_input == number:
                        genre_json= jsonToGenreMenu(user_input)
                        return genre_json
                        genre_loop = False

                    else:
                        continue
                except ValueError:
                    print('ValueError: Please pick an Integer value from the list above')
                    time.sleep(1)
                    print('**************Invalid selection**************')
                    time.sleep(1)
                    genrePrintMenu()
            genre_loop = False

    def findGenre(genre_dict):
        genre_list = genre_dict.get('anime')

        rand_select_loop = True

        while rand_select_loop:
            os.system('cls' if os.name == 'nt' else 'clear')
            random_selection = randint(0, len(genre_list))
            random_show = genre_list[random_selection]
            distinct_random_show = dict((key, random_show[key]) for key in  ['title', 'synopsis', 'score', 'url']
                                                                                if key in random_show)
            pprint.pprint(distinct_random_show)
            print('Search for this title?[Y/N]')
            user_input = input('->')
            if user_input.upper() == 'Y':
                print('Running search')
                rand_select_loop = False
            elif user_input.upper() == 'N':
                continue


    genrePrintMenu()
    genre_json = chooseGenre()
    findGenre(genre_json)

def upcomingMenu(titles, ranks, start_dates):
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
    upcomingTitleSelect(titles, ranks, user_input)



def main() :

    mainMenu()





main()
