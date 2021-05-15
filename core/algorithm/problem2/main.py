import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# re for data processing
import re
# tqdm to show progress bar
from tqdm import tqdm
# ignore warning due to skipping verification while scrapping
import warnings
warnings.filterwarnings('ignore')

companyList = [
    {'id': 'citylink', 'listLinks': ["https://www.thestar.com.my/business/business-news/2015/01/05/citylink-mulls-main-market-listing-in-three-years",
                                     "https://www.theborneopost.com/2015/01/07/company-sets-up-collection-centres-for-relief-aid/", "https://www.theborneopost.com/2020/05/28/courier-service-a-lifeline-in-time-of-enforced-isolation/"], 'contents':''},
    {'id': 'poslaju', 'listLinks': ["https://www.theborneopost.com/2020/07/08/poslaju-customers-urged-to-bear-with-longer-waiting-time/",
                                    "https://www.thestar.com.my/news/nation/2020/09/08/pos-malaysias-sendparcel-to-hit-record-breaking-two-million-parcels-monthly", "https://www.thestar.com.my/opinion/letters/2019/04/17/delivery-by---poslaju-needs-to-be-improved/"], 'contents':''},
    {'id': 'gdex', 'listLinks': ["https://www.thestar.com.my/business/business-news/2021/04/13/gdex-ties-up-with-doc2us-alpro-for-medicine-delivery-tracking",
                                 "https://www.theborneopost.com/2020/11/30/gdexs-long-term-industry-prospect-remains-bright/", "https://www.thestar.com.my/business/business-news/2020/09/12/gdex-rejuvenates-systems-and-processes"], 'contents':''},
    {'id': 'jnt', 'listLinks': ["https://www.thestar.com.my/news/nation/2019/11/10/jt-express-anticipates-promising-1111-big-sale",
                                "https://www.thestar.com.my/news/nation/2021/02/07/courier-company-says-sorry-over-039violent-sorting-of-packages039", "https://www.theborneopost.com/2018/08/09/jt-express-ready-to-serve-swak-customers/"], 'contents':''},
    {'id': 'dhl', 'listLinks': ["https://www.theborneopost.com/2017/04/05/dhl-express-forays-into-sarawakian-market/",
                                "https://www.thestar.com.my/business/business-news/2007/03/20/dhl-to-expand-retail-network", "https://www.theborneopost.com/2018/08/16/dhl-ecommerce-inks-pact-with-shopee-msia/"], 'contents':''},
]


def checkValidity(url):
    '''Check whether the webpage is exist'''
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        return r
    return False


def scrapeWeb(url):
    '''web scrapping'''
    r = checkValidity(url)
    isStopwords = False
    # word classifier is to indicate the scrapping of positive and negative words
    wordClassifier = False
    # result is to return a long string of article contents
    result = ''
    if r:
        article = BeautifulSoup(r.content, "html.parser")
        resultArr = []
        if "www.thestar.com" in url:
            body = article.find('div', attrs={"id": "story-body"})
        elif "www.theborneopost.com" in url:
            body = article.find('div', attrs={"class": "post-content description"})
        elif "stopwords" in url:
            isStopwords = True
            body = article.find_all('td')
        elif "positivewordsresearch.com" in url:
            wordClassifier = True
            body = article.find('div', attrs={"class": "entry-content"})
            body = body.findAll('p')

        scrapNews = not isStopwords and not wordClassifier
        if not scrapNews:
            # clean the tag like <p></p>
            clean = re.compile('<.*?>')
            for n in np.arange(0, len(body)):
                body[n] = re.sub(clean, ' ', str(body[n]))
        else:
            resultArr = body.findAll('p')

        if len(body) != 0:
            if not scrapNews:
                for n in np.arange(0, len(body)):
                    if wordClassifier:
                        # this bunch is based on the html of the website
                        body[n] = body[n].lower().replace(",", "")
                        if '\xa0' in body[n]:
                            tempArr = body[n].split()
                            for i in tempArr:
                                if i not in resultArr:
                                    resultArr.append(i)
                    else:
                        # this is where stopwords is scrapped
                        tempArr = body[n].split()
                        for i in tempArr:
                            if i not in resultArr:
                                resultArr.append(i.lower())
            else:
                # this is where news content is scrapped
                for j in resultArr:
                    result += str(j.get_text())
    if scrapNews:
        # return a long string
        return result
    # return array
    return resultArr

# standard Trie


