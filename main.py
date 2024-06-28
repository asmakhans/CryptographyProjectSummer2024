import numpy as np




a = input("Hello enter key value a: ")
b = input("Hello enter key value b: ")
c = input("Hello enter key value c: ")
d = input("Hello enter key value d: ")

f = open("encrypted-message.txt", "r")

cipher_key = np.array([[int(a), int(b)],
              [int(c), int(d)]])

testVal = np.array([[7],[8]])

cipher_key.shape
print(np.linalg.inv(cipher_key))

#print(f.read())
# print(u"!")
# print(u"?")
# print(ord("H"))
decipher_key = np.linalg.inv(cipher_key)
print(decipher_key)

def decrypt_msg (array, file):

    print(plain_txt)

def encrypt_msg (key, file):

    print(cipher_txt)