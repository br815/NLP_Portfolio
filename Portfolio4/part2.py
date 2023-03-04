# Names: Ghaida Alshiddi & Bushra Rahman
# Class: CS 4395.001
# Assignment: N-grams Part 2
# Due date: 3/4/23

import pathlib
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


# This function takes in a string of text, 2 dicts, and an int
# and returns a float for Laplace probability.
def compute_prob(text, unigram_dict, bigram_dict, V):
    # V is the vocabulary size in the training data (unique tokens)

    # Break the text into its unigrams
    text_unigrams = word_tokenize(text)
    # Break the text into its bigrams
    text_bigrams = list(ngrams(text_unigrams, 2))

    p_laplace = 1  # Calculate probability using Laplace smoothing

    for bigram in text_bigrams:
        # Numerator n = count of bigram if present in bigram dict, else 0
        # n = bigram_dict[bigram] if bigram in bigram_dict else 0
        n = int(bigram_dict.get(bigram)) if bigram in bigram_dict else 0
        # print('n = ', n, 'for', bigram)

        # Denominator = count of first unigram if present in unigram dict, else 0
        # d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        d = int(unigram_dict.get(bigram[0])) if bigram[0] in unigram_dict else 0
        # print('d = ', d, 'for', bigram)

        p_laplace = p_laplace * ((n + 1) / (d + V))
        # print('p_laplace =', p_laplace, 'for', bigram)

    # print("probability with laplace smoothing is %.10f" % p_laplace)
    return p_laplace


# main()
if __name__ == '__main__':
    # Read the pickle files back in
    bigrams1 = pickle.load(open('bigrams1.pickle', 'rb'))    # English bigrams
    unigrams1 = pickle.load(open('unigrams1.pickle', 'rb'))  # English unigrams
    bigrams2 = pickle.load(open('bigrams2.pickle', 'rb'))    # French bigrams
    unigrams2 = pickle.load(open('unigrams2.pickle', 'rb'))  # French unigrams
    bigrams3 = pickle.load(open('bigrams3.pickle', 'rb'))    # Italian bigrams
    unigrams3 = pickle.load(open('unigrams3.pickle', 'rb'))  # Italian unigrams

    # Vocab = total vocab size, # of unique tokens (add the lengths of the 3 unigram dictionaries)
    int_vocab = len(unigrams1) + len(unigrams2) + len(unigrams3)
    # print('The length is:', int_vocab)
    # Length should be 24842 for this particular data

    # Output file for appending language probabilities to (put it in same data folder as the other files)
    file_probs = open(pathlib.Path.cwd().joinpath('data/LangId.probs'), 'a')

    int_index = 1
    # Read in test file "LangId.test" line by line
    for line in open(pathlib.Path.cwd().joinpath('data/LangId.test'), 'r').readlines():
        # For each line, calculate the probability that the line may be each of the 3 languages
        # English, using unigrams1 and bigrams1
        probs1 = compute_prob(line, unigrams1, bigrams1, int_vocab)
        # French, using unigrams2 and bigrams2
        probs2 = compute_prob(line, unigrams2, bigrams2, int_vocab)
        # Italian, using unigrams3 and bigrams3
        probs3 = compute_prob(line, unigrams3, bigrams3, int_vocab)

        if (probs1 >= probs2) and (probs1 >= probs3):    # If largest is probs1, English
            langProb = 'English'
        elif (probs2 >= probs1) and (probs2 >= probs3):  # If largest is probs2, French
            langProb = 'French'
        else:                                            # If largest is probs3, Italian
            langProb = 'Italian'

        # Create string for the line index + the language that has the highest probability to be that line
        probString = str(int_index) + ' ' + langProb + '\n'
        # Update index
        int_index += 1
        # Write probString to "LangId.probs"
        file_probs.write(probString)
        # print(probString)
    # Close "LangId.probs" and open it again as readable instead
    file_probs.close()
    file_probs = open(pathlib.Path.cwd().joinpath('data/LangId.probs'), 'r')

    file_solutions = open(pathlib.Path.cwd().joinpath('data/LangId.sol'), 'r')
    probs_data = file_probs.readlines()
    sol_data = file_solutions.readlines()
    int_correct = 0
    # Compute accuracy by comparing "LangId.probs" to "LandId.sol"
    for i in range(len(probs_data)):
        if probs_data[i] == sol_data[i]:
            int_correct += 1
    accuracy = int_correct / len(probs_data)
    accuracy *= 100
    print('The percentage of correctly classified test cases is ' + str(accuracy) + '%.')
    # Accuracy should be about 97% for this data.

    # Close output files
    file_probs.close()
    file_solutions.close()
# End of main()
