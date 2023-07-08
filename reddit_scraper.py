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

# DISPLAY
def displaySubreddit(subreddit, content):
    index = 1
    banner = f'==================================== r/{subreddit} ===================================='
    printC(colors['purple'], banner)
    print()

    for elem in content:
        title = elem.find('p', class_='title')
        link = elem.find('li', class_='first')
        if link == None or title == None:
            pass
        else:
            title = title.find('a')
            href = title['href']
            if href[0] == '/':
                href = 'https://www.reddit.com' + href
            upvotes = elem.find('div', class_='midcol unvoted')
            upvotes = upvotes.find('div', class_='score unvoted')

            displayPost(index, subreddit, title.text, href, link.a['href'], upvotes.text, link.a.text)
            index += 1


def displayPost(index, subreddit, title, href, reddit_link, upvotes, comments):
    divider = '--------- ' + str(index) + '    /r/' + subreddit + ' ---------'
    print(divider)
    printC(colors['cyan'], title)
    print()
    printC(colors['yellow'], href)
    printC(colors['orange'], reddit_link)
    print('↑ ' + upvotes + ' ↓\t\t\t' + comments)
    print(len(divider) * '-')
    print('\n')


# REQUEST
def makeRequest(url):
    page = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/91.0.2'})
    infile = urllib.request.urlopen(page).read()
    soup = bs4.BeautifulSoup(infile, "html.parser")
    return soup 

# PARSE SUBREDDIT
def parseSubreddit(subreddit):
    url = 'https://old.reddit.com/r/' + subreddit
    soup = makeRequest(url)
    soup = soup.find('div', class_='content')
    siteTable = soup.find(id='siteTable')
    tableContent = list(siteTable.children)
    content = collectContent(tableContent)
    return content


def collectContent(tableContent):
    content = []
    for i in range(0, len(tableContent)):
        elem = tableContent[i]
        if elem['class'][0] == 'clearleft':
            pass
        else:
            isAd = elem.find(class_='promoted-tag')
            if isAd == None:
                content.append(elem)

    return content

subreddits = sys.argv[1:]
for subreddit in subreddits:
    content = parseSubreddit(subreddit)
    displaySubreddit(subreddit, content)
