import json
import requests
from bs4 import BeautifulSoup
import copy
# re for data processing
import re
# ignore warning due to skipping verification while scrapping
import warnings
warnings.filterwarnings('ignore')

class AlgoException(Exception):
    pass


class SentimentAnalysis:

    COMPR_TRIE = {}
    SENT_VALUE_KEY = '___'
    TRIE_JSON_FILE = r'core\storage\compressed_trie.json'

    def __init__(self, url: str, text: str):
        '''
        Initialize compressed sentiment tries from json file
        '''
        if len(self.__class__.COMPR_TRIE) == 0:
            self.read_compressed_trie()

        self.result = {}
        tempText = ''
        if url:
            # web scraping
            r = requests.get(url,verify = False)
            if r.status_code == 200:
                article = BeautifulSoup(r.content, "html.parser")
                resultArr = []
                if "www.thestar.com" in url:
                    body = article.find('div',attrs={"id": "story-body"})   
                elif "www.theborneopost.com" in url:
                    body = article.find('div',attrs={"class": "post-content description"})  
                resultArr = body.findAll('p')
                if len(resultArr) != 0:
                    for j in resultArr:
                        tempText += str(j.get_text()) 
        else:
            tempText = copy.deepcopy(text)
        # preprocessing
        textList = self.preprocess_strings(tempText)
        # sentiment_analysis
        self.sentiment_analysis(textList)

    def preprocess_strings(self, text: str) -> list:
        '''
        - Split strings into list of strings
        - Remove punctuation, symbols and unwanted spaces
        - All lowercase
        - Sort ascending
        '''
        tempText = copy.deepcopy(text)
        tempText = re.sub(r'[^a-zA-Z]', ' ', tempText)
        tempText = tempText.lower().split()
        tempText.sort()
        return tempText

    def sentiment_analysis(self, words: 'list[str]'):
        '''
        Sentiment analysis for a list of words
        '''
        # TODO: optimized searching by sorting
        ####
        def search(trie: dict, word: str) -> int:
            '''
            Helper method to search compressed trie
            '''
            word_length = len(word)
            offset = 0
            lastIndex = 0

            for i in range(word_length):
                key = word[offset:i+1]
                value = trie.get(key)

                if value is not None:
                    trie = value
                    offset += len(key)
                    lastIndex = i

            result = trie.get(self.__class__.SENT_VALUE_KEY)
            if result is None or lastIndex != word_length - 1:
                return 0
            return result
        ####

        # check imported compressed trie
        if len(self.__class__.COMPR_TRIE) == 0:
            raise AlgoException('Sentiment trie is empty')

        self.result = {} # TODO: exclude stop word

        self.pos_words = self.get_pos_words_frequency() # TODO: frequency
        self.neg_words = 0
        self.stop_words = 0
        self.neu_words = 0
        print(self.pos_words)
        # TODO: store words frq
        # TODO: check which company
        for word in words:
            self.result[word] = search(self.__class__.COMPR_TRIE, word)

    def get_sentiment_values(self) -> dict:
        '''
        Retrieve sentiment analysis result
        '''
        return self.result

    # TODO: write get freq methods
    def get_pos_words_frequency(self) -> dict:
        count = 0
        for value in self.result:
            if(self.result[value]==1):
                count+=1
        return count

    @classmethod
    def read_compressed_trie(cls) -> dict:
        '''Read compressed trie data into COMPR_TRIE class variable'''
        with open(cls.TRIE_JSON_FILE, 'r') as jsonFile:
            cls.COMPR_TRIE = json.load(jsonFile)
        return cls.COMPR_TRIE

    def generate_tries_json(file_paths: list, sentiment_values: list, output_path: str) -> None:
        '''
        Read the lists of positive/negative words from txt files, then build sentiment tries, output into a json file
        '''
        # TODO: read the files
        # TODO: sort the list
        # TODO: tries building
        pass


if __name__ == "__main__":
    SentimentAnalysis.read_compressed_trie()
    ex = SentimentAnalysis("https://www.thestar.com.my/business/business-news/2015/01/05/citylink-mulls-main-market-listing-in-three-years",None)
    # ex.sentiment_analysis(['no', "ya", "yea", "yeah"])
    # print(ex.cTrie)
    print(ex.get_sentiment_values())
