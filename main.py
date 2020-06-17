#! /usr/bin/python3

import json, requests, pprint, os, time, math, webbrowser, re, urllib.request, pyperclip, pymongo, urllib3
from pymongo import MongoClient
from tkinter import *
from jikanpy import Jikan
from random import randint
jikan = Jikan()



# Function to clear the terminal
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Makes a request to the webpage and then returns the request code
def pingSite(search_url):

    print(urllib.request.urlopen(search_url).getcode())
    code = urllib.request.urlopen(search_url).getcode()
    return code


#Function to search for an anime to stream
def animeSearch(search_string):


    # Function which  uses the request code and the search values to execute a search on gogoanime and to run a backup search if the main search fails
    def gogoAnimeSearch(res, search_alt, search_url):

        if res == 200:
            webbrowser.open(search_url)

        else:
            try:
                webbrowser.open(f'https://www.gogoanime.io//search.html?keyword={search_alt}')

            except HTTPError as error:
                print('Unable to locate that title on a free streaming platform')

    #if there's a space in the search string, split and rejoin it using the hyphen which is gogoanime's delimeter for more than one value
    if ' ' in search_string:
        search_array = search_string.split()
        gogoanime_search_token = '-'.join(search_array)
        search_url = f'https://www.gogoanime.io/category/{gogoanime_search_token}'
        response = pingSite(search_url)
        search_alt = search_array[0]
        gogoAnimeSearch(response, search_alt, search_url)

    else:
        search_url = f'https://www.gogoanime.io/category/{search_string}'
        response = pingSite(search_url)
        search_alt = search_array[0]
        gogoAnimeSearch(response, search_alt, search_url)

#Checks the user's input and confirms that it matches a value stored in the API request and pulls the corresponding genre's json data
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
    
   
def jsonToCollectionMenu(series_name):
    try:
        search_json = jikan.search('anime', series_name, parameters={'type': 'tv'})
        for key,value in search_json.items():
            if key == 'results':
                results = value
                result = results[0]

        for key,value in result.items():
            if key == 'episodes':
                if value == 0:
                    print('This seems to be an ongoing series')

                else:
                    return value

        
   
    except ConnectionError:
        print('Could not connect to the MAL API at: https://api.jikan.moe/v3')


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
# Some values arrived as NoneTypes so this is there to remedy that
                for date in range(0,len(start_dates)):
                    if start_dates[date] is None:
                        start_dates[date] = '-'
#returns titles, ranks, and start dates
    return titles, ranks, start_dates

#Initates the main menu
def mainMenu():
    def viewTopUpcoming():
        titles, ranks, start_dates = jsonToUpcomingMenu()
        upcomingMenu(titles, ranks, start_dates)
#Selects the menu to direct the user towards based on their input. It will return an error message if the choice is erroneous
    def menuSelect(input):
        menu = {
            1: viewTopUpcoming,
            2: randMenu,
            3: completedMenu
        }
        try:
            func=menu.get(int(input), 'Invalid Selection')
            return func()
        # except ValueError as error:
        #     print(error)
        #     print('wrong')
        #     return False
        except TypeError as error:
            print(error)
            return False

    main_loop = True
    while main_loop:
        clearScreen()
        print('[1]View Top Upcoming Anime.'.center(20) + '\n ' )
        print('[2]Select Random Anime To Watch.'.center(20) + '\n ' )
        print('[3]Collection')
        menu_option = input('->')
        menuSelect(menu_option)
       
        if menuSelect == False:
            continue
        time.sleep(2)
       
        

 

def completedMenu():

    def viewSeries():
        print('Completed view')


# Create connection to our local mongoDB
    def dbConnect():
        # Add fail safe to skip over this try catch if the connection is already in place
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["Anime_DB"]
            collection = db["completed"] 
            return db, collection

        except ConnectionError as error:
            print(error)