def stringMatching(oriArr, matchArr):
    freq = []
    # build trie
    root = {}
    for word in matchArr:
        cur = root
        for char in word:
            if char not in cur:
                if char == word[len(word) - 1]:
                    # to show the end of the word
                    cur[char] = {'end': 1}
                else:
                    # create new edge
                    cur[char] = {}
            cur = cur[char]
    # searching
    for word in oriArr:
        cur = root
        found = True
        for char in word[1]:
            if char not in cur:
                found = False
                break
            cur = cur[char]
        if found and "end" in cur.keys():
            # means the stopword is found
            freq.append(word)
    return freq

# findY is to create stack for plotly figure
# it returns array of frequency of certain word under 5 company articles


def findY(keyIndex):
    y = []
    for j in range(5):
        try:
            y.append(stopwordDict[j][stopWords[keyIndex]])
        except (KeyError):
            # means the stopword is not found then we assign 0 as the value
            y.append(0)
    return y


# Scrapping
for i in tqdm(companyList, desc='Scrapping'):
    index = 0
    # pass article link by link
    while index < 3:
        i['contents'] += str(scrapeWeb(i['listLinks'][index]))
        index += 1

stopWords = scrapeWeb("https://www.ranks.nl/stopwords")
positiveWords = scrapeWeb("https://positivewordsresearch.com/list-of-positive-words/")
negativeWords = scrapeWeb("https://positivewordsresearch.com/list-of-negative-words/")

# Data preprocessing
for i in tqdm(companyList, desc='Preprocess Data'):
    # remove punctuations
    i['contents'] = re.sub(r'[^a-zA-Z]', ' ', i['contents'])
    # to make all words in lower case and split them into array of words
    wordlist = i['contents'].lower().split()
    # count the frequency of each word
    wordfreq = [wordlist.count(w) for w in tqdm(wordlist, desc='Calculate Word Count')]
    # make them into dictionary to remove duplication
    i['unsortedWordPair'] = dict(list(zip(wordlist, wordfreq)))
    # make them in a pair for sorting purposes
    temp = [(i['unsortedWordPair'][key], key) for key in i['unsortedWordPair']]
    temp.sort()
    temp.reverse()
    # assign the pair array under wordFreq key
    i['wordFreq'] = temp
    # assign the stopword found in the array of words
    i['stopWordFreq'] = stringMatching(i['wordFreq'], stopWords)
    # remove the stopwords
    for word in i['stopWordFreq']:
        i['wordFreq'].remove(word)

# Can remove the comments below to get the positive and negative words and their respective word count directly
# Can refer company.csv under project directory to see the output
# # i['positiveWordFreq'] = stringMatching(i['wordFreq'],positiveWords)
# # i['negativeWordFreq'] = stringMatching(i['wordFreq'],negativeWords)
df = pd.DataFrame(companyList)
df.to_csv('company.csv', index=False, encoding='utf-8')

# Data Visualization for plotly in case needed (can remove when frontend is ready)
stopwordDict = [{'compName': 'Citylink'}, {'compName': 'Poslaju'}, {'compName': 'GDEX'}, {'compName': 'J&T'}, {'compName': 'DHL'}]
index = 0
for i in companyList:
    for j in i['stopWordFreq']:
        # to assign stopwords as keys and its word counts as value into stopwordDict
        stopwordDict[index][j[1]] = j[0]
    index += 1

# x-> category, y -> used for the stack that will be inserted row by row
x = ['Citylink', 'Poslaju', 'GDEX', 'JNT', 'DHL']

firstY = findY(0)
y = []
# example of element in y: [0,1,2,3,2]
# 5 elements = 5 companies, each value represent the word count of certain word under a company
y.append(firstY)
# this is the first stack
fig = go.Figure(go.Bar(x=x, y=firstY, name=stopWords[0]))

for i in tqdm(range(len(stopWords)-1), desc='Calculate Stopwords Word Count'):
    # we keep adding stack over here for each stopword
    tempY = findY(i+1)
    fig.add_trace(go.Bar(x=x, y=tempY, name=stopWords[i+1]))
    y.append(tempY)

# show the first plotly diagram with word count of each stopword
fig.update_layout(
    title="Stopwords Word Count",
    xaxis_title="Courier Company",
    yaxis_title="Word Count",
    barmode='stack', xaxis={'categoryorder': 'total descending'}
)
fig.show()

# we sum all the word count of all stopwords existed under a company
y = np.sum(y, axis=0)
fig = go.Figure(data=[go.Bar(
    x=x, y=y,
    text=y,
    textposition='auto',
)])
fig.update_layout(
    title="Stopwords Word Count",
    xaxis_title="Courier Company",
    yaxis_title="Word Count",
    xaxis={'categoryorder': 'total descending'}
)
# show a summarized word count plotly diagram
fig.show()
