"""

Names: Justin Hardy, Benji Frenkel
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import os
import json
import pickle
import pandas
import math
import sys
import re as regex
import random
from pandas import DataFrame
from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Define global variables
data_folder = "data"
kb_file = "kb.json"
pickled_model_r = "chatbot_model.p"
pickled_model_w = pickled_model_r
exit_inputs = ["exit", "leave", "quit"]
stop_words = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 1))


class UserModel:
    def __init__(self, name: str, likes: dict[str, list[str]] = {}, dislikes: dict[str, list[str]] = {},
                 life_info: list[str] = []):
        self.name = name
        self.likes = likes
        self.dislikes = dislikes
        self.life_info = life_info


def read_knowledge_base(path: str):
    """
    Reads the knowledge base from the given file path. Terminates program if the file doesn't exist, or if the
    knowledge base file is not a json file

    :param path: File path of the knowledge base. Loc of python file acts as working directory.
    :return: The raw knowledge base data, the knowledge base's tags and patterns in a data frame, and the knowledge
    base's tags mapped to responses in a dictionary
    """
    if not os.path.exists(path):
        print('ERROR: Knowledge Base not detected.')
        print('Please verify that the data folder and knowledge base file names are correct in the globals.')
        print('Terminating Program...')
        exit(1)

    # Check if knowledge base is a json file
    if '.json' not in kb_file.lower():
        print('Error: Knowledge Base is not of file type JSON...cannot read.')
        print('Terminating Program...')
        exit(2)

    # Load json
    kb_input = open(path, 'r')
    kb_raw = json.load(kb_input)
    kb_input.close()

    # Adjust KB pointer if applicable
    if kb_raw['kb']:
        kb_raw = kb_raw['kb']

    # Map tags to responses in dictionary
    responses = {tag['tag']: tag['responses'] for tag in kb_raw}

    # Remove specific tag(s) from training
    kb_raw = [tag for tag in kb_raw if 'conversation_replies' not in tag['tag']]

    # Put KB tags and patterns into dataframe
    kb = DataFrame(
        {
            'tags': [tag['tag'] for tag in kb_raw],
            'patterns': [' | '.join(tag['patterns']) for tag in kb_raw]
        }
    )

    # Return KB
    return kb_raw, kb, responses


def preprocess_inputs(df: DataFrame):
    """
    Preprocesses the input data frame. Creates train variables for the model, and vectorizes the predictor.

    :param df:
    :return:
    """
    # Convert tags to categorical representation
    tags_list = list(df.tags)
    tag_encoding = {tag: tag for tag in list(df.tags)}  # encoding
    df.tags = df.tags.astype('category').cat.codes  # conversion

    # Map tag category codes to actual tag names (for response retrieval later)
    tag_encoding = {df.tags.loc[i]: tags_list[i] for i in range(len(tags_list))}

    # Get vectorizer
    global vectorizer

    # Set x and y variables
    x_train = df.patterns
    y_train = df.tags

    # Vectorize x
    x_train = vectorizer.fit_transform(x_train)

    # Return contents
    return tag_encoding, x_train, y_train


def train_model(x_train, y_train):
    """
    Creates a logistic regression model using the provided training data.

    :param x_train: Training data for the predictors
    :param y_train: Training data for the target
    :return:
    """
    # Create LR Model
    model = LogisticRegression(solver='liblinear', random_state=66, max_iter=200)
    model.fit(x_train, y_train)
    return model


def word_untokenize(tokens: list):
    """
    NOTE: This function is not authored by me. This is a function retrieved from a public github repository, available
    at the following link:

    https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py

    All credits go to the members of the GitHub Organization, CommonSense.

    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(tokens)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = regex.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = regex.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


