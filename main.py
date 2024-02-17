# Generate QR codes
# ported from my Java project

from enum import Enum
Module = Enum('Module', ['BLACK', 'WHITE'])
EncodingMode = Enum('EncodingMode',
                    ['NUMERIC',
                    'ALPHANUMERIC',
                    'BYTE',
                    'KANJI',
                    'ECI'])
encoding_mode_value = {EncodingMode.NUMERIC: 1,
                       EncodingMode.ALPHANUMERIC: 2,
                       EncodingMode.BYTE: 4,
                       EncodingMode.KANJI: 8,
                       EncodingMode.ECI: 7}
EC_level = Enum('EC_level', ['L', 'M', 'Q', 'H'])  # might be better as a dict

# return the qr code for the text
# using the most appropriate parameters for encoding mode, error correction etc
# the code is returned as a 2D array of Module values
def qr_code(text):
    # Choose encoding mode
    encoding_mode = choose_encoding_mode(text)

    # TODO Choose error correction level
    error_correction = EC_level.Q

    # TODO Calculate required version to fit the data
    version = 1

    # TODO Encode the text
    data_codewords = encode(text, encoding_mode, version)

    # TODO Generate EC codes
    # TODO Combine data and EC codewords
    # TODO Generate grid
    # TODO Apply masking
    # TODO Add format and version info
    # TODO return completed grid
    return data_codewords

# return a list of 8-bit codewords using the specified encoding mode
def encode(text, mode, version):
    bit_sequence = []
    # append encoding mode value as a 4-bit value
    bit_sequence = to_bit_array(encoding_mode_value[mode], 4)

    # next is the length of the data in bytes
    # for version 1 - 9 and alphanumeric mode, 9 bits are reserved for this
    # eg "hello world" is 11 bytes, so 000001011 in 9-bit binary
    bit_sequence.extend(to_bit_array(len(text),
                                     number_of_length_bits(version, mode)));
    return bit_sequence

# convert an int to an array of '1's and '0's representing the binary
def to_bit_array(n, bits):
    return list(format(n, '#0'+str(bits+2)+'b')[2:])

# return the most space-efficient mode for the input string
# only selects from NUMERIC, ALPHANUMERIC or BYTE
# KANJI and ECI are considered out of scope for now
def choose_encoding_mode(text):
    # optimistically assume all 3 are possible to begin with
    is_numeric = True
    is_alpha = True
    i = 0
    while i<len(text) and (is_numeric or is_alpha):
        if text[i] not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:":
            is_alpha = False
        if text[i] not in "0123456789":
            is_numeric = False
        i += 1
    # return the smallest encoding that matches
    if is_numeric:
        return EncodingMode.NUMERIC
    elif is_alpha:
        return EncodingMode.ALPHANUMERIC
    else:
        return EncodingMode.BYTE

# return the number of bits used to encode the length of the data
def number_of_length_bits(version, mode):
    lookup = [
        # v1-9
        {EncodingMode.NUMERIC: 10,
         EncodingMode.ALPHANUMERIC: 9,
         EncodingMode.BYTE: 8},
        # v10-26
        {EncodingMode.NUMERIC: 12,
         EncodingMode.ALPHANUMERIC: 11,
         EncodingMode.BYTE: 16},
        # v27-40
        {EncodingMode.NUMERIC: 14,
         EncodingMode.ALPHANUMERIC: 13,
         EncodingMode.BYTE: 16}]
    if version <10:
        return lookup[0][mode]
    elif version <27:
        return lookup[1][mode]
    else:
        return lookup[2][mode]

    # output grid to the screen
# just printing as a text grid for now
# TODO replace with pygame or turtle later
def display(qr_grid):
    error = False
    for row in qr_grid:
        for cell in row:
            if cell==Module.BLACK:
                print('#', end='')
            elif cell==Module.WHITE:
                print(' ', end='')
            else:
                print('!', end='')
                error = True
        print()
    if error:
        print("ERROR: Invalid modules!")

# generate a known QR code to validate
if __name__ == '__main__':
    print(qr_code('HELLO WORLD'))  # just for testing intermediate steps
    print(choose_encoding_mode('HELLO WORLD'))
    print(choose_encoding_mode('HELLO 123'))
    print(choose_encoding_mode('123'))
    print(choose_encoding_mode('@@@'))
    print(choose_encoding_mode('HELLO@1 WORLD'))
    # display(qr_code("HELLO WORLD"))  # display the grid
