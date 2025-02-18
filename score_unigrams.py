# Write a function called score_unigrams that takes three arguments:
#   - a path to a folder of training data 
#   - a path to a test file that has a sentence on each line
#   - a path to an output CSV file
#
# Your function should do the following:
#   - train a single unigram model on the combined contents of every .txt file
#     in the training folder
#   - for each sentence (line) in the test file, calculate the log unigram 
#     probability ysing the trained model (see the lab handout for details on log 
#     probabilities)
#   - write a single CSV file to the output path. The CSV file should have two
#     columns with headers, called "sentence" and "unigram_prob" respectively.
#     "sentence" should contain the original sentence and "unigram_prob" should
#     contain its unigram probabilities.
#
# Additional details:
#   - there is training data in the training_data folder consisting of the contents 
#     of three novels by Jane Austen: Emma, Sense and Sensibility, and Pride and Prejudice
#   - there is test data you can use in the test_data folder
#   - be sure that your code works properly for words that are not in the 
#     training data. One of the test sentences contains the words 'color' (American spelling)
#     and 'television', neither of which are in the Austen novels. You should record a log
#     probability of -inf (corresponding to probability 0) for this sentence.
#   - your code should be insensitive to case, both in the training and testing data
#   - both the training and testing files have already been tokenized. This means that
#     punctuation marks have been split off of words. All you need to do to use the
#     data is to split it on spaces, and you will have your list of unigram tokens.
#   - you should treat punctuation marks as though they are words.
#   - it's fine to reuse parts of your unigram implementation from HW3.

# You will need to use log and -inf here. 
# You can add any additional import statements you need here.
from math import log, inf
from pathlib import Path
import csv

# In Corpus Linguistics, we would tokenize & run ngram counters using from nltk import ngrams. Is this something we'll be allowed to do eventually?


#######################
# YOUR CODE GOES HERE #
#######################


# Train the unigram model on contents in the training_data folder
    # Takes in the text files in the training data folder and returns a massive dictionary of probabilities of each unique token
def train_unigram_model(combined_lowercase_list): 
   
    training_folder = Path("training_data")  # Path to training_data folder

    combined_lowercase_list = [] # Creates an empty list for us to store the combined contents of each txt file in the training_data folder
    
    # For loop that goes through each txt file in the training_data folder and makes a massive list of tokens:
    for file_path in training_folder.glob("*.txt"): # Loops through each txt file in the training_data folder
        
        with file_path.open('r') as file: # Opens each file in read mode
            content = file.read() # Reads each file and stores in the content variable

        tokens_list = content.split() # Uses split function to make list of strings split on spaces

        # Another for loop that goes through each individual token in the combined list and converts it to lowercase, storing it in the combined_lowercase_list
        for token in tokens_list: # Loops through each string in the tokens list
            lowercase_token = token.lower() # Converts each individual token to lowercase
            combined_lowercase_list.append(lowercase_token) # Adds lowercase tokens to the empty list

    # Counts for unique tokens
    word_counts = {} # Creates an empty dictionary to store the counts of each instance of a unique word
    
    for word in combined_lowercase_list: # Goes through each word in the list of (now lowercase) tokens
        if word in word_counts: 
            word_counts[word] += 1 # If the word is already in the word counts dictionary, increase its count by one
        else: 
            word_counts[word] = 1 # If the word is not already in the dictionary, set it's starting count to one

    total_words = len(combined_lowercase_list) # Calculates the length of the combined lowercase tokens list (how many entries there are, so how many total words)

    # Calculating regular probabilities (will convert to log probabilities later)
    word_probabilities = {} # Creates an empty dictionary to store the probabilities of each word
    for word in word_counts: # Loops through each word in the dictionary of the words and their counts
        word_probabilities[word] = word_counts[word] / total_words # Divides each word's count by the total number of words, and puts this in the dictionary

    return word_probabilities # I want the function to return the dictionary of the words and their (regular) probabilities


# Now, I need to make a new function that takes the word probabilities and turns them into log probabilities
    # Takes in the dictionary of regular probabilities from above and returns log probabilities
def log_conversion(regular_probs): 

    log_probabilities = {} # Makes an empty dictionary to store the log probabilities

    for word, prob in regular_probs.items(): # Loops through each key value pair in the dictionary of regular probabilities
        if prob == 0: # I need this part to handle things like the words 'color' and 'television', which will later not have a probability
            log_probabilities[word] = -inf # This means that their log prob is thus assigned to -inf

        else: # In all other cases (when I have a regular probability that is not 0)
            log_probabilities[word] = log(prob) # Converts that regular prob to a log prob

    return log_probabilities # I want the function to return a dictionary of the the words and their log probabilities


# Now, I need to make a function that takes in the log probabilities of the training data and uses them to calculate a sentence score
def score_sentences(log_probabilities, test_file_path, output_path): 

    test_file = Path(test_file_path) # Will later plug in path to test_sentences text file
    output_csv = Path(output_path) # Will later plug in path to the csv file that the output will write to

    with test_file.open('r') as file: # Opens the file in read mode
        lines = file.readlines() # Returns a list of strings in which each string corresponds to a single line in the file

    results_list = [] # Makes an empty list to put the sentence scores in

    for line in lines: # Loops through each line in the file
        sentence = line.strip() # Removes the \n characters
        tokens = sentence.lower().split() # Splits the strings along the spaces and converts to lowercase

        sentence_log_prob = 0 # Starts off the sentence score probability at 0 so we can add to it (b/c logs)

        for token in tokens: # Loops through each token in the split, lowercased tokens
            if token in log_probabilities: # Checks if the token is in the log probabilities dictionary
                sentence_log_prob += log_probabilities[token] # If it is, add the log probability for that token
        
            else: 
                sentence_log_prob = -inf # If it's not, assign the probability to -inf
                break # I'm pretty sure I can put these here? Not so sure. Just to stop it after -inf

        data_dict = {} # Makes an empty dictionary for us to store our data
        # Defines the categories that we will later use in the csv file
        data_dict["sentence"] = sentence
        data_dict["unigram_prob"] = sentence_log_prob
        
        results_list.append(data_dict) # Add this info to our list

    with output_csv.open('w') as csvfile: # Creates the csv file for the results
        fieldnames = ["sentence", "unigram_prob"] # Creates the field names categories for the columns
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # Uses the csv.DictWriter tool from the csv library
        writer.writeheader() # Writes a row containing the field names
        writer.writerows(results_list) # Writes the dictionary to the csv rows

def score_unigrams(training_path, test_file_path, output_path): 

    word_probabilities = train_unigram_model(training_path) # Train the unigram model and get word probabilities

    word_log_probabilities = log_conversion(word_probabilities) # Convert the word probabilities into log probs

    score_sentences(word_log_probabilities, test_file_path, output_path) # Calculate the log sentence scores and write it to the csv file


# Calling the function (finally):
score_unigrams("training_data", "test_data/test_sentences.txt", "test_data/sentence_scores.csv")

# Results from this call: 
    # sentence,unigram_prob
    # "It was the best of times , it was the worst of times .",-73.42220869430832
    # There is no exquisite beauty without some strangeness in the proportion .,-84.09038166084301
    # We tell ourselves stories in order to live .,-65.50666393502672
    # Make it a rule never to give a child a book you would not read yourself .,-104.69385748118941
    # "The sky above the port was the color of television , tuned to a dead channel .",-inf

# Do not modify the following line
if __name__ == "__main__":
    # You can write code to test your function here
    pass 
