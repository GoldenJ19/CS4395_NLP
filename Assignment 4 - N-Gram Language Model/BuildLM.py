"""

Name: Justin Hardy
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import os
import pickle
from nltk import word_tokenize, ngrams

# Declare default file names & data folder path
file_names = ["LangId.train.English", "LangId.train.French", "LangId.train.Italian"]
data_folder = "data"
output_folder = "output"


# Create function(s).
def build_language_model(file_name):
    """
    Creates a language model using the text from the inputted file. Looks in folder specified by the
    global data folder path for the inputted file.

    :param file_name: The file that we wish to read from.
    :return: Tuple containing the Unigram and Bigram dictionary counts.
    """
    # Get global data folder path
    global data_folder

    # Open file stream
    input_stream = open(os.path.join(data_folder, file_name), "r", encoding="utf-8")

    # Read in the text
    input_text = input_stream.read()

    # Remove newlines
    input_text = input_text.replace("\n", "")

    # Tokenize the text
    tokens = word_tokenize(input_text)

    # Create list of bigrams
    bigrams = list(ngrams(tokens, 2))

    # Create dictionary of bigram and unigram counts, each separate
    unigrams_dict = {t:tokens.count(t) for t in set(tokens)}
    bigrams_dict = {b:bigrams.count(b) for b in set(bigrams)}

    # Close file stream
    input_stream.close()
    return unigrams_dict, bigrams_dict


""" ** Abandoned argument processing, commented out for archive **
def process_arguments():
    # Get globals
    global file_names, data_folder

    # Check if system arguments were inputted. Adjust program to utilize them if they were.
    # Notify user according to their input
    if len(system.argv) == 2 or len(system.argv) > 3:
        # Notify user of argument detection
        print("File name arguments detected.")

        # Check for 3 arguments (file name replace)
        if len(system.argv) > 3:
            # Notify user of file name overwrite
            print("Overwriting default file names with the following:")
            for i in range(3):
                print(" -", system.argv[i + 1])

        # Check for 1 or 4 arguments (data folder path replace)
        if len(system.argv) > 4 or len(system.argv) == 2:
            # Notify user of data folder path overwrite
            print("Overwriting default Data folder path with:")
            print(" -", system.argv[4 if len(system.argv) > 4 else 1])

        print()

    # Replacements will be an option if 1 argument, 3 arguments, or more were inputted.
    # Verify the user's intentions to overwrite defaults...
    if len(system.argv) == 2 or len(system.argv) > 3:
        # Ask user to confirm these changes
        response = input("Are you sure you'd like to make these changes? (Y/N):\n>")
        print()
        response = response.lower()

        # Overwrite file names & data folder
        if response == "y" or response == "ye" or response == "yes":
            print("Confirmed. Overwriting default folder path and file names...")
            # Overwrite file names for 3 or more arguments
            if len(system.argv) > 3:
                file_names = [system.argv[1], system.argv[2], system.argv[3]]
            # Overwrite data folder for 4 or more arguments
            if len(system.argv) > 4:
                data_folder = system.argv[4]
            # Overwrite only data folder for 1 argument
            elif len(system.argv) == 2:
                data_folder = system.argv[1]
        else:
            print("Either a \"no\" response was read, or the input was unexpected.\n"
                  "Ignoring arguments, and keeping defaults...")
        print()
    # Check for invalid argument count (2 arguments)
    elif len(system.argv) == 3:
        # Print warning/notification of insufficient arguments
        print("WARNING: 2 arguments were inputted, which is an invalid argument input.")
        print("You can input:")
        print(" - 1 argument to replace the default data folder path")
        print(" - 3 arguments to replace the default file names")
        print(" - 4 arguments to replace the default file names, followed by the default data folder path.")
        print("")
        print("Using default file names instead...")
        print("")
"""

def main():
    """
    This program is designed to create language models using the LangId files provided in the data
    folder. The language models are of the English, French, and Italian languages. Each n-gram will
    be outputted to their own pickle file for use in the other program, EvaluateLM.py, after which
    this program will no longer need to be ran as the output can be accessed via the pickle file.

    :return: exit code (0 = success, 1 = error)
    """
    # Get global file names
    global file_names, output_folder

    """
    # Process any program arguments
    process_arguments()
    """

    # Build language models
    print("Building English Language Model...")
    unigrams_dict_en, bigrams_dict_en = build_language_model(file_names[0])
    print("Building French Language Model...")
    unigrams_dict_fr, bigrams_dict_fr = build_language_model(file_names[1])
    print("Building Italian Language Model...")
    unigrams_dict_it, bigrams_dict_it = build_language_model(file_names[2])
    print("Finished creating language models.", "\n")

    # Pickle the dictionaries
    print("Pickling language models...")
    pickle.dump(unigrams_dict_en, open(os.path.join(output_folder, "lm_uni_en.p"), "wb"))
    pickle.dump(bigrams_dict_en, open(os.path.join(output_folder, "lm_bi_en.p"), "wb"))
    pickle.dump(unigrams_dict_fr, open(os.path.join(output_folder, "lm_uni_fr.p"), "wb"))
    pickle.dump(bigrams_dict_fr, open(os.path.join(output_folder, "lm_bi_fr.p"), "wb"))
    pickle.dump(unigrams_dict_it, open(os.path.join(output_folder, "lm_uni_it.p"), "wb"))
    pickle.dump(bigrams_dict_it, open(os.path.join(output_folder, "lm_bi_it.p"), "wb"))
    print("Finished pickling.")

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
