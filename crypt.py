import string
import numpy as np
from sympy import Matrix
from collections import Counter

# Assign each element (letter) into its corresponding indexed value (starting from 0)
alphabet_mod26 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_mod29 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ?!'  # this includes space, ?, and !

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
    text = "".join(index_to_letter[n] for n in numbers)
    return text


# Convert text to number based on alphabet chart mapping (e.g., 'a' to 0)
def text_to_num(text, letter_to_index):
    text = text.upper()  # make it all input text to uppercase to avoid any confusion
    return [letter_to_index[char] for char in text]


# Create bigrams from numerical values
def create_bigrams(numbers):
    bigrams = []

    # Pad the message if its length is odd
    if len(numbers) % 2 != 0:
        numbers.append(letter_to_index_26['X'])

    # Iterate through the list of numbers in steps of 2 since we're creating bigrams
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


def mod_inv(matrix, mod):
    matrix = Matrix(matrix)
    matrix_mod_inv = matrix.inv_mod(mod)
    return np.array(matrix_mod_inv).astype(int)


# suggested approach: sovle the linear system for key matrix using only the top 2 bigrams of 'th' and 'he'
def find_key_matrix(two_bigrams, expected_bigrams, mod):
    # take list of bigrams and converts each bigram to a list  so like converts the list of lists into an array
    bigram_vec = np.array(
        [list(bigram) for bigram in two_bigrams]).T  # .T transponses: swaps the rows and cols of the array
    result_vec = np.array([list(bigram) for bigram in expected_bigrams]).T

    bigram_matrix = Matrix(bigram_vec).T
    result_matrix = Matrix(result_vec).T
    print(bigram_matrix)
    # now we need to find the mod inverse of the bigram matrix
    bigram_matrix_inverse = bigram_matrix.inv_mod(mod)

    # Find the key matrix by multiplying the inverse of the bigram matrix with the result matrix
    key_matrix = (bigram_matrix_inverse * result_matrix) % mod

    return np.array(key_matrix).astype(int)  # cast to int


# just like how we convert from num to text and text to num, convert letter bigrams to numerical bigrams
def bigram_to_num(bigram, letter_to_index):
    return [letter_to_index[bigram[0]], letter_to_index[bigram[1]]]


english_bigram_frequencies = ['TH', 'HE']


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
def decrypt(text, key, mod, letter_to_index, index_to_letter):
    # Convert text to numerical values
    text_nums = text_to_num(text, letter_to_index)

    # Create bigrams from the numerical values
    bigrams = create_bigrams(text_nums)

    # Get the inverse of the key matrix modulo the specified modulus
    key_inv = mod_inv(key, mod)
    print(key_inv)

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


# UNCOMMENT OUT FOR QUESTION 1, currently commented out to make sure question 2 errors are different than q1
# Encrypt the message using key_26 and mod 26, then with key_29 and mod 29
message_to_encrypt = "TRYTOBREAKTHISCODE"  # len = 18
first_encrypt = encrypt(message_to_encrypt, key_26, 26, letter_to_index_26, index_to_letter_26)
final_encrypt = encrypt(first_encrypt, key_29, 29, letter_to_index_29, index_to_letter_29)
print("Encrypted Message:", final_encrypt)

# Decrypt the message using key_29 and mod 29, then with key_26 and mod 26
message_to_decrypt = "LYNY JRVMQNS JL ! "  # len = 18
first_decrypt = decrypt(message_to_decrypt, key_29, 29, letter_to_index_29, index_to_letter_29)
final_decrypt = decrypt(first_decrypt, key_26, 26, letter_to_index_26, index_to_letter_26)
print("Decrypted Message:", final_decrypt)


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
