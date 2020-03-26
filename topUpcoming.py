#! /usr/bin/python3

import json, requests, pprint
from jikanpy import Jikan
jikan = Jikan()
titles = ''

top_anime = jikan.top(type='anime', page=1, subtype='upcoming')

for key,value  in top_anime.items():
     if key ==  'top':
        animes_data = value


def jsonToMenu():
    title = ''
    rank = ''
    start_date = ''
    for data in animes_data:
        for key, value in data:

            if key == 'rank':
                rank = value
            if key == 'title':
                title = value
            if key == 'start_date':
                start_date = value

def mainMenu():
    print("Hello. Please select 1 to view upcoming anime.")
    try:
        menu_option = int(input())

    except ValueError:
        try:
            float(num)
            print('Input is a float. Please select a menu option.')

        except ValueError:
            print('That was not a number. Please enter a valid number')



# pprint.pprint(titles)

