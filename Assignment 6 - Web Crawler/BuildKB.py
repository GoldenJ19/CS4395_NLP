"""

Names: Justin Hardy, Benji Frenkel
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import os
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Define global variables
output_folder = "output"
output_file_names = ["linktext", "linktext_c", "kb.p"]
punctuation = [".", "?", "!"]
ignore_spaces_for = [".", "?", "!", ",", ":", "\"", "%"]


def clean_text(text):
    """
    Cleans a given text in preparation for NLP.

    :param text: text to clean up
    :return: cleaned up text
    """
    #remove new lines and tabs from the text
    text = text.replace("\n", "")
    text = text.replace("\t", "")

    tokenized_text = word_tokenize(text)

    return tokenized_text


def extract_important_terms(token_list: list):
    """
    Extracts important terms from a list of texts, and ranks them by frequency.

    :param token_list: List of texts to extract terms from.
    :return: List of important terms (by sorted by frequency).
    """
    # Lowercase all tokens
    clean_token_list = []
    for i in range(len(token_list)):
        tokens = token_list[i]
        clean_token_list.insert(len(clean_token_list), [token.lower() for token in tokens
                                                        if token.isalpha() and token.lower() not in stopwords.words("english")])
    # print("Cleaned Tokens:\n", clean_token_list)

    # Create dictionary to store counts
    token_dict = {}

    # Loop through tokens of each file, get counts
    for tokens in clean_token_list:
        for token in tokens:
            if not token in token_dict.keys():
                # add token to dict
                token_dict[token] = 1
            else:
                # update count of token in dict
                token_dict[token] += 1

    # Sort tokens by frequency into a list (most frequent -> least frequent)
    sorted_token_list = [tup[0] for tup in sorted(token_dict.items(), key=lambda x: x[1], reverse=True)]
    top_tokens = sorted_token_list[:25]
    # print(top_tokens)

    # Return the top 25 tokens
    return top_tokens


def build_kb(terms_list: list, texts: list):
    """
    Builds a knowledge base for the given list of words using the text from the texts list.

    :param terms_list: Terms to use as the knowledge base's keys.
    :param texts: Texts to use for the knowledge base's values.
    :return: A knowledge base dictionary; each word is a key, each value is a sentence relevant to the key.
    """
    # Initialize knowledge base dict
    kb = {}

    # Search texts for every mention of the word.
    for term in terms_list:
        # Create list of relevant sentences
        relevant_sentences = []

        # Search each text for word mention
        for text in texts:
            # Copy text to temporary variable
            _text = text

            # Look for mention of word in text
            while term in _text:
                # Get index of the term
                index = _text.index(term)
                start = end = index

                # Get start index of the sentence
                while not _text[start] in punctuation and not start == 0:
                    start -= 1
                start += 1

                # Get end index of the sentence
                while not _text[end] in punctuation and not end == len(_text)-1:
                    end += 1
                end += 1

                # Pop tokens from the start to end indexes
                sentence = ""
                for i in range(end-start):
                    # Capitalize first token
                    if i == 0:
                        _text[start] = _text[start].title()

                    # Insert token into list
                    sentence += (" " + _text[start]) if _text[start] not in ignore_spaces_for and not i == 0 else _text[start]

                    # Remove token from list
                    _text.remove(_text[start])

                # Insert sentence into relevant sentences list
                if sentence not in relevant_sentences:
                    relevant_sentences.insert(len(relevant_sentences), sentence)

        # Insert term into knowledge base
        kb[term] = relevant_sentences

    # Return knowledge base dict
    return kb


def main():
    """
    Builds a knowledge base using the texts read in from the pickle files from a given output folder and set of
    15 output files.

    :return: exit code (0 = success, 1 = error)
    """
    # Get global
    global output_folder, output_file_names

    # Read pickle files
    print("Loading pickles...")
    texts = []
    for i in range(15):
        # Go from 1-15 instead of 0-14
        _i = i+1

        # Read pickle file
        texts.insert(len(texts), pickle.load(open(os.path.join(output_folder, output_file_names[0] + str(_i) + ".p")
                                                  , "rb")))
    print("Done loading pickles.")
    print()

    # Clean each individual text
    print("Cleaning texts and writing them to files...")
    texts_clean = []
    for i in range(15):
        # Clean up text, insert into list
        ct = clean_text(texts[i])
        texts_clean.insert(len(texts_clean), ct)

        # Write to pickle file
        _i = i+1
        pickle.dump(ct, open(os.path.join(output_folder, output_file_names[1] + str(_i)) + ".p", "wb"))
    print("Done cleaning text and writing them to files.")
    print()

    # Get top 25 terms from text
    print("Extracting important terms...")
    terms_list_25 = extract_important_terms(texts_clean)
    print("Done extracting important terms.")
    print()

    # Get top 10 terms from top 25 terms
    terms_list_10 = terms_list_25[:10]

    # Build searchable knowledge base of these top 10 terms
    print("Building knowledge base...")
    kb = build_kb(terms_list_10, texts_clean)
    print("Done building knowledge base.")
    print()

    # Pickle the kb
    pickle.dump(kb, open(os.path.join(output_folder, output_file_names[2]), "wb"))

    # Print kb
    for k in kb:
        v = kb[k]
        print("[", k, "]")
        for sentence in v:
            print(" •", sentence)
        print()

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
