"""

Name: Justin Hardy
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import pickle
import os
from nltk import word_tokenize, ngrams

# Declare default file names & data folder path
pickle_file_names = ["lm_uni_en.p", "lm_bi_en.p", "lm_uni_fr.p", "lm_bi_fr.p", "lm_uni_it.p", "lm_bi_it.p"]
test_file_names = ["LangId.test", "LangId.sol"]
data_folder = "data"
output_folder = "output"


# Create function(s).
def get_probability(unigrams_dict, bigrams_dict, test_text):
    """
    Calculates probability of the language being used in a given text using the language model provided.

    :param unigrams_dict: Dictionary of unigrams and their counts in the language model.
    :param bigrams_dict: Dictionary of unigrams and their counts in the language model.
    :param test_text: Text to calculate the language probability on.
    :return: List of probabilities for each line of the test text.
    """
    # Calculate token count and number of unique tokens
    token_count = sum([v for v in unigrams_dict.values()])
    unique_token_count = len(unigrams_dict)

    # Declare probabilities list
    probabilities = []

    # For each line in the test text, calculate probability
    for line in test_text.split("\n"):
        # Skip empty lines
        if line == "":
            continue

        # Tokenize line
        unigrams_test = word_tokenize(line)
        bigrams_test = list(ngrams(unigrams_test, 2))

        # Declare p values
        p_laplace = 1    # Initial laplace smoothing probability

        # Go through each bigram, modify probabilities accordingly
        for bigram in bigrams_test:
            # Get count of bigram from the language model
            bigram_count = bigrams_dict[bigram] if bigram in bigrams_dict else 0
            bigram_count_gt = bigrams_dict[bigram] if bigram in bigrams_dict else (1 / token_count)

            # Get count of first unigram in the bigram from the language model
            unigram_count = unigrams_dict[bigram[0]] if bigram[0] in unigrams_dict else 0

            # Modify laplace smoothing probability
            p_laplace *= ((bigram_count + 1) / (unigram_count + unique_token_count))

        # Insert probability calculations into probabilities list
        probabilities.insert(len(probabilities), p_laplace)

    # Return probabilities list
    return probabilities


def main():
    """
    This program is designed to use the language models generated from BuildLM.py to classify language
    for each line of a given text file. After classifying, it will check its accuracy using a file
    containing details of the actual language used in each line. All classifications and the program's
    accuracy will be outputted to a file.

    :return: exit code (0 = success, 1 = pickle files not found, 2 = unpickling error)
    """
    # Get globals
    global data_folder, output_folder, pickle_file_names, test_file_names

    # Read pickled dictionaries
    print("Reading pickled dictionaries...")
    try:
        # Attempt to oad unigrams / bigrams
        unigrams_en = pickle.load(open(os.path.join(output_folder, pickle_file_names[0]), "rb"))
        bigrams_en = pickle.load(open(os.path.join(output_folder, pickle_file_names[1]), "rb"))
        unigrams_fr = pickle.load(open(os.path.join(output_folder, pickle_file_names[2]), "rb"))
        bigrams_fr = pickle.load(open(os.path.join(output_folder, pickle_file_names[3]), "rb"))
        unigrams_it = pickle.load(open(os.path.join(output_folder, pickle_file_names[4]), "rb"))
        bigrams_it = pickle.load(open(os.path.join(output_folder, pickle_file_names[5]), "rb"))
    except FileNotFoundError as e:
        # Error opening input stream to pickle file(s)...
        print("Failed to load pickle files from folder \"" + output_folder + "\".")
        print("There appears to be missing pickle file(s).", "\n")
        print("Exception message:", e if not str(e) == "" else "None", "\n")

        # Error in pickle file stream opening, terminate the program. (exit code 1)
        print("Terminating Program...")
        exit(2)
    except (pickle.UnpicklingError, MemoryError) as e:
        # Error reading pickled dictionaries...
        print("Failed to load pickle file from folder \"" + output_folder + "\".")
        print("There seems to have been a problem unpickling one of the files.", "\n")
        print("Exception message:", e if not str(e) == "" else "None", "\n")

        # Error in pickle file, terminate the program. (exit code 2)
        print("Terminating Program...")
        exit(1)
    print("Finished unpickling the dictionaries.")
    print("")

    # Open input file stream to train file
    test_file = open(os.path.join(data_folder, test_file_names[0]), "r")

    # Read test file text
    test_text = test_file.read()

    # Close test file stream
    test_file.close()

    # Calculate probabilities of the languages
    print("Calculating language probabilities...")
    probabilities_en = get_probability(unigrams_en, bigrams_en, test_text)
    probabilities_fr = get_probability(unigrams_fr, bigrams_fr, test_text)
    probabilities_it = get_probability(unigrams_it, bigrams_it, test_text)
    print("Finished calculations.")
    print("")

    # Start classifying, create output stream...
    print("Writing language classifications to file...")
    output_stream = open(os.path.join(output_folder, "evaluation.txt"), "w")

    # For each line in the test text, classify the line's language using most probable language...
    classifications = []
    for i in range(len(probabilities_en)):
        # Find out which probability is highest
        highest = max(probabilities_en[i], probabilities_fr[i], probabilities_it[i])

        # Print predicted langauge to file for line
        if highest == probabilities_en[i]:
            # Predict English
            output_stream.write(str(i+1))
            output_stream.write(" English\n")
            classifications.insert(len(classifications), "English")
        elif highest == probabilities_fr[i]:
            # Predict French
            output_stream.write(str(i+1))
            output_stream.write(" French\n")
            classifications.insert(len(classifications), "French")
        elif highest == probabilities_it[i]:
            # Predict Italian
            output_stream.write(str(i+1))
            output_stream.write(" Italian\n")
            classifications.insert(len(classifications), "Italian")
        else:
            # Prediction error
            output_stream.write(str(i+1))
            output_stream.write(" Error\n")
            classifications.insert(len(classifications), "Error")
    print("Finished writing language classifications.")
    print("")

    # Compute and output accuracy, read solutions...
    print("Computing accuracy...")
    solution_stream = open(os.path.join(data_folder, test_file_names[1]), "r")
    solutions = solution_stream.read().split("\n")
    if solutions[len(solutions) - 1] == "":  # Remove empty split from end of solutions list, if it's present
        solutions.remove("")
    solutions = [line.split(" ")[1] for line in solutions]

    # Calculate number of correct classifications
    correct = 0
    for i in range(len(classifications)):
        if classifications[i] == solutions[i]:
            correct += 1

    # Calculate accuracy
    accuracy = correct / len(classifications)
    print("Finished computing accuracy.")
    print("")

    # Write & Print prediction accuracy
    output_stream.write("\nAccuracy: ")
    output_stream.write(str(accuracy))
    print("Accuracy:", accuracy)

    # Close streams
    solution_stream.close()
    output_stream.close()

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
