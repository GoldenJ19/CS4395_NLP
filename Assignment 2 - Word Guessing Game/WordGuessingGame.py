"""

Name: Justin Hardy
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import sys as system
import os.path as path
import PySimpleGUI as gui
import random
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords


# Create function(s).
def preprocess_input(stream):
    """
    Processes through an input stream, tokenizing its text, and extracting its unique nouns. All while printing out
    relevant information about what is being processed to the console.

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
    print("Lexical Diversity: ", round(lexical_diversity, 2))

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
        if pos == "NN":  # "NN" in pos: (need to ask about this)
            nouns.insert(0, token)

    # Print number of tokens & number of nouns.
    print("Number of tokens: ", len(tokens))
    print("Number of nouns: ", len(nouns))

    # Return tokens and nouns
    return tokens, nouns


def get_censored_word(word, letters_guessed):
    """
    Formats a given word based off of what letters of the word have been guessed, to hide un-guessed letters.
    For example, for the word "hello" and letters_guessed ['a','e','i','o','u'], return "_ e _ _ o".

    :param word: Word the user must guess
    :param letters_guessed: List of letters guessed already
    :return: string containing formatted word censored to only show correct guesses
    """
    censored_word = ""
    for i in range(len(word)):
        # Format to only show correctly guessed letters
        censored_word += word[i] if word[i] in letters_guessed else "_"
        censored_word += "" if i == len(word) - 1 else " "
    return censored_word


def check_win_condition(word, letters_guessed):
    """
    Returns true if all letters in the given word are a part of the letters_guessed list. In other words,
    a win state is given if all letters have been guessed correctly.

    :param word: Word the user must guess
    :param letters_guessed: List of letters guessed already
    :return: boolean denoting win condition
    """
    for letter in word:
        if letter not in letters_guessed:
            return False
    return True


def guessing_game(word_list, start_score=5):
    """
    Starts a guessing game, which will randomly select a word from a given word list, which the user can interact
    with through the GUI.

    :param word_list: List of potential words to be used in the guessing game.
    :param start_score: Starting score for this game. Default value is 5.
    :return: Ending score
    """
    # Select word
    random.seed()
    word_index = random.randint(0, len(word_list))
    word = word_list[word_index]
    # print("(DEBUG) Selected Index: " + str(word_index) + "\nWord: " + word)

    # Create game attributes
    score = start_score
    letters_guessed = []

    # Create GUI Window
    gui.SetOptions(
        text_element_background_color="#DADADA",
        element_background_color="#DADADA",
        background_color="#DADADA",
        input_elements_background_color="#FFFFFF",
        button_color=("#000000", "#AC3E31"),
        text_color="#000000",
        font=("MS Sans Serif", 10)
    )
    game_layout = [
        [gui.Text("Guessing Game", text_color="#DBAE58", font=("MS Sans Serif", 18, "bold"))],
        [gui.Text("Word: " + get_censored_word(word, letters_guessed), enable_events=True, key="word",
                  font=("MS Sans Serif", 10, "bold"))],
        [gui.InputText(size=(25, 1), enable_events=True, key="input")],
        [gui.Button("Guess", key="guess", bind_return_key=True)],
        [gui.Text("Score: " + str(score), font=("MS Sans Serif", 6), enable_events=True, key="score"), gui.Push()]
    ]
    game_window = gui.Window(
        "Guessing Game",
        layout=game_layout,
        size=(300, 160),
        element_justification="center"
    )

    # Present Window
    game_active = True
    while game_active:
        # Read events
        game_event, game_values = game_window.read()
        if game_event == gui.WIN_CLOSED:
            score = -100
            break
        elif game_event == "guess":
            # Remove any non-letters from inputted guess
            guesses = str(game_values["input"])
            for c in guesses:
                if not c.isalpha():
                    guesses = guesses.replace(c, "")

            # Check if entire word was guessed
            if guesses == word:
                letters_left = 0
                for guess in guesses:
                    if guess not in letters_guessed:
                        letters_left += 1
                        letters_guessed.insert(0, guess)
                score += letters_left
                gui.popup_auto_close("You correctly guessed the word, \"" + word + "\"!\n\n" +
                                     "(+" + str(letters_left) + " score)\n\nYou win!",
                                     title="Correct Guess",
                                     auto_close_duration=1)

                # Set game state to inactive; break out of for loop
                game_active = False
                break

            # Split guess into characters
            for guess in guesses:
                if guess not in letters_guessed and guess in word:
                    # Insert letter into guessed letter list, update score
                    letters_guessed.insert(0, guess)
                    score += 1

                    if check_win_condition(word, letters_guessed):
                        # Notify user of win, exit game.
                        gui.popup_auto_close("Congrats! You guessed correctly, which completed the word.\n\n" +
                                             "(+1 score)\n\nYou win!",
                                             title="Correct Guess",
                                             auto_close_duration=1)

                        # Set game state to inactive; break out of for loop
                        game_active = False
                        break
                    else:
                        # Notify user of correct guess
                        gui.popup_auto_close("You correctly guessed the letter \"" + guess + "\"\n\n(+1 score)",
                                             title="Correct Guess",
                                             auto_close_duration=1)
                elif guess in letters_guessed:
                    # Notify user of repeat guess
                    gui.popup_auto_close("You've already guessed the letter \"" + guess + "\". Ignoring input.",
                                         title="Notice",
                                         auto_close_duration=1)
                else:
                    # Insert letter into guessed letter list, update score
                    letters_guessed.insert(0, guess)
                    score -= 1

                    if score < 0:
                        # Notify user of loss, exit game.
                        gui.popup_auto_close(
                            "Sorry. You guessed wrong, which caused your score to go negative.\n\nYou Lose! :(",
                            title="Incorrect Guess",
                            auto_close_duration=1)

                        # Set game state to inactive; break out of for loop
                        game_active = False
                        break
                    else:
                        # Notify user of incorrect guess
                        gui.popup_auto_close("You incorrectly guessed the letter \"" + guess + "\"\n\n(-1 score)",
                                             title="Incorrect Guess",
                                             auto_close_duration=1)

                # Update GUI to match game state
                game_window["word"].update("Word: " + get_censored_word(word, letters_guessed))
                game_window["score"].update("Score: " + str(score))
                game_window["input"].update("")
    game_window.close()
    return score


def main():
    """
    This program is designed to process text from a given data file, and extract its unique nouns. It will then use
    those unique nouns as words in a word guessing game, to which the user can play the game as much as they like.

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
    continue_playing = True
    score = 5
    high_score = 0
    while continue_playing:
        # Play the game
        score = guessing_game(common_words, score)
        high_score = score if high_score < score else high_score

        # Ask if the user wants to play again
        if score >= 0:
            # User won, Continue with previous score
            response = gui.popup_yes_no("You finished this guessing game with a score of " + str(score) +
                                        ". Your highest score was " + str(high_score) + ".\n\n" +
                                        "Would you like to continue playing?", title="Continue Playing?")
            # Process response. Assume Yes if response unexpected.
            if response == "No":
                continue_playing = False
        elif score == -100:
            # User closed window (special value). Close program.
            continue_playing = False
        else:
            # User lost, ask if they want to start again
            response = gui.popup_yes_no("You lost the game. Your highest score was " + str(high_score) + ".\n\n" +
                                        "Would you like to play again?", title="Play Again?")
            # Process response. Assume no if response unexpected.
            if response == "Yes":
                score = high_score = 5
            else:
                continue_playing = False

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
