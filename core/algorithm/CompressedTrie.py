import json
import copy
import os

class CompressedTrie:
    SENT_VALUE_KEY = '___'
    PARENT_FOLDER = r'..\storage'
    ALTER_PARENT_FOLDER = r'.\core\storage'
    TRIE_JSON_FILE = r'compressed_trie.json'
    # TRIE_JSON_FILE = r'core\storage\compressed_trie.json'
    POS_WORDS = []
    NEG_WORDS = []
    STOP_WORDS = []
    WORDS_VALUES = []
    UNC_TRIE = {}
    C_TRIE = {}

    def __init__(self) -> None:
        if not os.path.exists(self.__class__.PARENT_FOLDER):
            self.__class__.PARENT_FOLDER = self.__class__.ALTER_PARENT_FOLDER

    @classmethod
    def run_generate_compressed_trie(cls):
        cls.read_word_files()
        cls.generate_input_variable()
        cls.UNC_TRIE = cls.build_trie(cls.WORDS_VALUES)
        cls.C_TRIE = cls.compress_trie(cls.UNC_TRIE)
        # output
        with open(os.path.join(cls.PARENT_FOLDER, cls.TRIE_JSON_FILE), 'w') as outfile:
            json.dump(cls.C_TRIE, outfile, indent=4)

    @classmethod
    def read_word_files(cls):
        # positive words
        with open(os.path.join(cls.PARENT_FOLDER, 'pos_words.txt'), 'r') as reader:
            cls.POS_WORDS = sorted(reader.read().split('\n'))
        
        # negative words
        with open(os.path.join(cls.PARENT_FOLDER, 'neg_words.txt'), 'r') as reader:
            cls.NEG_WORDS = sorted(reader.read().split('\n'))

        # stop words
        with open(os.path.join(cls.PARENT_FOLDER, 'stop_words.txt'), 'r') as reader:
            cls.STOP_WORDS = sorted(reader.read().split('\n'))

    @classmethod
    def generate_input_variable(cls):
        # create input variable for build_tries()
        pos_values = [1] * len(cls.POS_WORDS)
        pos_words_values = list(zip(cls.POS_WORDS, pos_values)) # [('a reason for being', 1), ('able', 1), ()]
        # print(pos_words_values[0])

        neg_values = [-1] * len(cls.NEG_WORDS)
        neg_words_values = list(zip(cls.NEG_WORDS, neg_values))
        # print(neg_words_values[0])

        # create input variable for stop words
        stop_values = [-1000] * len(cls.STOP_WORDS)
        stop_words_values = list(zip(cls.STOP_WORDS, stop_values))
        # print(stop_words_values[0])

        cls.WORDS_VALUES = stop_words_values + pos_words_values + neg_words_values

    @classmethod
    def build_trie(cls, words_values: list) -> dict:
        'Creates a basic uncompressed trie from a sorted list of words with sentiment values.'
        root = {}
        for (word, value) in words_values:
            node = root
            word_len = len(word)
            for i, char in enumerate(word):
                # create a new child if no char found
                if char not in node:
                    node[char] = {}
                
                # put a key in child indicate end of a complete word
                if i == word_len - 1:
                    node[char][cls.SENT_VALUE_KEY] = value
                node = node[char]
        return root

    @classmethod
    def compress_trie(cls, trie: dict) -> dict:
        '''Compress trie'''
        # compress the tries
        def rec_search(key: str, trie: dict) -> 'Tuple[str, dict]':
            # base case
            # end of last character of complete word
            if type(trie) is int:
                return key[:-len(cls.SENT_VALUE_KEY)], {cls.SENT_VALUE_KEY:trie}

            children_size = len(trie)
            newChildren = {}

            if children_size == 1:
                for childKey, childTrie in trie.items():
                    prefixKey = key+childKey
                    newKey, newChild = rec_search(prefixKey, childTrie)

                    # special case
                    # if the root tree only has one children
                    if key == '':
                        return '', {newKey:newChild}

                    return newKey, newChild
            else:
                for childKey, childTrie in trie.items():
                    if childKey == cls.SENT_VALUE_KEY:
                        newChildren[childKey] = childTrie
                    else:
                        prefixKey = ''+childKey
                        newKey, newChild = rec_search(prefixKey, childTrie)
                        newChildren[newKey] = newChild

            return key, newChildren

        trie = copy.deepcopy(trie)
        _, compressedTrie = rec_search('', trie)
        return compressedTrie

if __name__ == "__main__":
    tr = CompressedTrie()
    print(tr.PARENT_FOLDER)
    print(CompressedTrie.PARENT_FOLDER)
    tr.run_generate_compressed_trie()
    print('\n'.join(json.dumps(tr.C_TRIE, indent=4).split('\n')[:30]))