def negate_sentence(sentence: str):
    # Tokenize sentence
    tokenized_sentence = word_tokenize(sentence)
    rebuilt_tokenized_sentence = []

    antonym_next = False
    for token in tokenized_sentence:
        # print("parsing:", token)
        if token in ["'t", "n't"]:
            antonym_next = True
            rebuilt_tokenized_sentence.pop()
        elif antonym_next:
            synsets = wn.synsets(token)
            antonym = None
            for synset in synsets:
                if antonym is None:
                    lemmas = synset.lemmas()
                    for lemma in lemmas:
                        antonyms = lemma.antonyms()
                        if len(antonyms) > 0:
                            antonym = antonyms[0]
            if antonym:
                rebuilt_tokenized_sentence.append(antonym.name())
                antonym_next = False
        else:
            rebuilt_tokenized_sentence.append(token)
    return word_untokenize(rebuilt_tokenized_sentence)


def find_topic(text: str):
    # Tokenize the text
    lower_text = 'i ' + text.lower()
    tokenized_text = word_tokenize(lower_text)

    # POS tag the tokenized text
    # print(tokenized_text) # debug
    tagged_text = pos_tag(tokenized_text)
    # print(tagged_text)  # debug

    # Choose first noun as topic
    noun: str = ''
    for tag in tagged_text:
        if ('NN' in tag[1] or 'VBG' in tag[1]) and not 'i' == tag[0]:
            noun = tag[0]
            break
    return noun


def format_response(response_text: str, user_input: str, responses: dict, user_model: UserModel):
    if "<topic>" in response_text:
        # Determine topic
        topic = find_topic(user_input)
        if topic != '':
            response_text = response_text.replace("<topic>", topic)
        else:
            return ''
    if "<remark>" in response_text:
        # Determine remark to make
        random_remark = random.randint(0, 2)
        if random_remark == 0 and len(user_model.life_info) > 0:
            chosen_remark = random.choice(user_model.life_info)
            response_text = response_text.replace("<remark>", "I recall you said, \"" + chosen_remark +
                                                  "\". Do you want to talk more about that?")
        elif random_remark == 1 and len(user_model.likes) > 0:
            chosen_tuple = random.choice(list(user_model.likes.items()))
            chosen_remark = random.choice(chosen_tuple[1])
            response_text = response_text.replace("<remark>", "I recall you said, \"" + chosen_remark +
                                                  "\" about " + chosen_tuple[0] + "." +
                                                  " Is there anything else that you like about it?")
        elif random_remark == 2 and len(user_model.dislikes) > 0:
            chosen_tuple = random.choice(list(user_model.dislikes.items()))
            chosen_remark = random.choice(chosen_tuple[1])
            response_text = response_text.replace("<remark>", "I recall you said, \"" + chosen_remark +
                                                  "\" about " + chosen_tuple[0] + "." +
                                                  " Is there anything else that you dislike about it?")
        else:
            response_text = response_text.replace("<remark>", "I don't think I've heard much about you"
                                                  + " yet. Anything you'd like to share?")
    if '<name>' in response_text:
        # Insert user's name
        response_text = response_text.replace("<name>", user_model.name)

    return response_text


