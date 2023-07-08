#!/usr/bin/python3

import urllib, requests, bs4, sys

# COLORS
colors = {}
colors['reset'] = '\033[0m'
colors['black'] = '\033[30m'
colors['red'] = '\033[31m'
colors['green'] = '\033[32m'
colors['orange'] = '\033[33m'
colors['purple'] = '\033[35m'
colors['cyan'] = '\033[36m'
colors['blue'] = '\033[34m'
colors['pink'] = '\033[95m'
colors['yellow'] = '\033[93m'

def printC(color, text):
    print(color + '{}\033[00m'.format(text))


# DISPLAY POST
def displayPost(index, subreddit, title, href, upvotes):
    print(str(index) + '\t/r/' + subreddit)
    printC(colors['cyan'], title)
    printC(colors['yellow'], href)
    print('↑ ' + upvotes + ' ↓')
    #printC(colors['red'], '↑ ' + upvotes + ' ↓')


# REQUEST
url = 'https://old.reddit.com/r/' + sys.argv[1]

page = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/91.0.2'})
infile = urllib.request.urlopen(page).read()
#data = infile.decode('ISO-8859-1')
soup = bs4.BeautifulSoup(infile, "html.parser")

soup = soup.find('div', class_='content')
siteTable = soup.find(id='siteTable')
tableContent = list(siteTable.children)
content = []

# TODO: produce html

# collect content
for i in range(0, len(tableContent)):
    elem = tableContent[i]
    if elem['class'][0] == 'clearleft':
        pass
    else:
        isAd = elem.find(class_='promoted-tag')
        if isAd == None:
            content.append(elem)

index = 1
for elem in content:
    title = elem.find('p', class_='title')
    if title != None:
        title = title.find('a')
        href = title['href']
        if href[0] == '/':
            href = 'https://www.reddit.com' + href
        upvotes = elem.find('div', class_='midcol unvoted')
        upvotes = upvotes.find('div', class_='score unvoted')

        displayPost(index, sys.argv[1], title.text, href, upvotes.text)
        index += 1
        print()
        print()
