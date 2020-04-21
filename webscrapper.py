#Scraped from www.roomies.com. publicly available website.

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

URLS = []
starting = "https://www.roomies.com/profiles/"
c = 500000
counter = 50
text_data = []

while (counter != 0):
    x_str = str(c)
    new_starting = starting + x_str
    page = requests.get(new_starting)
    soup = BeautifulSoup(page.content, 'lxml')
    container = soup.find("div",attrs={'class': 'markdown text-gray-darkest'})
    for p in container.find_all('p'):
        text_data.append(p.text)
    
    c = c + 1
    counter = counter - 1
    
df = pd.DataFrame(text_data)
df.to_csv("output.csv")
