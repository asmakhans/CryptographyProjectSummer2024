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


# Convert text to number based on alphabet chart mapping (e.g., 'A' to 0)
def text_to_num(text, letter_to_index):
    return [letter_to_index[char] for char in text]

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


# Create pairs from numerical values
def create_pairs(numbers):
    pairs = []
    # Iterate through the list of numbers in steps of 2
    for i in range(0, len(numbers), 2):
        pair = (numbers[i], numbers[i + 1])  # Create a pair using current and next element
        pairs.append(pair)  # Add each pair to the pairs list
    return pairs


# Encryption function using Hill 2-cipher
def encrypt(message, key, mod, letter_to_index, index_to_letter):
    # Convert the message to uppercase
    message = message.lower()

    # Pad the message if its length is odd
    if len(message) % 2 != 0:
        message += 'x'  # Padding with 'X' (assuming 'X' is not a frequent character in the message)

    # Convert the message to numerical values
    message_nums = text_to_num(message, letter_to_index)

    # Create pairs from the numerical values
    pairs = create_pairs(message_nums)

    encrypted_pairs = []
    for pair in pairs:
        # construct the pair as an array
        array = np.array(pair)

        # Multiply the key matrix with the vector
        encrypted_array = np.dot(key, array) % mod

        # convert to list and append to encrypted_pairs
        encrypted_pair = encrypted_array.tolist()
        encrypted_pairs.append(encrypted_pair)

    encrypted_nums = []
    for p in encrypted_pairs:
        for i in p:
            encrypted_nums.append(i)
    encrypted_text = numbers_to_text(encrypted_nums, index_to_letter)

    return encrypted_text


# Message to be encrypted
text = "TRYTOBREAKTHISCODE"

# Encrypt the message using key_26 and mod 26
print("Encrypted Message:", encrypt(text, key_26, 26, letter_to_index_26, index_to_letter_26))