#Add a series to our list of completed series 
    def addSeries(series_name):
        db, collection = dbConnect()
        if collection.find_one({'title': series_name}) != None:
            print('You have already added this item to your collection')
            time.sleep(3)
            addSeriesMenu()
        else:
            series = {'title': series_name}
            db_addition = collection.insert_one(series)
            print('Inserting value: ' + str(db_addition))

    def viewSeries():

        clearScreen()
        db, collection = dbConnect()
        #Print the titles of the series in our completed collection. Exclude the id.
        for series in collection.find():
            print('-' + series['title'] + '\n')
        print('\n' + '\n' + 'Choose one of the series above (input series name), I will then randomly select an episode.')
        print('\n' + 'Press [B] to go back')
        user_input = input('->')
        selectRandEpisode(user_input.lower())

    def selectRandEpisode(user_input):

        def gogoAnimeSearch(res, search_url):
            try:
             if res == 200:
                webbrowser.open(search_url)


            except HTTPError as error:
                print('Unable to locate that title on a free streaming platform')



        total_episodes = jsonToCollectionMenu(user_input)
        print(total_episodes)
        episode_number = randint(1,total_episodes)
        if ' ' in  user_input:
            search_array = user_input.split()
            gogoanime_search_token = '-'.join(search_array)
            search_url = f'https://www.gogoanime.io/{gogoanime_search_token}-episode-{episode_number}'
            response = pingSite(search_url)
            gogoAnimeSearch(response, search_url)
        
        else:
            gogoanime_search_token = user_input
            search_url = f'https://www.gogoanime.io/{gogoanime_search_token}-episode-{episode_number}'
            response = pingSite(search_url)
            gogoAnimeSearch(response, search_url)
        



    def addSeriesMenu():
        clearScreen()
        add_series_menu_loop = True
        while add_series_menu_loop:
            clearScreen()
            user_input = input(f'Please enter a series name to add to your "Watched List": ')

            if user_input.upper() == 'B':
                completedMenu()
                add_series_loop = False
            else:
                clearScreen()
                print(f'You have entered "{user_input}" to add to your collection. Is this correct?')
                selection = input('[Y][N]->')

                try:
                    if selection.upper() == 'Y':
                        # Put this value into a dictionary so that it can be used by MongoDB
                        addSeries(user_input)
                        add_series_menu_loop = False

                    elif user_input == 'N':
                        continue
                    else:
                        print('**************Invalid selection**************')
                except ValueError as error:
                    print('**************Invalid selection**************')
                    time.sleep(.2)
                    print(error)
                    time.sleep(2)



    completed_menu_loop = True
    while completed_menu_loop:
        clearScreen()
        print('[1]View Completed Series\n')
        print('[2]Add to Completed Series\n')
        print('Press [B] to go back')

        user_input = input('->')
        try:
            if int(user_input) == 1:
                viewSeries()
                completed_menu_loop = False

            elif int(user_input) == 2:
                addSeriesMenu()
                completed_menu_loop = False


            elif user_input.upper() == 'B':
                mainMenu()
                completed_menu_loop = False

        except ValueError as error:
            if user_input.upper() == 'B':
                mainMenu()
                completed_menu_loop = False
            else:
                print('**************Invalid selection**************')
                time.sleep(.2)
                print(error)
                time.sleep(2)

#Menu used to randomly select a show
def randMenu():
    def menuSelect(input):
        menu = {
            1: genreMenu
            
        }
        if input.upper() == 'B':
            mainMenu()
        else:
            try:
                func=menu.get(int(input), 'Invalid Selection')
                return func()
            except ValueError as error:
                print(error)
                return False
            except TypeError as error:
                print(error)
                return False

    rand_menu_loop = True

    while rand_menu_loop:
        clearScreen()
        print('**************Randomly Select a Title**************' + '\n')
        print('How would you like to randomly select an anime?')
        print('[1] Genre')
        print('\n' + '\n' + "Press [B] to go back")
        user_input = input('->')
        menuSelect(user_input)
        if menuSelect == False:
            continue


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
    search_loop = True
    while search_loop:

            # Go back to main menu
           

        try:
            for rank in ranks:
              if int(user_input) == rank:
                search_string = titles[rank-1]
                  # If there's white space in the string then we're going to join the string using '%20' as the delimeter
                    # Which is reddit's method of appending search string values
                if ' ' in search_string:
                    search_array = search_string.split()
                    reddit_search_token = '%20'.join(search_array)
                    wikipedia_search_token = '_'.join(search_array)
                    youtube_search_token = '+'.join(search_array)
                        # Run three different searches for reddit, wikepedia, and Youtube. Absolutely overkill, but fuck it
                    redditSearch(reddit_search_token)
                    wikipediaSearch(wikipedia_search_token)
                    youtubeSearch(youtube_search_token)
                    print(f'searching for: {search_string}')
                    search_loop = False

                else:
                    redditSearch(search_string)
                        
                    wikipediaSearch(search_string)
                    youtubeSearch(search_string)
                    print(f'searching for: {search_string}')
                    search_loop = False

                
                    
        except ValueError:
            if str(user_input).upper() == 'B':
                mainMenu()
                search_loop = False
            else:
                time.sleep(1)
                print('**************Invalid selection**************')
                time.sleep(5)
                    # upcomingMenu(titles, ranks, user_input)

