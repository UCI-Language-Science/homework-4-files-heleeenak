# The file valence_data/winter_2016_senses_valence.csv contains data from an 
# experiment that asked people to provide valence ratings for words associated
# with each of the five senses (touch, taste, smell, sight, sound). The file has
# three columns: Word, Modality, and Val. Word contains the word, Modality the
# sensory modality, and Val contains the mean valence rating for that word,
# where higher valence corresponds to more positive emotional states.

# The question we'll try to answer is whether certain sensory modalities have 
# higher or lower mean valences than others.
# 
#  Write a function called get_mean_valence that takes a Path to a CSV file
#  as input. You can assume the file will be formatted as described above.
#  Your function should return a dictionary with keys corresponding to each
#  of the five modalities. The value for each key should be its mean valence
#  score across all of the words in the CSV file.

# The data are from the paper 
#
# Winter, B. (2016). Taste and smell words form an affectively loaded and emotionally
# flexible part of the English lexicon. Language, Cognition and Neuroscience, 31(8), 
# 975-988.

#######################
# YOUR CODE GOES HERE #
#######################

from pathlib import Path
import csv

# Goal: I want a dictionary with keys corresponding to each of the five modalities
    # The value for each key should be its mean valence score across all of the words in the CSV file
def get_mean_valence(csv_path): 

    valence_sums = {} # Makes an empty dictionary to store the sum of the valence ratings for each modality

    valence_counts = {} # Makes an emtpy dictionary to store the count of words for each modality

    with csv_path.open('r') as file: # Opens the csv file in read mode (later add the csv path)
        reader = csv.DictReader(file) # Uses the csv.DictWriter tool from the csv library (processes CSV files and gives it back in the form of a dictionary)

        for row in reader: # Loops through each row of the csv file
            modality = row["Modality"] # Assigns the modality variable to the values in the modality column
            # I need to convert each valence score to a float (b/c rn they are strings):
            valence_string = row["Val"] # Accesses the valence values (strings in the csv file)
            valence = float(valence_string) # Converts them to floats and assigns to valence variable

            if modality not in valence_sums: # Checks if the modality is NOT IN the valence sums dictionary already
                valence_sums[modality] = 0.0 # Sets the sum equal to 0 to start it off in the dict
                valence_counts[modality] = 0 # Also sets the count equal to 0 to start it off in that dict

            # Now that the counts have been initiated, we can add to them:
            valence_sums[modality] += valence # This adds the float numbers to the sum total
            valence_counts[modality] += 1 # This increases the total count by 1 each time

    mean_valence_scores = {} # Makes an empty dictionary for us to store the mean valence scores
    for modality in valence_sums: # Loops through each modality entry in the sum total
        mean_valence_scores[modality] = valence_sums[modality] / valence_counts[modality] # This calculates the mean valence for the modality by dividing the sum of its scores by the count of its occurrences

    return mean_valence_scores # I want this function to return the dictionary of the means


# Calling the function finally yippee!
csv_path = Path("valence_data/winter_2016_senses_valence.csv") # Defines the csv_path variable (referenced in the function) to the csv file we're using here
mean_valences = get_mean_valence(csv_path) # Calls function and stores result in variable
print(mean_valences) # Prints dictionary of means

# Results of this call: 
    # {'Touch': 5.534434953514705, 'Sight': 5.579663071651515, 'Taste': 5.808123902468085, 'Smell': 5.471011590119999, 'Sound': 5.405192706701493}

# This question was significantly easier than the unigram one. I think it's because I'm not used to making functions have a side effect of writing to a file rather than returning something, like this one

# Do not modify the following line
if __name__ == "__main__":
    # You can write code to test your function here
    pass 
