# NLTK is our Natural-Language-Took-Kit
import re
import string
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

# Libraries for helping us with strings
# Regular Expression Library


def lowercase(s):
    return s.lower()


def lem_with_pos_tag(a_string):
    # Initalize our Lemmer
    lemmatizer = WordNetLemmatizer()

    # Break the sentence down into a list of words
    words = word_tokenize(a_string)

    # Get the word and pos_tag for each of the words.
    tagged_words = nltk.pos_tag(words)

    # Make a list to append valid words into
    valid_words = []

    # Loop through all the words
    for word in tagged_words:

        # The word is the first element in the tuple
        the_word = word[0]

        # The pos_tag is the second element in the tuple
        the_pos_tag = word[1]

        # Convert the pos_tag into the format the lemmatizer accepts
        the_pos_tag = convert_pos(the_pos_tag)

        # Lemmatize the word with the pos_tag
        lemmed_word = lemmatizer.lemmatize(the_word, the_pos_tag)

        # Append stemmed word to our valid_words
        valid_words.append(lemmed_word)

    # Join the list of words together into a string
    a_string = ' '.join(valid_words)


    return a_string


def stem_words(a_string):
    # Initalize our Stemmer
    porter = PorterStemmer()

    # Break the sentence down into a list of words
    words = word_tokenize(a_string)

    # Make a list to append valid words into
    valid_words = []

    # Loop through all the words
    for word in words:
        # Stem the word
        stemmed_word = porter.stem(word)

        # Append stemmed word to our valid_words
        valid_words.append(stemmed_word)

    # Join the list of words together into a string
    a_string = ' '.join(valid_words)

    return a_string


def remove_stopwords(a_string):
    # Break the sentence down into a list of words
    words = word_tokenize(a_string)

    # Make a list to append valid words into
    valid_words = []

    # Loop through all the words
    for word in words:

        # Check if word is not in stopwords
        if word not in stopwords:

            # If word not in stopwords, append to our valid_words
            valid_words.append(word)

    # Join the list of words together into a string
    a_string = ' '.join(valid_words)

    return a_string


def remove_punctuation(a_string):
    a_string = re.sub(r'[^\w\s]', '', a_string)
    return a_string


def convert_pos(pos):
    if pos.startswith('V'):
        return wordnet.VERB
    elif pos.startswith('J'):
        return wordnet.ADJ
    elif pos.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def text_pipeline(s):
    # s = remove_punctuation(s)
    # s = lowercase(s)
    # s = remove_stopwords(s)
    s = lem_with_pos_tag(s)
    # s = stem_words(s)
    return s
