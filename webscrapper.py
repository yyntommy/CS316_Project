#Scraped from www.roomies.com. publicly available website.

import requests
from bs4 import BeautifulSoup

URLS = []
starting = "https://www.roomies.com/profiles/"
c = 500000
counter = 500
text_data = []

while (counter != 0):
    x_str = str(c)
    new_starting = starting + x_str
    page = requests.get(new_starting)
    soup = BeautifulSoup(page.content, 'html.parser')
    mydivs = soup.body.div.findAll({'class':'markdown text-gray-darkest'})
    text = ''
    for x in mydivs:
        text = x.find('p').text

    text_data.append(text)
    c = c + 1
    counter = counter - 1
    #print(x_str)

with open('roommate_blog.txt', 'w') as filehandle:
    for item in text_data:
        filehandle.write('%s\n' % item)
