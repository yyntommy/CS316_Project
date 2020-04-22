#Scraped from www.roomies.com. publicly available website.

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
from datetime import datetime
import random

URLS = []
starting = "https://www.roomies.com/profiles/"
c = 500000
counter = 500#number of pages you want to extract
text_data = []
post = "'"

while (counter != 0):
    x_str = str(c)
    new_starting = starting + x_str
    page = requests.get(new_starting)
    soup = BeautifulSoup(page.content, 'lxml')
    container = soup.find("div",attrs={'class': 'markdown text-gray-darkest'})
    if container is not None:
        for p in container.find_all('p'):
            if post in p.text:
                x = p.text
                pe = x.replace("'", '')
                text_data.append(pe)
            else:
                text_data.append(p.text)
        
    
    c = c + 1
    counter = counter - 1
    print(x_str)
    
df = pd.DataFrame(text_data)

# take the already inputted netids from the inputted load file in order to match netids to randomly generated blog posts extracted from www.roomies.com

def generate_random_date():
    start = datetime.today().replace(day=1, month=1).toordinal()
    end = datetime.today().toordinal()
    random_day = datetime.fromordinal(random.randint(start, end))
    dateStr = random_day.strftime("%d %b %Y")
    return dateStr


s = open('load1.sql', 'r').read()
s = s.replace('\n', '')
s = s.replace('insert into Users values ', '')
s = s.replace('insert into UserLikes values ', '')
s = s.replace('insert into UserMajor values ', '')
s_list = s.split(';')
netids = []
for x in s_list:
    x = x.replace('(', '')
    values = x.split(',')
    id = values[0]
    id = id.replace("'", "")
    netids.append(id)

length_of_text_data = len(text_data)
insert_netids = netids[0:length_of_text_data]

output = []
id = 0
for x, j in zip(insert_netids, text_data):
    id_str = str(id)
    date = generate_random_date
    title = j[0:10]
    xx = "insert into Blog_Post values  ('{idstr}', '{user_id}', '{date}', '{title}', '{text}');".format(idstr = id_str, user_id = x, date=generate_random_date(), title= j[0:10], text=j)
    output.append(xx)
    id = id + 1
    

f = open("load2.sql", "w+")
for line in output:
    insert = line + "\n"
    f.write(insert)
    
f.close()

    
    


