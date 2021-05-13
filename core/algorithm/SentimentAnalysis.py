from pathlib import Path
import json


class AlgoException(Exception):
    pass


class SentimentAnalysis:

    cTrie: dict[str,str] = {}
    SENT_VALUE_KEY = '___'

    def __init__(self, file_path: str) -> None:
        '''
        Initialize compressed sentiment tries from json file
        '''
        # check file extension
        if Path(file_path).suffix != '.json':
            raise AlgoException('Not a json file')

        # import json and convert into compressed trie
        with open(file_path, 'r') as jsonFile:
            self.__class__.cTrie = json.load(jsonFile)

        # check imported compressed trie
        if len(self.__class__.cTrie) == 0:
            raise AlgoException('Sentiment trie is empty')

    def get_sentiment_values(self, words: 'list[str]') -> dict:
        '''
        Sentiment analysis for a list of words
        '''
        # TODO: implement looping with searching
        # TODO: raise error if cTrie is empty
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
        if len(self.__class__.cTrie) == 0:
            raise AlgoException('Sentiment trie is empty')

        results = {}

        for word in words:
            results[word] = search(self.__class__.cTrie, word)

        return results

    def generate_tries_json(file_paths: list, sentiment_values: list, output_path: str) -> None:
        '''
        Read the lists of positive/negative words from txt files, then build sentiment tries, output into a json file
        '''
        # TODO: read the files
        # TODO: sort the list
        # TODO: tries building
        pass


if __name__ == "__main__":
    TRIE_JSON_FILE = r'core\storage\compressed_trie.json'
    ex = SentimentAnalysis(TRIE_JSON_FILE)
    print(ex.cTrie)
    print(ex.get_sentiment_values(['no', "ya", "yea", "yeah"]))