def chatbot(model: LogisticRegression, responses: dict, tag_encoding: dict, user_name=""):
    """
    Starts a chat between the user and chatbot

    :return: Exit code (if applicable)
    """
    # initial vars
    global exit_inputs, vectorizer
    response = ""
    chat_history = []
    conversation_active = False

    # Ask for name
    user_name = ''
    while user_name == '':
        user_name = input("What is your name? (or type 'exit'):\n>").strip()
        if user_name.lower() in exit_inputs:
            exit(0)
    user_name = user_name.split(' ')[0]
    user_model = UserModel(user_name.title())
    file = os.path.join(data_folder, user_model.name + ".um")

    # Overwrite user model with existing one if saved
    if os.path.exists(file):
        user_model = pickle.load(open(file, 'rb'))
        print("Welcome back, " + user_model.name + "!")
    print()

    print("You are now in a chat session with the Poker Chatbot.")
    print("Ask it anything you want:")
    while True:
        # Print user response arrow, get response from input
        user_input = input(">")
        user_input_copy = user_input

        # Check if input is an exit response
        if user_input.lower() in exit_inputs:
            # Leave program
            print("Thank you for your time, " + user_model.name +
                  "! See you another time.")
            break

        # Negate sentence response
        user_input = negate_sentence(user_input)

        # Remove negation if sentence is very short
        if len(user_input.split(' ')) < 2:
            user_input = user_input_copy

        user_input_copy2 = user_input
        user_input = [user_input]

        # DEBUG print read-in user_input
        # print("Read:", user_input)

        # Vectorize response
        user_input = vectorizer.transform(user_input)

        # Predict tag off of vectorized response
        tag = model.predict(user_input)[0]

        # Get response from tags
        tag = tag_encoding.get(tag)
        response = responses.get(tag)
        response_index = random.randint(0, len(response) - 1)
        tag_og = tag

        # DEBUG print tag info
        # print(tag)

        # If conversational
        if conversation_active:
            # Parse response
            if '_confused' in tag:
                # Print clarification response
                print(response[response_index])
                print()
            elif '_no' in tag:
                # Print clarification response
                print(response[response_index])
                print()

                # Set conversation active to false (no longer expecting response, context doesn't matter anymore)
                conversation_active = False
            else:
                # Set tag to conversation_replies tag
                tag = "conversation_replies"

                # Get new response
                response = responses.get(tag)

                # Determine which set of responses to use
                recent_conversations = [chat_history.pop()]

                # Get recent conversation that isn't that of confusion
                while '_confused' in recent_conversations[len(recent_conversations) - 1][0]:
                    recent_conversations.append(chat_history.pop())

                # Pop non-confused conversation
                prompt = recent_conversations.pop()
                prompt_text, prompt_response, prompt_tag = prompt

                # Determine if it is a user model reply, or small talk response
                if '_interests' in prompt_tag or '_life' in prompt_tag or '_history' in prompt_tag \
                        or ('_howareyou' in prompt_tag and 'How about you' not in prompt_response):
                    # Use second set of responses
                    response = response[1]
                    response_index = random.randint(0, len(response) - 1)
                    response_to_print: str = format_response(response[response_index], user_input_copy2, responses, user_model)
                    if response_to_print == '':
                        # Had trouble determining topic, react with confusion.
                        conversation_active = False
                        tag = 'unknown'
                        response = responses.get(tag)
                        response_index = random.randint(0, len(response) - 1)
                        response_to_print = response[response_index]

                    # Print response
                    print(response_to_print)
                    print()

                    # Save info to user model
                    if '_interests' in prompt_tag:
                        # Determine interest topic
                        topic = find_topic(prompt_text)
                        topic = topic.lower()

                        # Save to interests dict
                        if '_like' in prompt_tag:
                            if topic in user_model.likes.keys():
                                # Add on to preexisting interest
                                user_model.likes[topic].append(user_input_copy)
                            else:
                                # Create new interest in interests dict
                                interests = [user_input_copy]
                                user_model.likes[topic] = interests
                        else:
                            if topic in user_model.dislikes.keys():
                                # Add on to preexisting interest
                                user_model.dislikes[topic].append(user_input_copy)
                            else:
                                # Create new interest in interests dict
                                interests = [user_input_copy]
                                user_model.dislikes[topic] = interests
                    elif '_history' in prompt_tag or '_howareyou' in prompt_tag:
                        tokenized_prompt_response = word_tokenize(prompt_response)
                        # print("parsing:", prompt_response)
                        if 'Is there anything else that you' in prompt_response:
                            # Determine topic and like/dislike
                            prompt_topic = tokenized_prompt_response[tokenized_prompt_response.index('about') + 1]
                            like = False if 'dislike about it' in prompt_response else True

                            # DEBUG
                            # print("detected topic:", prompt_topic, "like:", like)

                            if like:
                                # Add on to preexisting interest
                                user_model.likes[prompt_topic].append(user_input_copy)
                            else:
                                # Add on to preexisting interest
                                user_model.dislikes[prompt_topic].append(user_input_copy)
                        elif '_like' in tag_og or '_dislike' in tag_og:
                            # Need more info. Ask for like or dislike info
                            tag = tag_og
                            response = responses.get(tag)
                            response_index = random.randint(0, len(response) - 1)
                            response_to_print = format_response(response[response_index], user_input_copy2, responses, user_model)
                            if response_to_print == '':
                                # Had trouble determining topic, react with confusion.
                                conversation_active = False
                                tag = 'unknown'
                                response = responses.get(tag)
                                response_index = random.randint(0, len(response) - 1)
                                response_to_print = response[response_index]

                            # Print response
                            print(response_to_print)
                            print()

                            # Add user input and response to history
                            chat_history.append((user_input_copy2, response_to_print, tag))
                            continue
                        else:
                            # Save to life info list
                            user_model.life_info.append(user_input_copy)
                    else:
                        # Save to life info list
                        user_model.life_info.append(prompt_text)

                    # DEBUG
                    # print(user_model.likes)
                    # print(user_model.dislikes)
                    # print(user_model.life_info)

                else:
                    # Use first set of responses
                    response = response[0]
                    response_index = random.randint(0, len(response) - 1)

                    # Print response
                    print(response[response_index])
                    print()

                # Add conversations back to history
                chat_history.append(prompt)
                if recent_conversations.reverse():
                    for conversation in recent_conversations.reverse():
                        chat_history.append(conversation)

                # Set conversation active to false (no longer expecting response, context doesn't matter anymore)
                conversation_active = False

        elif 'conversation_' in tag and '_no' not in tag and '_confused' not in tag:
            # Set conversation active to true (expecting response, context matters)
            conversation_active = True

            # Get response
            response_to_print: str = format_response(response[response_index], user_input_copy2, responses, user_model)
            if response_to_print == '':
                # Had trouble determining topic, react with confusion.
                conversation_active = False
                tag = 'unknown'
                response = responses.get(tag)
                response_index = random.randint(0, len(response) - 1)
                response_to_print = response[response_index]

            # Print response
            print(response_to_print)
            print()

            # Add user input and response to history
            chat_history.append((user_input_copy2, response_to_print, tag))
            continue

        else:
            response_to_print: str = format_response(response[response_index], user_input_copy2, responses, user_model)
            if response_to_print == '':
                # Had trouble determining topic, react with confusion.
                conversation_active = False
                tag = 'unknown'
                response = responses.get(tag)
                response_index = random.randint(0, len(response) - 1)
                response_to_print = response[response_index]

            # Print response
            print(response_to_print)
            print()

        # Add user input and response to history
        chat_history.append((user_input_copy2, response[response_index], tag))

    # Save user model to file
    pickle.dump(user_model, open(file, 'wb'))

    # Return exit code 0
    return 0


