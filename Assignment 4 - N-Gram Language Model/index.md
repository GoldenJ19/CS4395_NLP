# **Assignment 4 - N-Gram Language Model**

This assignment involved creating language models for a few languages, and using the models to predict the language being used in different lines of a text file using a probablistic approach. Specifically, this is done using Laplace smoothing.

*Run Instructions:* 
- Open command prompt into the directory where the .py file is. 
- Use the command 'python BuildLM.py' first. This will run the program that builds the Language Models, and should take a couple of minutes to complete. 
    - You can edit the program to change the data folder location, and names of the files to use. 
- Use the command 'python EvaluateLM.py' after running the first program. This will use the files generated by the first program to classify/predict language off of the test file in the /data folder. 
    - You can edit the program to change the data and output folder location, as well as the names of the files to use. 
    - Note that the program is hard-coded to assume that the languages we're classifying are English, French, and Italian. If using different languages, the code will need to be changed to reflect that. 

*Notable File(s):* 
- [Overview](/NGrams.pdf) 
- [Code - Build Language Model](/BuildLM.py) 
- [Code - Evaluate Language Model](/EvaluateLM.py)
- [Data - Train (English)](/data/LangId.train.English)
- [Data - Train (French)](/data/LangId.train.French)
- [Data - Train (Italian)](/data/LangId.train.Italian)
- [Data - Test](/data/LangId.test)
- [Data - Solutions](/data/LangId.sol)