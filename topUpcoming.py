#! /usr/bin/python3

#Script to search internet for relevant information regarding MyAnimeLists'
#Top Upcoming Anime

import requests
from bs4 import BeautifulSoup
# Create Connection to webpage
webpage = requests.get('https://myanimelist.net/topanime.php?type=upcoming')
soup = BeautifulSoup(webpage.content, 'html.parser')
title_div = soup.find_all(class_='di-ib clearfix')

def collectTitles(divs):
    index = 0
    titles = []
    for div in divs:
        title = div.contents[0]
        titles.append(title)
        index+=1
        if index >= 10:
            break
        else:
            continue
    return titles

def titlesToText(title_tag):
    titles = []
    for title in title_tag:
        titles.append(title.get_text())
    return titles

def topUpcomingMenu(text_titles):
    index = 0
    for title in text_titles:
        menu_number = '[%s] ' % index
        index+=1
        print(menu_number + title)

titles = collectTitles(title_div)
text_titles = titlesToText(titles)
topUpcomingMenu(text_titles)