def main():
    """
    Trains and Runs a Chatbot capable of holding conversations with, and informing, a user about poker.

    :return: exit code (0 = success, 1 = knowledge base not found, 2 = incorrect file type)
    """
    # Grab globals
    global data_folder, kb_file, pickled_model_r, pickled_model_w, vectorizer
    ml_model, kb, responses, tag_encoding = (None, None, None, None)

    # Check if user can use previously made model
    if os.path.exists(os.path.join(data_folder, pickled_model_r)):
        choice = ''
        while choice == '':
            choice = input("Detected previously made model. Use it? (Y/N)\n>").strip()

        if choice.lower() in ['y', 'ye', 'yes', 'yep', 'yeah']:
            ml_model, kb, responses, tag_encoding, vectorizer = pickle.load(open(os.path.join(data_folder, pickled_model_r), 'rb'))

            # Run chatbot
            exit(chatbot(ml_model, responses, tag_encoding))

    # Read kb json
    print("Reading KB...")
    path = os.path.join(data_folder, kb_file)
    kb_raw, kb, responses = read_knowledge_base(path)
    print("Done reading KB.")
    print()

    # Preprocess the inputs of the data frame
    print("Preprocessing inputs...")
    tag_encoding, x_train, y_train = preprocess_inputs(kb)
    print("Done preprocessing inputs.")
    print()

    # debug
    # print(kb.head())
    # print(tag_encoding)

    # Train the model
    print("Training model...")
    ml_model = train_model(x_train, y_train)
    print("Done training model.")
    print()

    # Write model to file
    print("Writing model to file...")
    pickle.dump((ml_model, kb, responses, tag_encoding, vectorizer), open(os.path.join(data_folder, pickled_model_w), "wb"))
    print("Done writing model to file.")
    print()

    # Run chatbot
    exit(chatbot(ml_model, responses, tag_encoding))


if __name__ == "__main__":
    main()
