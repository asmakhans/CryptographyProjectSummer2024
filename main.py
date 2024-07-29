import string
from random import random
import numpy as np
from sympy import Matrix
from collections import Counter

# Create mappings
def create_mappings(alphabet):
    letter_to_index = {letter: index for index, letter in enumerate(alphabet)}
    index_to_letter = {index: letter for index, letter in enumerate(alphabet)}
    return letter_to_index, index_to_letter

# General function to handle encryption and decryption for any alphabet
def process_message(message, key, alphabet, encrypt_mode=True):
    letter_to_index, index_to_letter = create_mappings(alphabet)
    mod = len(alphabet)

    if encrypt_mode:
        return encrypt(message, key, mod, letter_to_index, index_to_letter, alphabet)
    else:
        return decrypt(message, key, mod, letter_to_index, index_to_letter, alphabet)

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
    text = text.upper() # Convert text to uppercase
    return [letter_to_index[char] for char in text]

# Create bigrams from numerical values
def create_bigrams(numbers, letter_to_index, alphabet):
    bigrams = []

    # Pad the message if its length is odd
    if len(numbers) % 2 != 0:
        # numbers.append(letter_to_index_26['x']) # Use numerical value of 'x' for padding
        padding_char = random.choice(alphabet)
        numbers.append(letter_to_index[padding_char])

    # Iterate through the list of numbers in steps of 2
    for i in range(0, len(numbers), 2):
        pair = (numbers[i], numbers[i + 1]) # Create a pair using current and next element
        bigrams.append(pair) # Add each bigram to the bigrams list

    return bigrams

frequency_percentages = {}
# Count frequency of each bigram from an intercepted encrypted message
def frequency_analysis(encrypted_message, mod, letter_to_index, alphabet):
    encrypted_nums = text_to_num(encrypted_message, letter_to_index)
    encrypted_bigrams = create_bigrams(encrypted_nums, letter_to_index, alphabet)
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
#
# # "Frequency of bigrams in English language" dictionary
# english_bigram_frequencies = {
#     'TH': 1.52, 'HE': 1.28, 'IN': 0.94, 'ER': 0.94, 'AN': 0.82, 'RE': 0.68, 'ND': 0.63, 'AT': 0.59,
#     'ON': 0.57, 'NT': 0.56, 'HA': 0.56, 'ES': 0.56, 'ST': 0.55, 'EN': 0.55, 'ED': 0.53, 'TO': 0.52,
#     'IT': 0.50, 'OU': 0.50, 'EA': 0.47, 'hi': 0.46, 'is': 0.46, 'or': 0.43, 'ti': 0.34, 'as': 0.33,
#     'te': 0.27, 'et': 0.19, 'ng': 0.18, 'of': 0.16, 'al': 0.09, 'de': 0.09, 'se': 0.08, 'le': 0.08,
#     'sa': 0.06, 'si': 0.05, 'ar': 0.04, 've': 0.04, 'ra': 0.04, 'ld': 0.02, 'ur': 0.02
#     # Add more bigrams if needed from other references
# }

plaintext_bigrams = {}
# Makes dictionary with plaintext bigrams
def plaintext(encrypted_message, mod, letter_to_index, alphabet):
    sorted_frequencies = frequency_analysis(encrypted_message, mod, letter_to_index, alphabet)

    sorted_plaintext_bigrams = {}
    # Used sorted_plaintext_bigrams and replaces key with the keys from english_bigram_frequencies
    for encrypted_frequency, english_bigram in zip(sorted_frequencies.values(), english_bigram_frequencies.keys()):
        sorted_plaintext_bigrams[english_bigram] = encrypted_frequency

    # make an array of the keys from sorted_plaintext_bigrams
    sorted_plaintext_keys = list(sorted_plaintext_bigrams.keys())
    frequency_percentages = sorted_frequencies  # Get the frequency percentages again
    # take the key values of frequency_percentages and pair them with the value of the sorted_plaintext_keys
    for index, key in enumerate(frequency_percentages.keys()):
        if index < len(sorted_plaintext_keys):
            new_key = sorted_plaintext_keys[index]
            plaintext_bigrams[new_key] = frequency_percentages[key]

    return plaintext_bigrams

def mod_inv(matrix, mod):
    matrix = Matrix(matrix)
    if not is_invertible(matrix, mod):
        raise ValueError("Matrix is not invertible under modulus", mod)
    matrix_mod_inv = matrix.inv_mod(mod)
    return np.array(matrix_mod_inv).astype(int)

# Check if matrix is invertible under given modulus
def is_invertible(matrix, mod):
    matrix = Matrix(matrix)
    det = matrix.det() % mod
    return det != 0 and greatest_common_divisor(det, mod) == 1

def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return a

