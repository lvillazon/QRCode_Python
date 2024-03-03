# Generate QR codes
# This is intended as a v2 attempt,
# based on what I have learned from my Java project
# but it is not intended as a straight port and will try to use more
# efficient table-driven algorithms

from enum import Enum
from reed_solomon import test

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


# generate a known QR code to validate
if __name__ == '__main__':
    print('Python QR Code generator')
    test()  # run test function