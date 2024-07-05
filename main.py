import string
import numpy as np

# assign each element(letter) into its corresponding indexed value(starting from 0)
alphabet_mod26 = 'abcdefghijklmnopqrstuvwxyz'
alphabet_mod29 = 'abcdefghijklmnopqrstuvwxyz ?!'  # this includes _ ? !

# create empty dictionaries
letter_to_index_26 = {}
index_to_letter_26 = {}

# iterate through the dictionaries and fill them up with the mappings of the alphabet
# uses a for loop to map each letter to its index and vice versa
for index, letter in enumerate(alphabet_mod26):
    letter_to_index_26[letter] = index
    index_to_letter_26[index] = letter

# index = range(len(alphabet_mod26)) #char in alphabet_mod26
# index_29 = range(len(alphabet_mod29))

# letter_to_index = dict(zip(index, alphabet_mod26))
# we need for letter to index to return an array, so let's make this into a function that goes throguh each char in the text
# this is where we need to return an array, since at the moment it is only returning a value of 1

# index_to_letter = dict(zip(alphabet_mod26, index))
# this part will be a bit more complicated since we have to return a .join version of the array according to the mappings of the index

# matrices for encryption
key_26 = np.array([[6, 11], [25, 15]])
key_29 = np.array([[28, 7], [19, 18]])

# convert text to number based on alphabet chart mapping so like 'A' to 0
def text_to_num(text, letter_to_index):
    return [letter_to_index[char] for char in text]

def numbers_to_text(numbers, index_to_letter):
    # start an empty string to build return
    text = ""
    # iterate through all the numbers
    for n in numbers:
        letter = index_to_letter[n] #converting each number to its letter using the index to letter dictionary
        text += letter # concatenate the letter to the return

    return text

# create pairs from numerical values
def to_pairs(numbers):
    pairs = []

    #iterate thorugh list of nums by 2
    for i in range(0, len(numbers), 2):
        pair = (numbers[i], numbers[i + 1]) # creates a pair using curr and curr + 1
        pairs.append(pair) # add each pair to the pairs list

    return pairs

# function for the encrypting thing using 2-Hill Cipher
def encrypt(message, key, mod, letter_to_index, index_to_letter):
    message.lower()
    # checking if text length is even
    # if not even, then pad
    if len(message) % 2 != 0:
        message += 'x'

    # mapping
    # letter_to_index = dict(zip(index, alphabet_mod26)) # A: 0
    # letter_to_index = dict(enumerate(alphabet_mod26, 0))

    # convert message to nums
    message_to_num = text_to_num(message, letter_to_index)
    #create pairs of 2 from nums
    pairs = to_pairs(message_to_num)

    encrypted = []
    for pair in pairs:
        ve

    # MOVE THIS FOR LOOP INTO ITS OWN FUNCTION
    # example: 13671
    for i in range(0, len(letter_to_index), 2):
        # block = np.array(letter_to_index[i:i+2])
        block = np.array([letter_to_index]).reshape(-1, 2).T
        # print(block)
        # atp: 13 67 1x
        # dot product of the arrays (using the key and the newly created blocks) then modded to either 26 or 29
        encrypted = np.dot(key, block) % mod

    encrypted_to_text = dict(zip(encrypted, index)) # confused here
    return encrypted_to_text


text = "TRYTOBREAKTHISCODE"
print(encrypt(text, key_26, 26))












