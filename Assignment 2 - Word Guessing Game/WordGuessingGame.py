"""

Name: Justin Hardy
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""


import sys as system
import os.path as path
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords


# Create function(s).
def preprocess_input(stream):
    """
    Function description goes here!

    :param stream: File stream of text to process.
    :return: Tuple containing the list of tokens and the list of nouns.
    """
    # Read in input text as raw data...
    raw_text = stream.read()
    stream.close()

    # Replace newlines with blank spaces, and tokenize the text.
    raw_text = raw_text.replace("\n", " ")
    tokens = word_tokenize(raw_text)

    # Get unique token count...
    unique_tokens = []
    for token in tokens:
        if token not in unique_tokens:
            unique_tokens.insert(0, token)
    # Calculate Lexical Diversity.
    lexical_diversity = len(unique_tokens) / len(tokens)
    print("Lexical Diversity: ", lexical_diversity)

    # Get rid of punctuation tokens and normalize to lowercase...
    tokens = [token.lower() for token in tokens if token.isalpha() and token not in stopwords.words("english")
              and len(token) > 5]

    # Lemmatize the tokens...
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(token) for token in tokens]
    lemmas_unique = list(set(lemmas))

    # POS tag the unique lemmas...
    tags = pos_tag(lemmas_unique)
    print("Unique Lemmas Tagged (First 20): ", tags[:20])

    # Create list of noun-only lemmas...
    nouns = []
    for token, pos in tags:
        if "NN" in pos:
            nouns.insert(0, token)
    print(nouns)

    # Print number of tokens & number of nouns.
    print("Number of tokens: ", len(tokens))
    print("Number of nouns: ", len(nouns))

    # Return tokens and nouns
    return tokens, nouns


def guessing_game(word_list):
    """
    Function description goes here!

    :param word_list: List of potential words to be used in the guessing game.
    :return:
    """
    ## CODE GOES HERE


def main():
    """
    Function description goes here!

    :return: exit code (0 = success, 1 = missing argument(s), 2 = invalid input file name)
    """
    # Create input file stream...
    print("Opening file stream...")

    # Check if user inputted an argument...
    if len(system.argv) < 2:
        # Error in user input, terminate the program. (exit code 1)
        print("Unable to open file stream. User must input relative path of data.csv as program argument.")
        print("Terminating program...")
        exit(1)
    argument = system.argv[1]
    print("Inputted argument: \"" + argument + "\"")

    # Check if user argument leads to existing file...
    if not path.exists(argument):
        # Error in user input, terminate the program. (exit code 2)
        print("Unable to open file stream. Inputted file path leads to file that doesn't exist.")
        print("Terminating program...")
        exit(2)

    # Set up file stream.
    file_input = open(argument, mode="r")
    print("Successfully opened file stream.\n")

    # Preprocess text.
    tokens, nouns = preprocess_input(file_input)

    # Make dictionary that maps nouns to their count...
    noun_dict = {}
    for token in tokens:
        if token in nouns:
            if token not in noun_dict:
                noun_dict[token] = 1
            else:
                noun_dict[token] += 1

    # Sort the dictionary by most common noun.../
    noun_dict = dict(sorted(noun_dict.items(), key=lambda x: x[1], reverse=True))

    # Print the 50 most common words and their counts...
    print("Top 50 Most Common Words: ", dict(list(noun_dict.items())[:50]))

    # Save these words to a list.
    common_words = [noun for noun in dict(list(noun_dict.items())[:50])]

    # Run the guessing game:
    guessing_game(common_words)

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