# Function to generate the genre menu
def genreMenu():

    #Genres and their types
    genre_dict = {'1': 'Action', '2':'Adventure', '3':'Cars', '4':'Comedy', '5':'Dementia', '6':'Demons', '7': 'Mystery', '8':'Drama', '9':'Ecchi',
        '10':'Fantasy', '11':'Game', '12':'Hentai', '13':'Historical', '14':'Horror', '15':'Kids', '16':'Magic', '17':'Martial Arts',
        '18':'Mecha', '19':'Music', '20':'Parody', '21':'Samurai', '22':'Romance', '23': 'School', '24':'Sci Fi', '25': 'Shoujo',
        '26':'Shoujo Ai', '27':'Shounen', '28':'Shounen Ai', '29': 'Space', '30':'Sports', '31':'Super Power', '32':'Vampire', '33':'Yaoi',
        '34':'Yuri', '35':'Harem', '36':'Slice Of Life', '37':'Supernatural', '38':'Military', '39':'Police', '40':'Psychological', '41':'Thriller',
        '42':'Seinen', '43':'Josei'}

    # Prints the genre menu
    def printGenreMenu():
        clearScreen()
        print('Genres to choose from include:')
        #Loops through the values of the genre dictionary and displays them for the user to see
        for number, genre in genre_dict.items():
            print(f'[{number}]:-> {genre}')

        print("\n Press [B] to go back...")

    #Genre Selection
    def chooseGenre():

        genre_loop = True

        while genre_loop:
            user_input = input('->')

            #Loops through the genre dictionary for a match in the user's selection
            for number, genre in genre_dict.items():
                try:
                #Return the JSON data of the anime genre
                    if user_input == number:
                        #jsonToGenreMenu ensures that the user's selection is a valid option in the JSON genre option
                        genre_json= jsonToGenreMenu(user_input)
                        return genre_json
                        genre_loop = False

                    elif user_input.upper() == 'B':
                        randMenu()

                    else:
                        continue
                except ValueError:
                    print('ValueError: Please pick an Integer value from the list above or  press B to return')
                    time.sleep(1)
                    print('**************Invalid selection**************')
                    time.sleep(1)
                    printGenreMenu()
                    continue


    def findGenre(genre_d):

        rand_select_loop = True
        while rand_select_loop:

            clearScreen()
            #creates a list of elements made up of the anime genre
            genre_list = genre_d.get('anime', 'none')
            #Randomly generates a number using the number of shows given
            random_selection = randint(0, len(genre_list))
            #Randomly selects a show using the random number
            random_show = genre_list[random_selection]
            #Limit the keys and values that will be diplayed on the screen from the returned show
            distinct_random_show = dict((key, random_show[key]) for key in  ['title', 'type', 'url','image_url'] if key in random_show)

            pprint.pprint(distinct_random_show)
            print('\n Search for this title?[Y/N]')
            print('\n Press [B] to go back')
            user_input = input('->')
            try:
        #Get the title of the show and pass it to the function to search/stream it
                if user_input.upper() == 'Y':
                    search_string = distinct_random_show.get('title', 'none')
                    response = animeSearch(search_string)

                # If we get a good response, proceed to the site
                    if response == 200:
                        try:
                            webbrowser.Open(search_string)
                            rand_select_loop = False

                        except:
                            print('Sorry for the inconvenience. I am unable to complete your query at this time')
                        
                elif user_input.upper() == 'N':
                    continue

                elif user_input.upper() == 'B':
                    rand_select_loop = False
                    printGenreMenu()


            except ValueError:
                print('Please enter a valid value')
                continue

            except urllib.error.HTTPError as exception:
                print(exception)
                #Copy the search string to the clipboard
                user_copy = pyperclip.copy(search_string)
                time.sleep(1)
                print('Title was not located on gogoanime....\n')
                time.sleep(1)
                print('Alternatively you can search for this title manually. It has been copied to the clipboard\n')
                time.sleep(3)
                continue

    printGenreMenu()
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
    print("Press [B] to go back...")
    user_input = input()
    upcomingTitleSelect(titles, ranks, user_input)



def main() :

    mainMenu()





main()