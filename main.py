import string

import numpy as np

# assign each element(letter) into its corresponding indexed value(starting from 0)
alphabet_mod26 = 'abcdefghijklmnopqrstuvwxyz'
alphabet_mod29 = 'abcdefghijklmnopqrstuvwxyz ?!'  # this includes _ ? !

index = range(len(alphabet_mod26)) #char in alphabet_mod26
# index_29 = range(len(alphabet_mod29))

# letter_to_index = dict(zip(index, alphabet_mod26))
# we need for letter to index to return an array, so let's make this into a function that goes throguh each char in the text
# this is where we need to return an array, since at the moment it is only returning a value of 1

# index_to_letter = dict(zip(alphabet_mod26, index))
# this part will be a bit more complicated since we have to return a .join version of the array according to the mappings of the index

# matrices for encryption
key_26 = np.array([[6, 11], [25, 15]])
key_29 = np.array([[28, 7], [19, 18]])


# function for the encrypting thing using 2-Hill Cipher
def encrypt(message, key, mod):
    # checking if text length is even
    # if not even, then pad
    if len(message) % 2 != 0:
        message += 'x'
    message.lower()

    # mapping
    # letter_to_index = dict(zip(index, alphabet_mod26)) # A: 0
    letter_to_index = dict(enumerate(alphabet_mod26, 0))


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












