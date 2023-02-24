import os
import time
import hashlib
import base64
import math


# Length of name-based part of encrypting string (should be from 1 to 16).
PREFIX_LEN = 5
# Encrypted files' names will start with this prefix (ex.: UDPP_12345....jpg). Must end with '_'.
ENCRYPTED_NAME_PREFIX = 'UDPP_'
# Password to encrypt/decrypt files' manes. Use '' if you want a password to be asked.
PASSWORD = 'h51e#(x&k2fT'
# Path to working folder. Use '.' to work in script's folder, or '' if you want a path to be asked.
PATH = '.'
# Name of file to store the renaming results (files' names pairs). Must not be ''.
RESULTS_FILE_NAME = 'rename_results.txt'


# Write list to file safely
def write_To_File(file, mode, list):
    with open(file, mode) as f:
        for line in list:
            f.write(line + '\n')

# Generating encrypting string and calculating XOR


def extended_XOR(byte_string, password, encrypting_prefix):

    encrypting_len = math.ceil(len(byte_string) / 16)

    encrypting_string = hashlib.md5(
        ('0' + encrypting_prefix + password).encode()).digest()
    for i in range(1, encrypting_len):
        encrypting_string += hashlib.md5((str(i) +
                                         encrypting_prefix + password).encode()).digest()

    xored = []
    for i in range(len(byte_string)):
        xored.append(byte_string[i] ^ encrypting_string[i])

    return bytearray(xored)


# Encrypting string with given password, encrypting prefix length and name prefix
def encrypt_string(string, password, prefix_len, name_prefix):

    byte_string = string.encode()
    encrypting_prefix = ''.join(hashlib.md5(
        byte_string).hexdigest())[:prefix_len]

    encrypted_bytes = extended_XOR(byte_string, password, encrypting_prefix)

    encrypted_name = name_prefix + encrypting_prefix + \
        base64.b64encode(encrypted_bytes, altchars=b'-#').decode()

    return encrypted_name


# Decrypting string with given password, encrypting and name prefixes lengths
def decrypt_string(string, password, encrypting_prefix_len, name_prefix):

    if string[:len(name_prefix)] != name_prefix:
        return "$E"

    encrypting_prefix = string[encrypting_prefix_len:
                               encrypting_prefix_len + len(name_prefix)]
    encrypted_string = base64.b64decode(
        string[encrypting_prefix_len + len(name_prefix):].encode(), altchars=b'-#')

    decrypted_name = extended_XOR(
        encrypted_string, password, encrypting_prefix).decode()

    return decrypted_name


# Reading input values and executing recursive files' names encrypting in given path
def filename_encrypt(name):
    (base, ext) = os.path.splitext(name)
    new_name = encrypt_string(
        base, PASSWORD, PREFIX_LEN, ENCRYPTED_NAME_PREFIX) + ext
    return new_name


if __name__ == "__main__":
    filename_encrypt()
