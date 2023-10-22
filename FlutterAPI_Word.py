import pandas as pd
import difflib
from flask import Flask, request, jsonify

# Read data
df = pd.read_excel('DataSet.xlsx')

app = Flask(__name__)

def find_most_similar_word(input_word, word_list):
    similarities = difflib.get_close_matches(input_word, word_list)
    return similarities[0] if similarities else None

def find_different_letters(input_word, similar_word):
    differences = []
    for char1, char2 in zip(input_word, similar_word):
        if char1 != char2:
            differences.append(char1)
    return ''.join(differences)

@app.route('/API_Word', methods=['POST'])
def compare_words():
    try:
        data = request.get_json()
        input_word = data['input_word']

        most_similar_word = find_most_similar_word(input_word, df['words'])

        if most_similar_word:
            different_letters = find_different_letters(input_word, most_similar_word)
            user_input = input_word
            candidate_words = [most_similar_word]

            def find_differing_letters(input_word, candidate_word):
                differing_letters = list(difflib.ndiff(input_word, candidate_word))
                differing_letters = [char[2] for char in differing_letters if char[0] != ' ']
                return ''.join(differing_letters)

            most_matching_word = None
            differing_letters = None

            for candidate_word in candidate_words:
                candidate_differing_letters = find_differing_letters(user_input, candidate_word)
                if differing_letters is None or len(candidate_differing_letters) < len(differing_letters):
                    differing_letters = candidate_differing_letters
                    most_matching_word = candidate_word

            if differing_letters:
                position_info = []
                input_word = most_matching_word
                input_letter = differing_letters
                row = df[df['words'] == input_word].iloc[0]

                if input_letter in row['initial']:
                    position_info.append("Position: initial")
                if input_letter in row['middle']:
                    position_info.append("Position: middle")
                if input_letter in row['final']:
                    position_info.append("Position: final")

                differing_letter_count = len(differing_letters)
                position_info.append(f"Number of Different Letters: {differing_letter_count}")

                return jsonify({
                    "User Input": input_word,
                    "Most Match": most_matching_word,
                    "Differing Letters": differing_letters,
                    "Position Info": position_info
                })

        return jsonify({"message": "No similar word found in the dataset."})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
