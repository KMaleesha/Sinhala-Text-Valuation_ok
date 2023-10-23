import pandas as pd
import difflib

# Read data
df = pd.read_excel('DataSet.xlsx')


def find_most_similar_word(input_word, word_list):
    similarities = difflib.get_close_matches(input_word, word_list)
    return similarities[0] if similarities else None


def find_different_letters(input_word, similar_word):
    differences = []
    for char1, char2 in zip(input_word, similar_word):
        if char1 != char2:
            differences.append(char1)
    return ''.join(differences)


# Input word
input_word = input("Please enter the word: ")
most_similar_word = find_most_similar_word(input_word, df['words'])

if most_similar_word:
    # Find different letters
    different_letters = find_different_letters(input_word, most_similar_word)
    print("User Input:", input_word)
    print("Most Match:", most_similar_word)

else:
    print("No similar word found in the dataset.")


user_input = input_word
candidate_words = [most_similar_word]


# Function to find differing letters
def find_differing_letters(input_word, candidate_word):
    differing_letters = list(difflib.ndiff(input_word, candidate_word))
    differing_letters = [char[2] for char in differing_letters if char[0] != ' ']
    return ''.join(differing_letters)

# Initialize variables to track the most matching word and its differing letters
most_matching_word = None
differing_letters = None

for candidate_word in candidate_words:
    candidate_differing_letters = find_differing_letters(user_input, candidate_word)
    if differing_letters is None or len(candidate_differing_letters) < len(differing_letters):
        differing_letters = candidate_differing_letters
        most_matching_word = candidate_word

if differing_letters:
    print(f"Differing Letters: {differing_letters}")
    # Differentiating stage here
else:
    print("No differing letters found.")


#--------------xxxxx
# Input word and letter
input_word = most_similar_word
input_letter = differing_letters

# Find the first row
row = df[df['words'] == input_word].iloc[0]

initial_position = None
middle_position = None
final_position = None

if input_letter in row['initial']:
    initial_position = row['initial'].index(input_letter)

if input_letter in row['middle']:
    middle_position = row['middle'].index(input_letter)

if input_letter in row['final']:
    final_position = row['final'].index(input_letter)

# Print
if initial_position is not None:
    print("Position: initial")
if middle_position is not None:
    print("Position: middle")
if final_position is not None:
    print("Position: final")

# Check if differing_letter is not None before getting its length
if differing_letters is not None:
    differing_letter_count = len(differing_letters)
    print(f"Number of Different Letters: {differing_letter_count}")
else:
    print("No differing letter found.")
