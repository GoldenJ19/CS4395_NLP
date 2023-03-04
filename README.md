# **CS4395 - NLP**
## **Overview**

This is a repository (sub-portfolio) containing all the programs created for the class, Human Language Technologies (AKA Natural Language Processing) during my 4th year of college.

*Notable File(s):* 
- [Write-Up](Overview/Overview%20of%20NLP.pdf) 

## **Assignment 1 - Text Processing with Python**

This simple assignment involved processing through a text file using regex pattern checks. It also had us try out object creation and serialization in python.

You can view the assignment 1 directory [here](Assignment%201%20-%20Text%20Processing%20with%20Python).

*Run Instructions:* 
- Open command prompt into the directory where the .py file is.
- Use the command 'python TextProcessing.py data.csv' to run the program.
    - You can replace 'data.csv' with the path to any file of your choosing. It should follow a similar format as the provided data.csv file, though.

*Notable File(s):* 
- [Overview](Assignment%201%20-%20Text%20Processing%20with%20Python/TextProcessing.pdf)
- [Code](Assignment%201%20-%20Text%20Processing%20with%20Python/TextProcessing.py)

## **Assignment 2 - Word Guessing Game**

This assignment involved tokenizing words from a text file, extracting the nouns, and using the extracted nouns as words for a word guessing game. The preprocessing runs through the terminal, however I'd designed a simple GUI to play the word guessing game through.

You can view the assignment 2 directory [here](Assignment%202%20-%20Word%20Guessing%20Game).

*Run Instructions:*
- Open command prompt into the directory where the .py file is.
- Use the command 'python WordGuessingGame.py anat19.txt' to run the program.
    - You can replace 'anat19.txt' with the path to any file of your choosing. It should be a file that consists of various words and sentences.
- Once the preprocessing finishes, you can begin playing the word guessing game. Various details about the processed tokens will be outputted to the console, along with the words the game will be using (the top 50 ost commons nouns).

*Notable File(s):* 
- [Code](Assignment%202%20-%20Word%20Guessing%20Game/WordGuessingGame.py) 

## **Assignment 3 - WordNet**

This assignment involved exploring the WordNet and SentiWordNet APIs of the NLTK library. Specifically, we explore word relations/hierarchies, sentiment scoring, and collocation identification.

You can view the assignment directory [here](Assignment%203%20-%20WordNet).

*Notable File(s):* 
- [Overview](Assignment%203%20-%20WordNet/WordNet.pdf) 
- [Code](Assignment%203%20-%20WordNet/WordNet.ipynb) 

## **Assignment 4 - N-Gram Language Model**

This assignment involved creating language models for a few languages, and using the models to predict the language being used in different lines of a text file using a probablistic approach. Specifically, this is done using Laplace smoothing.

You can view the assignment directory [here](Assignment%204%20-%20N-Gram%20Language%20Model).

*Run Instructions:* 
- Open command prompt into the directory where the .py file is. 
- Use the command 'python BuildLM.py' first. This will run the program that builds the Language Models, and should take a couple of minutes to complete. 
    - You can edit the program to change the data folder location, and names of the files to use. 
- Use the command 'python EvaluateLM.py' after running the first program. This will use the files generated by the first program to classify/predict language off of the test file in the /data folder. 
    - You can edit the program to change the data and output folder location, as well as the names of the files to use. 
    - Note that the program is hard-coded to assume that the languages we're classifying are English, French, and Italian. If using different languages, the code will need to be changed to reflect that. 

*Notable File(s):* 
- [Overview](Assignment%204%20-%20N-Gram%20Language%20Model/NGrams.pdf) 
- [Code - Build Language Model](Assignment%204%20-%20N-Gram%20Language%20Model/BuildLM.py) 
- [Code - Evaluate Language Model](Assignment%204%20-%20N-Gram%20Language%20Model/EvaluateLM.py) 

## **Assignment 5 - Web Crawler**

TBD

*Notable File(s):* 
- TBD

## **Assignment 6 - TBD**

TBD.

*Notable File(s):* 
- TBD

## **Assignment 7 - TBD**

TBD.

*Notable File(s):* 
- TBD

## **Assignment 8 - TBD**

TBD.

*Notable File(s):* 
- TBD