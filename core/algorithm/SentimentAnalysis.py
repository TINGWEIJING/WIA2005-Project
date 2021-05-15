import json


class AlgoException(Exception):
    pass


class SentimentAnalysis:

    COMPR_TRIE = {}
    SENT_VALUE_KEY = '___'
    TRIE_JSON_FILE = r'core\storage\compressed_trie.json'

    def __init__(self, url: str = None, text: str = None):
        '''
        Initialize compressed sentiment tries from json file
        '''
        if len(self.__class__.COMPR_TRIE) == 0:
            self.read_compressed_trie()

        if url:
            # TODO: web scraping
            # TODO: run preprocess_strings()
            pass
        elif text:
            # TODO: run preprocess_strings()
            pass

    def preprocess_strings(self, text: str) -> list:
        '''
        - Split strings into list of strings
        - Remove punctuation, symbols and unwanted spaces
        - All lowercase
        - Sort
        '''
        pass

    def sentiment_analysis(self, words: 'list[str]'):
        '''
        Sentiment analysis for a list of words
        '''
        # TODO: optimized searching by sorting
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

        self.results = {}

        # TODO: stop words will not store in results
        for word in words:
            self.results[word] = search(self.__class__.COMPR_TRIE, word)

    def get_sentiment_values(self, words: 'list[str]') -> dict:
        '''
        Retrieve sentiment analysis result
        '''
        # TODO: optimized searching by sorting
        ####
        return self.result

    @classmethod
    def read_compressed_trie(cls) -> dict:
        '''Read compressed trie data into cTrie class variable'''
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
    ex = SentimentAnalysis()
    # print(ex.cTrie)
    print(ex.get_sentiment_values(['no', "ya", "yea", "yeah"]))
