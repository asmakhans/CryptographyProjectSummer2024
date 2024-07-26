import string
import numpy as np
from sympy import Matrix
from collections import Counter

# Assign each element (letter) into its corresponding indexed value (starting from 0)
alphabet_mod26 = 'abcdefghijklmnopqrstuvwxyz'
alphabet_mod29 = 'abcdefghijklmnopqrstuvwxyz ?!'  # this includes space, ?, and !

# Create empty dictionaries
letter_to_index_26 = {}
index_to_letter_26 = {}

letter_to_index_29 = {}
index_to_letter_29 = {}

# Iterate through the dictionaries and fill them up with the mappings of the alphabet
for index, letter in enumerate(alphabet_mod26):
    letter_to_index_26[letter] = index
    index_to_letter_26[index] = letter

# Iterate through the dictionaries and fill them up with the mappings of the alphabet
for index, letter in enumerate(alphabet_mod29):
    letter_to_index_29[letter] = index
    index_to_letter_29[index] = letter

# Matrices for encryption
key_26 = np.array([[6, 11], [25, 15]])
key_29 = np.array([[28, 7], [19, 18]])

# Convert numbers back to text
def numbers_to_text(numbers, index_to_letter):
    # Start with an empty string to build the return value
    text = ""
    # Iterate through all the numbers
    for n in numbers:
        # Convert each number to its letter using the index_to_letter dictionary
        letter = index_to_letter[n]
        # Concatenate the letter to the return string
        text += letter
    return text

# Convert text to number based on alphabet chart mapping (e.g., 'a' to 0)
def text_to_num(text, letter_to_index):
    text = text.lower()  # Convert text to lowercase
    return [letter_to_index[char] for char in text]

# Create bigrams from numerical values
def create_bigrams(numbers):
    bigrams = []

    # Pad the message if its length is odd
    if len(numbers) % 2 != 0:
        numbers.append(letter_to_index_26['x'])  # Use numerical value of 'x' for padding

    # Iterate through the list of numbers in steps of 2
    for i in range(0, len(numbers), 2):
        pair = (numbers[i], numbers[i + 1])  # Create a pair using current and next element
        bigrams.append(pair)  # Add each bigram to the bigrams list
    return bigrams

frequency_percentages = {}
# Count frequency of each bigram from an intercepted encrypted message
def frequency_analysis(encrypted_message, mod, letter_to_index):
    encrypted_nums = text_to_num(encrypted_message, letter_to_index)
    encrypted_bigrams = create_bigrams(encrypted_nums)
    total_bigrams = len(encrypted_bigrams)
    frequency = {}

    # Counts how many times each pair occurs within the encrypted message
    for bigram in encrypted_bigrams:
        if bigram in frequency:
            frequency[bigram] += 1
        else:
            frequency[bigram] = 1

    # Calculate the frequencies of each pair as a percentage
    frequency_percentages = {bigram: round((count / total_bigrams) * 100, 2) for bigram, count in frequency.items()}

    # Sort the frequency_percentage dictionary by frequency in descending order
    sorted_frequency_percentages = dict(sorted(frequency_percentages.items(), key=lambda item: item[1], reverse=True))

    return sorted_frequency_percentages

# "Frequency of bigrams in English language" dictionary
english_bigram_frequencies = {
    'th': 1.52, 'he': 1.28, 'in': 0.94, 'er': 0.94, 'an': 0.82, 're': 0.68, 'nd': 0.63, 'at': 0.59,
    'on': 0.57, 'nt': 0.56, 'ha': 0.56, 'es': 0.56, 'st': 0.55, 'en': 0.55, 'ed': 0.53, 'to': 0.52,
    'it': 0.50, 'ou': 0.50, 'ea': 0.47, 'hi': 0.46, 'is': 0.46, 'or': 0.43, 'ti': 0.34, 'as': 0.33,
    'te': 0.27, 'et': 0.19, 'ng': 0.18, 'of': 0.16, 'al': 0.09, 'de': 0.09, 'se': 0.08, 'le': 0.08,
    'sa': 0.06, 'si': 0.05, 'ar': 0.04, 've': 0.04, 'ra': 0.04, 'ld': 0.02, 'ur': 0.02
    # Add more bigrams if needed from other references
}

