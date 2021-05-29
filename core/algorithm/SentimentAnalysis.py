import json
import requests
from bs4 import BeautifulSoup
import copy
import re
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')


class AlgoException(Exception):
    pass


class SentimentAnalysis:

    COMPR_TRIE = {}
    SENT_VALUE_KEY = '___'
    TRIE_JSON_FILE = r'core\storage\compressed_trie.json'
    POS_VALUE = 1
    NEU_VALUE = 0
    NEG_VALUE = -1
    STOP_VALUE = -1000

    def __init__(self, url: str, text: str, courier: str = ''):
        '''
        Initialize compressed sentiment tries from json file
        '''
        if len(self.__class__.COMPR_TRIE) == 0:
            self.read_compressed_trie()

        self.courier = courier
        self.url = url
        self.title = ''
        self.ori_text = ''
        self.result = {}
        self.clean_result = {}
        self.pos_words = 0
        self.neg_words = 0
        self.neu_words = 0
        self.stop_words = 0
        self.processed_word_list = []

        if url:
            # web scraping
            r = requests.get(url, verify=False)
            if r.status_code == 200:
                article = BeautifulSoup(r.content, "html.parser")
                resultArr = []
                if "www.thestar.com" in url:
                    body = article.find('div', attrs={"id": "story-body"})
                    title_tag = article.find('meta', attrs={"name": "content_title"})
                    self.title = title_tag.get('content', None)
                elif "www.theborneopost.com" in url:
                    body = article.find('div', attrs={"class": "post-content description"})
                    title_tag = article.find('h1', attrs={"class": "post-title item fn"})
                    self.title = title_tag.text.strip()
                resultArr = body.findAll('p')
                if len(resultArr) != 0:
                    for j in resultArr:
                        self.ori_text += str(j.get_text())
        else:
            self.ori_text = copy.deepcopy(text)
        # preprocessing
        self.processed_word_list = self.preprocess_strings(self.ori_text)
        # sentiment_analysis
        self.sentiment_analysis(self.processed_word_list)

    def preprocess_strings(self, text: str) -> list:
        '''
        - Split strings into list of strings
        - Remove punctuation, symbols and unwanted spaces
        - All lowercase
        - Sort ascending
        '''
        # tempText = copy.deepcopy(text)
        # tempText = re.sub(r'[^a-zA-Z]', ' ', tempText)
        # tempText = tempText.lower().split()
        # tempText.sort()
        tempText = re.sub(r'[^a-zA-Z]', ' ', text)
        tempText = tempText.lower().split()
        tempText.sort()
        return tempText

    def sentiment_analysis(self, words: 'list[str]'):
        '''
        Sentiment analysis for a list of words
        '''
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

        # searching
        for word in words:
            sentiment_value = search(self.__class__.COMPR_TRIE, word)
            # if positive word
            if sentiment_value == self.__class__.POS_VALUE:
                self.result[word] = sentiment_value
                self.clean_result[word] = sentiment_value
                self.pos_words += 1
            # if negative word
            elif sentiment_value == self.__class__.NEG_VALUE:
                self.result[word] = sentiment_value
                self.clean_result[word] = sentiment_value
                self.neg_words += 1
            # if neutral word
            elif sentiment_value == self.__class__.NEU_VALUE:
                self.result[word] = sentiment_value
                self.clean_result[word] = sentiment_value
                self.neu_words += 1
            # if stop word
            else:
                self.result[word] = sentiment_value
                self.stop_words += 1

    def get_sentiment_result(self) -> dict:
        '''
        Retrieve sentiment analysis result
        '''
        return self.result

    def get_analysis_result(self) -> tuple:
        '''Return analysis_result and its value in tuple'''
        result = ''
        result_val = 0
        if(self.pos_words == self.neg_words * 4 and self.pos_words<=10):
            result = "This article shows neutral sentiment."
            result_val = 0
        elif (self.pos_words >= self.neg_words * 4):
            result = "This article shows positive sentiment."
            result_val = 1
        else:
            result = "This article shows negative sentiment."
            result_val = -1

        return result, result_val

    def get_data(self) -> dict:
        '''Return a json data'''
        result, result_value = self.get_analysis_result()
        data = {
            "courier": self.courier,
            "url": self.url,
            "title": self.title,
            "ori_text": self.ori_text,
            "sentiment": self.clean_result,
            "frequency": {
                "positive": self.pos_words,
                "negative": self.neg_words,
                "neutral": self.neu_words,
            },
            "result": result,
            "result_value": result_value,
            "last_retrieve": datetime.now(),
            "dull_sentiment": self.result,
        }
        return data

    @classmethod
    def get_instance(cls, data: dict) -> 'SentimentAnalysis':
        '''Return a new analysis result from data'''
        newObj = cls(url=data['url'],
                     text=data['ori_text'],
                     courier=data['courier'])
        return newObj

    @classmethod
    def read_compressed_trie(cls) -> dict:
        '''Read compressed trie data into COMPR_TRIE class variable'''
        with open(cls.TRIE_JSON_FILE, 'r') as jsonFile:
            cls.COMPR_TRIE = json.load(jsonFile)
        return cls.COMPR_TRIE

    @classmethod
    def retrieve_all(cls) -> list:
        result_list = []
        URL_LIST_JSON_FILE = r'core\storage\url_list.json'
        with open(URL_LIST_JSON_FILE, 'r') as reader:
            url_dict = json.load(reader)
            for courier, urls in url_dict.items():
                print(courier)
                for url in urls:
                    ex = SentimentAnalysis(url=url, text=None, courier=courier)
                    data = ex.get_data()
                    del data["dull_sentiment"]
                    result_list.append(data)
                    print(url)
                print('')
        return result_list

    def generate_tries_json(file_paths: list, sentiment_values: list, output_path: str) -> None:
        '''
        Read the lists of positive/negative words from txt files, then build sentiment tries, output into a json file
        '''
        # TODO: read the files
        # TODO: sort the list
        # TODO: tries building
        pass

