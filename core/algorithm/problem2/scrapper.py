import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}
url1 = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
url2 = "https://elpais.com/elpais/inenglish.html"
results = requests.get(url1, headers=headers) 

r1 = requests.get(url2)

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, "html.parser")

# News identification
coverpage_news = soup1.find_all('h2', class_='articulo-titulo')
print(len(coverpage_news))

soup = BeautifulSoup(results.text, "html.parser")

#print(soup.prettify())