plaintext_bigrams = {}
# Makes dictionary with plaintext bigrams
def plaintext(encrypted_message, mod, letter_to_index):
    sorted_frequencies = frequency_analysis(encrypted_message, mod, letter_to_index)

    sorted_plaintext_bigrams = {}
    # Used sorted_plaintext_bigrams and replaces key with the keys from english_bigram_frequencies
    for encrypted_frequency, english_bigram in zip(sorted_frequencies.values(), english_bigram_frequencies.keys()):
        sorted_plaintext_bigrams[english_bigram] = encrypted_frequency

    # make an array of the keys from sorted_plaintext_bigrams
    sorted_plaintext_keys = list(sorted_plaintext_bigrams.keys())
    # take the key values of frequency_percentages and pair them with the value of the sorted_plaintext_keys
    for index, key in enumerate(frequency_percentages.keys()):
        if index < len(sorted_plaintext_keys):
            new_key = sorted_plaintext_keys[index]
            plaintext_bigrams[new_key] = frequency_percentages[key]

    return plaintext_bigrams

def mod_inv(matrix, mod):
    matrix = Matrix(matrix)
    det = int(matrix.det())
    det_inv = pow(det, -1, mod)
    matrix_mod_inv = det_inv * matrix.inv_mod(mod)

    return np.array(matrix_mod_inv).astype(int)

# Fuction finds the key matrix using the encrypted message and the inverse of the plaintext
def find_key_matrix(mod):
    # inverse plaintext_bigrams
    plaintext_inv = mod_inv(plaintext_bigrams.keys()[:2], mod)
    key = np.dot(frequency_percentages.keys()[:2], plaintext_inv) % mod

    return key

# Encryption function using Hill 2-cipher
def encrypt(message, key, mod, letter_to_index, index_to_letter):
    # Convert the message to numerical values
    message_nums = text_to_num(message, letter_to_index)

    # Create bigrams from the numerical values
    bigrams = create_bigrams(message_nums)

    encrypted_bigrams = []
    for bigram in bigrams:
        # construct the pair as an array
        array = np.array(bigram)

        # Multiply the key matrix with the vector
        encrypted_array = np.dot(key, array) % mod

        # convert to list and append to encrypted_bigrams
        encrypted_bigram = encrypted_array.tolist()
        encrypted_bigrams.append(encrypted_bigram)

    encrypted_nums = []
    for p in encrypted_bigrams:
        for i in p:
            encrypted_nums.append(i)
    encrypted_text = numbers_to_text(encrypted_nums, index_to_letter)

    return encrypted_text

# Decrypt function using Hill 2-cipher
def decrypt():
    return

# Encrypt the message using key_26 and mod 26
message_to_encrypt = "TRYTOBREAKTHISCODE" # len = 18
print("Encrypted Message:", encrypt(message_to_encrypt, key_26, 26, letter_to_index_26, index_to_letter_26))

# Encrypt the message using key_29 and mod 29
message_to_decrypt = "LYNY JRVMQNS JL ! " # len = 18
# print("Decrypt Message:", decrypt(message_to_decrypt, key_29, 29, letter_to_index_29, index_to_letter_29))

# Encrypted file
with open('encrypted-message.txt', 'r') as file:
    intercepted_message = file.read().strip()
print(create_bigrams(text_to_num(intercepted_message, letter_to_index_26)))
print(frequency_analysis(intercepted_message, 26, letter_to_index_26), '\n')

print(plaintext(intercepted_message, 26, letter_to_index_26))
