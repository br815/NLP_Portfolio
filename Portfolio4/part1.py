# Name: Bushra Rahman
# Class: CS 4395.001
# Assignment: N-grams Part 1
# Due date: 3/4/23

import pathlib
import sys
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


# This function takes a file name as an argument
# and returns a tuple of 2 dictionaries.
def read_file(filename):
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r', encoding="utf8") as f:
        # str_text is a string of all text from input file f, with newlines removed
        str_text = f.read().replace('\n', '')

    # Tokenize the text and use NLTK to create bigrams and unigrams lists
    unigrams = word_tokenize(str_text)
    bigrams = list(ngrams(unigrams, 2))

    # Unigram dictionary of unigrams and counts: [‘token’] -> count
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    # Bigram dictionary of bigrams and counts: [‘token1 token2’] -> count
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    return bigram_dict, unigram_dict
# End of read_file()


# main()
if __name__ == '__main__':
    # File names should be provided as sysargs as follows:
    # "data/LangId.train.English" "data/LangId.train.French" "data/LangId.train.Italian"
    # They need to be provided this way bc the data/ folder contains other junk files.
    if len(sys.argv) < 4:
        print("Please enter filenames as sys args as follows:")
        print("data/LangId.train.English" "data/LangId.train.French" "data/LangId.train.Italian")
        quit()

    for i in range(1, 4):  # The sysargs correspond to the indexes 1, 2, and 3
        rel_path = sys.argv[i]
        print("\nNow reading " + rel_path + ".")
        bigrams, unigrams = read_file(rel_path)

        # pickle the dictionaries
        print("Pickling bigrams...")
        bigrams_file = open('bigrams%d.pickle' % i, 'wb')
        pickle.dump(bigrams, bigrams_file)
        bigrams_file.close()

        print("Pickling unigrams...")
        unigrams_file = open('unigrams%d.pickle' % i, 'wb')
        pickle.dump(unigrams, unigrams_file)
        unigrams_file.close()

# End of main()
