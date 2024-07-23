import string
import numpy as np

# Assign each element (letter) into its corresponding indexed value (starting from 0)
alphabet_mod26 = 'abcdefghijklmnopqrstuvwxyz'
alphabet_mod29 = 'abcdefghijklmnopqrstuvwxyz ?!'  # this includes _ ? !

# Create empty dictionaries
letter_to_index_26 = {}
index_to_letter_26 = {}

# Iterate through the dictionaries and fill them up with the mappings of the alphabet
for index, letter in enumerate(alphabet_mod26):
    letter_to_index_26[letter] = index
    index_to_letter_26[index] = letter

# Matrices for encryption
key_26 = np.array([[6, 11], [25, 15]])
# key_29 = np.array([[28, 7], [19, 18]])

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


# Convert text to number based on alphabet chart mapping (e.g., 'A' to 0)
def text_to_num(text, letter_to_index):
    return [letter_to_index[char] for char in text]

# Create bigrams from numerical values
def create_bigrams(numbers):
    bigrams = []
    # Iterate through the list of numbers in steps of 2
    for i in range(0, len(numbers), 2):
        pair = (numbers[i], numbers[i + 1])  # Create a pair using current and next element
        bigrams.append(pair)  # Add each bigram to the bigrams list
    return bigrams


# Frequency analysis of the bigrams from an intercepted encrypted message
def frequency_analysis(encrypted_message):
    encrypted_bigrams = create_bigrams(encrypted_message)
    total_bigrams = len(encrypted_bigrams) - 1
    frequency = {}

    # Counts how many times each pair occurs within the encrypted message
    for bigram in encrypted_bigrams:
        if bigram in frequency:
            frequency[bigram] += 1
        else:
            frequency[bigram] = 1

    # Calculate the frequency of each pair as a percentage
    frequency_percentage = {}
    for bigram, number_of_bigrams in frequency.items():
        frequency_percentage[bigram] = (number_of_bigrams / total_bigrams) * 100

    # Sort the frequency_percent dictionary by frequency in descending order
    sorted_frequency_percent = dict(sorted(frequency_percentage.items(), key=lambda item: item[1], reverse=True))

    return sorted_frequency_percent

    # create "Frequency of Character bigrams in English Language Text" dictionary
    # compare frequency_percentage to "Frequency of Character bigrams in English Language Text" dictionary
    # assign like bigrams together?


# Encryption function using Hill 2-cipher
def encrypt(message, key, mod, letter_to_index, index_to_letter):
    # Convert the message to uppercase
    message = message.lower()

    # Pad the message if its length is odd
    if len(message) % 2 != 0:
        message += 'x'  # Padding with 'X' (assuming 'X' is not a frequent character in the message)

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


# Message to be encrypted
text = "TRYTOBREAKTHISCODE"

# Encrypt the message using key_26 and mod 26
print("Encrypted Message:", encrypt(text, key_26, 26, letter_to_index_26, index_to_letter_26))

# Encrypted file
with open('/mnt/data/encrypted-message.txt', 'r') as file:
    encrypted_message = file.read().strip()

frequency_analysis(encrypted_message)
print("Decrypted Message:", decrypt(text, key_26, 26, letter_to_index_26, index_to_letter_26))