def identify_best_sentiment_company(result_list: list) -> dict:
    word_count = {}
    # accumulate word count
    for article in result_list:
        if article['courier'] not in word_count:
            word_count[article['courier']] = {'positive_word':0, 'negative_word':0}
        word_count[article['courier']]['positive_word'] += article['frequency']['positive']
        word_count[article['courier']]['negative_word'] += article['frequency']['negative']
    # calculate positive to negative ratio 
    max = 0
    bestCourier = ''
    for courier in word_count:
        ratio = word_count[courier]['positive_word'] / word_count[courier]['negative_word']
        if ratio > max:
            bestCourier = courier
            max = ratio
        word_count[courier]['ratio'] = ratio
    print(word_count)
    formatted_ratio = "{:.2f}".format(ratio)
    print(bestCourier+" has the best sentiment at ratio of positive word to negative word at "+str(formatted_ratio)+"\n")

if __name__ == "__main__":
    # URL_LIST_JSON_FILE = r'core\storage\url_list.json'
    # with open(URL_LIST_JSON_FILE, 'r') as reader:
    #     url_dict = json.load(reader)
    #     for courier, urls in url_dict.items():
    #         print(courier)
    #         for url in urls:
    #             print(url)
    #         print('')
    result_list = SentimentAnalysis.retrieve_all()
    identify_best_sentiment_company(result_list)

    # SentimentAnalysis.read_compressed_trie()
    # ex = SentimentAnalysis(url="https://www.theborneopost.com/2020/07/08/poslaju-customers-urged-to-bear-with-longer-waiting-time/", text=None)
    # data = ex.get_data()
    # print(json.dumps(data, indent=2, default=json_util.default))
    # newObj = SentimentAnalysis.get_instance(data)
    # data2 = newObj.get_data()
    # print(json.dumps(data2, indent=2, default=json_util.default))