# suggested approach: sovle the linear system for key matrix using only the top 2 bigrams of 'th' and 'he'
def find_key_matrix(two_bigrams, expected_bigrams, mod):
    # take list of bigrams and converts each bigram to a list  so like converts the list of lists into an array
    bigram_vec = np.array(
        [list(bigram) for bigram in two_bigrams]).T  # .T transponses: swaps the rows and cols of the array
    result_vec = np.array([list(bigram) for bigram in expected_bigrams]).T

    bigram_matrix = Matrix(bigram_vec).T
    result_matrix = Matrix(result_vec).T

    # now we need to find the mod inverse of the bigram matrix
    bigram_matrix_inverse = bigram_matrix.inv_mod(mod)

    # now that we have the inverse of the matrix, we can find the key matrix
    key_matrix = (result_matrix * bigram_matrix_inverse) % mod

    return np.array(key_matrix).astype(int)  # cast to int

# just like how we convert from num to text and text to num, convert letter bigrams to numerical bigrams
def bigram_to_num(bigram, letter_to_index):
    return [letter_to_index[bigram[0]], letter_to_index[bigram[1]]]


english_bigram_frequencies = ['TH', 'HE']

# Encryption function using Hill 2-cipher
def encrypt(message, key, mod, letter_to_index, index_to_letter, alphabet):
    if not is_invertible(key, mod):
        raise ValueError("Key matrix is not invertible under modulus", mod)

    # Convert the message to numerical values
    message_nums = text_to_num(message, letter_to_index)

    # Create bigrams from the numerical values
    bigrams = create_bigrams(message_nums, letter_to_index, alphabet)

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
def decrypt(text, key, mod, letter_to_index, index_to_letter, alphabet):
    if not is_invertible(key, mod):
        raise ValueError("Key matrix is not invertible under modulus", mod)

    # Convert text to numerical values
    text_nums = text_to_num(text, letter_to_index)

    # Create bigrams from the numerical values
    bigrams = create_bigrams(text_nums, letter_to_index, alphabet)

    # Get the inverse of the key matrix modulo the specified modulus
    key_inv = mod_inv(key, mod)

    decrypted_bigrams = []
    for bigram in bigrams:
        # Construct the pair as an array
        array = np.array(bigram)

        # Multiply the inverse key matrix with the vector and take modulo
        decrypted_array = np.dot(key_inv, array) % mod

        # Convert to list and append to decrypted_bigrams
        decrypted_bigram = decrypted_array.tolist()
        decrypted_bigrams.append(decrypted_bigram)

    decrypted_nums = []
    for p in decrypted_bigrams:
        for i in p:
            decrypted_nums.append(i)
    decrypted_text = numbers_to_text(decrypted_nums, index_to_letter)

    return decrypted_text


alphabet_mod26 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_mod29 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ?!'  # this includes space, ?, and !
letter_to_index_26, index_to_letter_26 = create_mappings(alphabet_mod26)
letter_to_index_29, index_to_letter_29 = create_mappings(alphabet_mod29)

# UNCOMMENT OUT FOR QUESTION 1, currently commented out to make sure question 2 errors are different than q1
# Encrypt the message using key_26 and mod 26, then with key_29 and mod 29
message_to_encrypt = "TRYTOBREAKTHISCODE"  # len = 18
first_encrypt = encrypt(message_to_encrypt, key_26, 26, letter_to_index_26, index_to_letter_26, alphabet_mod26)
final_encrypt = encrypt(first_encrypt, key_29, 29, letter_to_index_29, index_to_letter_29, alphabet_mod29)
print("Encrypted Message:", final_encrypt)

# Decrypt the message using key_29 and mod 29, then with key_26 and mod 26
message_to_decrypt = "LYNY JRVMQNS JL ! "  # len = 18
first_decrypt = decrypt(message_to_decrypt, key_29, 29, letter_to_index_29, index_to_letter_29, alphabet_mod29)
final_decrypt = decrypt(first_decrypt, key_26, 26, letter_to_index_26, index_to_letter_26, alphabet_mod26)
print("Decrypted Message:", final_decrypt)

print('\n')

# QUESTION 2:
with open('encrypted-message.txt', 'r') as file:
    encrypted_message = file.read().strip()

print("letter_to_index_26:", letter_to_index_26)

# Frequency analysis on intercepted message
frequency_data = frequency_analysis(encrypted_message, 26, letter_to_index_26)
top_bigrams = list(frequency_data.keys())[:2]
print("Top bigrams in encrypted file's message:", top_bigrams)

# Expected bigrams in plaintext
expected_bigrams = [bigram_to_num(bigram, letter_to_index_26) for bigram in english_bigram_frequencies]

# Find the key matrix
found_key_matrix = find_key_matrix(top_bigrams, expected_bigrams, 26)
print("Found Key Matrix:", found_key_matrix)

print('\n')

# QUESTION 3:
try:
    encrypted_message = process_message(message_to_encrypt, key_26, alphabet_mod26, encrypt_mode=True)
    print("Encrypted Message:", encrypted_message)

    # decrypted_message = process_message(encrypted_message, key_29, alphabet_29, encrypt_mode=False)
    # print("Decrypted Message:", decrypted_message)
except ValueError as e:
    print(f"Error: {e}")
