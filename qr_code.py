# Generate a valid QR code as a 2D array of 1s and 0s

# STEPS:
# 1. Choose appropriate encoding, size and error correction level (assuming BYTE and Q for now)
# 2. Encode the message string into a binary sequence
# 3. Interleave and add error correction codes
# 4. Place function patterns on the grid
# 5. TODO Add data bits to the grid
# 6. TODO Apply best mask
# 7. TODO Add format and version information (version info is done)

# encoding modes - only actually implementing BYTE
from reed_solomon import ec_codewords
from visualiser import draw_grid

NUMERIC = 1
ALPHANUMERIC = 2
BYTE = 4

# error correction levels TODO - is this the only ordering? I have a feeling it is LMHQ in a few places
L = 0
M = 1
Q = 2
H = 3

MODULE_WHITE = 0
MODULE_BLACK = 1
MODULE_EMPTY = 8

total_codewords = [
    [19, 34, 55, 80, 108, 136, 156, 194, 232, 274, 324, 370, 428, 461, 523, 589, 647, 721, 795, 861, 932, 1006, 1094,
     1174, 1276, 1370, 1468, 1531, 1631, 1735, 1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956, ],  # L
    [16, 28, 44, 64, 86, 108, 124, 154, 182, 216, 254, 290, 334, 365, 415, 453, 507, 563, 627, 669, 714, 782, 860, 914,
     1000, 1062, 1128, 1193, 1267, 1373, 1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334, ],  # M
    [13, 22, 34, 48, 62, 76, 88, 110, 132, 154, 180, 206, 244, 261, 295, 325, 367, 397, 445, 485, 512, 568, 614, 664,
     718, 754, 808, 871, 911, 985, 1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666, ],  # Q
    [9, 16, 26, 36, 46, 60, 66, 86, 100, 122, 140, 158, 180, 197, 223, 253, 283, 313, 341, 385, 406, 442, 464, 514, 538,
     596, 628, 661, 701, 745, 793, 845, 901, 961, 986, 1054, 1096, 1142, 1222, 1276, ]]  # H

ec_codewords_per_block = [
    [7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, ],
    [10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28,
     28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, ],
    [13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, ],
    [17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, ]]

group1_blocks = [
    [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 4, 2, 4, 3, 5, 5, 1, 5, 3, 3, 4, 2, 4, 6, 8, 10, 8, 3, 7, 5, 13, 17, 17, 13, 12, 6,
     17, 4, 20, 19, ],
    [1, 1, 1, 2, 2, 4, 4, 2, 3, 4, 1, 6, 8, 4, 5, 7, 10, 9, 3, 3, 17, 17, 4, 6, 8, 19, 22, 3, 21, 19, 2, 10, 14, 14, 12,
     6, 29, 13, 40, 18, ],
    [1, 1, 2, 2, 2, 4, 2, 4, 4, 6, 4, 4, 8, 11, 5, 15, 1, 17, 17, 15, 17, 7, 11, 11, 7, 28, 8, 4, 1, 15, 42, 10, 29, 44,
     39, 46, 49, 48, 43, 34, ],
    [1, 1, 2, 4, 2, 4, 4, 4, 4, 6, 3, 7, 12, 11, 11, 3, 2, 2, 9, 15, 19, 34, 16, 30, 22, 33, 12, 11, 19, 23, 23, 19, 11,
     59, 22, 2, 24, 42, 10, 20, ]]

data_codewords_in_group1 = [
    [19, 34, 55, 80, 108, 68, 78, 97, 116, 68, 81, 92, 107, 115, 87, 98, 107, 120, 113, 107, 116, 111, 121, 117, 106,
     114, 122, 117, 116, 115, 115, 115, 115, 115, 121, 121, 122, 122, 117, 118, ],
    [16, 28, 44, 32, 43, 27, 31, 38, 36, 43, 50, 36, 37, 40, 41, 45, 46, 43, 44, 41, 42, 46, 47, 45, 47, 46, 45, 45, 45,
     47, 46, 46, 46, 46, 47, 47, 46, 46, 47, 47, ],
    [13, 22, 17, 24, 15, 19, 14, 18, 16, 19, 22, 20, 20, 16, 24, 19, 22, 22, 21, 24, 22, 24, 24, 24, 24, 22, 23, 24, 23,
     24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, ],
    [9, 16, 13, 9, 11, 15, 13, 14, 12, 15, 12, 14, 11, 12, 12, 15, 14, 14, 13, 15, 16, 13, 15, 16, 15, 16, 15, 15, 15,
     15, 15, 15, 15, 16, 15, 15, 15, 15, 15, 15, ]]

group2_blocks = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 1, 1, 1, 5, 1, 4, 5, 4, 7, 5, 4, 4, 2, 4, 10, 7, 10, 3, 0, 1, 6, 7, 14, 4,
     18, 4, 6, ],
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 4, 2, 1, 5, 5, 3, 1, 4, 11, 13, 0, 0, 14, 14, 13, 4, 3, 23, 7, 10, 29, 23, 21, 23,
     26, 34, 14, 32, 7, 31, ],
    [0, 0, 0, 0, 2, 0, 4, 2, 4, 2, 4, 6, 4, 5, 7, 2, 15, 1, 4, 5, 6, 16, 14, 16, 22, 6, 26, 31, 37, 25, 1, 35, 19, 7,
     14, 10, 10, 14, 22, 34, ],
    [0, 0, 0, 0, 2, 0, 1, 2, 4, 2, 8, 4, 4, 5, 7, 13, 17, 19, 16, 10, 6, 0, 14, 2, 13, 4, 28, 31, 26, 25, 28, 35, 46, 1,
     41, 64, 46, 32, 67, 61, ]]

data_codewords_in_group2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 69, 0, 93, 0, 116, 88, 99, 108, 121, 114, 108, 117, 112, 122, 118, 107, 115, 123, 118,
     117, 116, 116, 0, 116, 116, 122, 122, 123, 123, 118, 119, ],
    [0, 0, 0, 0, 0, 0, 0, 39, 37, 44, 51, 37, 38, 41, 42, 46, 47, 44, 45, 42, 0, 0, 48, 46, 48, 47, 46, 46, 46, 48, 47,
     47, 47, 47, 48, 48, 47, 47, 48, 48, ],
    [0, 0, 0, 0, 16, 0, 15, 19, 17, 20, 23, 21, 21, 17, 25, 20, 23, 23, 22, 25, 23, 25, 25, 25, 25, 23, 24, 25, 24, 25,
     25, 25, 25, 25, 25, 25, 25, 25, 25, 25, ],
    [0, 0, 0, 0, 12, 0, 14, 15, 13, 16, 13, 15, 12, 13, 13, 16, 15, 15, 14, 16, 17, 0, 16, 17, 16, 17, 16, 16, 16, 16,
     16, 16, 16, 17, 16, 16, 16, 16, 16, 16, ]]


def generate_qr_code(message):
    encoding = _choose_encoding(message)
    ec_level = _choose_ec_level(message)
    version = _choose_smallest_version(message, encoding, ec_level)
    # encode the message
    message_codewords = _encode(message, ec_level, version)

    # interleave and add ec
    combined_data = _interleave_with_ec(message_codewords, ec_level, version)

    # create the grid and place the function patterns
    grid = _create_grid_with_function_patterns(version)

    # convert the codewords to binary and add to the grid
    sequence = []
    for word in combined_data:
        sequence.extend(_binary_sequence(word, 8))
    # add remainder bits, depending on version
    if version > 1:
        sequence.extend([0] * [7, 0, 3, 4, 3, 0][version // 7])

    grid, module_path = _add_data_modules(grid, sequence)

    # apply masking, format and version info
    grid = _apply_mask(grid, module_path, ec_level)

    return grid


def _choose_encoding(message):
    return BYTE


def _choose_ec_level(message):
    return Q


def _choose_smallest_version(message, encoding, ec):
    # max character capacities of each QR version indexed as [error correction][version][encoding]
    # error correction = LMQH 0 - 3
    # version = v1 - v40 as 0 - 39
    # encoding = numeric / alpha / byte 0 - 2
    encoding_index = {NUMERIC: 0, ALPHANUMERIC: 1, BYTE: 2}
    qr_capacity = [[  # L error correction
        [41, 25, 17], [77, 47, 32], [127, 77, 53], [187, 114, 78], [255, 154, 106],
        [322, 195, 134], [370, 224, 154], [461, 279, 192], [552, 335, 230], [652, 395, 271],
        [772, 468, 321], [883, 535, 367], [1022, 619, 425], [1101, 667, 458], [1250, 758, 520],
        [1408, 854, 586], [1548, 938, 644], [1725, 1046, 718], [1903, 1153, 792], [2061, 1249, 858],
        [2232, 1352, 929], [2409, 1460, 1003], [2620, 1588, 1091], [2812, 1704, 1171], [3057, 1853, 1273],
        [3283, 1990, 1367], [3517, 2132, 1465], [3669, 2223, 1528], [3909, 2369, 1628], [4158, 2520, 1732],
        [4417, 2677, 1840], [4686, 2840, 1952], [4965, 3009, 2068], [5253, 3183, 2188], [5529, 3351, 2303],
        [5836, 3537, 2431], [6153, 3729, 2563], [6479, 3927, 2699], [6743, 4087, 2809], [7089, 4296, 2953]
    ], [  # M error correction
        [34, 20, 14], [63, 38, 26], [101, 61, 42], [149, 90, 62], [202, 122, 84],
        [255, 154, 106], [293, 178, 122], [365, 221, 152], [432, 262, 180], [513, 311, 213],
        [604, 366, 251], [691, 419, 287], [796, 483, 331], [871, 528, 362], [991, 600, 412],
        [1082, 656, 450], [1212, 734, 504], [1346, 816, 560], [1500, 909, 624], [1600, 970, 666],
        [1708, 1035, 711], [1872, 1134, 779], [2059, 1248, 857], [2188, 1326, 911], [2395, 1451, 997],
        [2544, 1542, 1059], [2701, 1637, 1125], [2857, 1732, 1190], [3035, 1839, 1264], [3289, 1994, 1370],
        [3486, 2113, 1452], [3693, 2238, 1538], [3909, 2369, 1628], [4134, 2506, 1722], [4343, 2632, 1809],
        [4588, 2780, 1911], [4775, 2894, 1989], [5039, 3054, 2099], [5313, 3220, 2213], [5596, 3391, 2331]
    ], [  # Q error correction
        [27, 16, 11], [48, 29, 20], [77, 47, 32], [111, 67, 46], [144, 87, 60], [178, 108, 74],
        [207, 125, 86], [259, 157, 108], [312, 189, 130], [364, 221, 151], [427, 259, 177],
        [489, 296, 203], [580, 352, 241], [621, 376, 258], [703, 426, 292], [775, 470, 322],
        [876, 531, 364], [948, 574, 394], [1063, 644, 442], [1159, 702, 482], [1224, 742, 509],
        [1358, 823, 565], [1468, 890, 611], [1588, 963, 661], [1718, 1041, 715], [1804, 1094, 751],
        [1933, 1172, 805], [2085, 1263, 868], [2181, 1322, 908], [2358, 1429, 982], [2473, 1499, 1030],
        [2670, 1618, 1112], [2805, 1700, 1168], [2949, 1787, 1228], [3081, 1867, 1283], [3244, 1966, 1351],
        [3417, 2071, 1423], [3599, 2181, 1499], [3791, 2298, 1579], [3993, 2420, 1663]
    ], [  # H error correction
        [17, 10, 7], [34, 20, 14], [58, 35, 24], [82, 50, 34], [106, 64, 44], [139, 84, 58],
        [154, 93, 64], [202, 122, 84], [235, 143, 98], [288, 174, 119], [331, 200, 137],
        [374, 227, 155], [427, 259, 177], [468, 283, 194], [530, 321, 220], [602, 365, 250],
        [674, 408, 280], [746, 452, 310], [813, 493, 338], [919, 557, 382], [969, 587, 403],
        [1056, 640, 439], [1108, 672, 461], [1228, 744, 511], [1286, 779, 535], [1425, 864, 593],
        [1501, 910, 625], [1581, 958, 658], [1677, 1016, 698], [1782, 1080, 742], [1897, 1150, 790],
        [2022, 1226, 842], [2157, 1307, 898], [2301, 1394, 958], [2361, 1431, 983], [2524, 1530, 1051],
        [2625, 1591, 1093], [2735, 1658, 1139], [2927, 1774, 1219], [3057, 1852, 1273]
    ]]
    v = 0
    while qr_capacity[ec][v][encoding_index[encoding]] < len(message):
        v += 1
    return v + 1  # version numbers are 1-40


# apply the patterns for alignment, timing etc
def _create_grid_with_function_patterns(version):
    size = (version - 1) * 4 + 21
    grid = []
    for row in range(size):
        grid.append([MODULE_EMPTY] * size)

    # 1. The finder patterns are the three blocks in the corners of the
    # QR code at the top left, top right, and bottom left.
    for finder_y, finder_x in [[0, 0], [size - 7, 0], [0, size - 7]]:
        for i in range(7):
            for j in range(7):
                # this complicated boolean condition generates the concentric finder pattern
                grid[finder_y + i][finder_x + j] = int((i not in [1, 5] or j in [0, 6])
                                                       and (i in [0, 6] or j not in [1, 5]))

        # 2. The separators are areas of whitespace beside the finder patterns, on the inner edges only.
        for i in range(8):
            grid[i][7] = grid[i][size - 8] = \
                grid[size - i - 1][7] = grid[7][i] = grid[7][size - i - 1] = grid[size - 8][i] = 0

    # 3. The alignment patterns are similar to finder patterns, but smaller, and are placed throughout the code.
    # They are used in versions 2 and larger, and their positions depend on the QR code version.
    alignment_locations = [
        [], [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50],
        [6, 30, 54], [6, 32, 58], [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], [6, 30, 54, 78],
        [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], [6, 28, 50, 72, 94], [6, 26, 50, 74, 98],
        [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110], [6, 30, 58, 86, 114], [6, 34, 62, 90, 118],
        [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126], [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134],
        [6, 34, 60, 86, 112, 138], [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146], [6, 30, 54, 78, 102, 126, 150],
        [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158], [6, 32, 58, 84, 110, 136, 162],
        [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]
    ]
    for row in alignment_locations[version]:
        for col in alignment_locations[version]:
            # add alignment pattern at row i, col j, provided this doesn't overlap a finder
            overlap = False
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if grid[row + i][col + j] != MODULE_EMPTY:
                        overlap = True
            if not overlap:
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        grid[row + i][col + j] = int(i * 5 + j not in [-6, -5, -4, -1, 1, 4, 5, 6])

    # 4. reserve space for the format information, which goes in 4 strips around the separators
    # this also takes care of the permanently black module in the top-right corner of the bottom finder pattern
    for i in range(8):
        grid[8][i] = grid[8][size - i - 1] = grid[i][8] = grid[size - i - 1][8] = MODULE_BLACK
    grid[8][8] = MODULE_BLACK  # single square missed by the loop

    # 5. The timing patterns are dotted lines that connect the finder patterns.
    # This always starts and ends with a black module
    for i in range(8, size - 8, 2):
        # horizontal pattern
        grid[6][i] = MODULE_BLACK
        grid[6][i + 1] = MODULE_WHITE
        # vertical pattern
        grid[i][6] = MODULE_BLACK
        grid[i + 1][6] = MODULE_WHITE

    # 6. For versions 7 and above, version info is added in two 6x3 blocks
    # above the bottom-left finder pattern and to the left of the top-right finder pattern
    version_info_strings = [
        "000111110010010100", "001000010110111100", "001001101010011001", "001010010011010011",
        "001011101111110110", "001100011101100010", "001101100001000111", "001110011000001101",
        "001111100100101000", "010000101101111000", "010001010001011101", "010010101000010111",
        "010011010100110010", "010100100110100110", "010101011010000011", "010110100011001001",
        "010111011111101100", "011000111011000100", "011001000111100001", "011010111110101011",
        "011011000010001110", "011100110000011010", "011101001100111111", "011110110101110101",
        "011111001001010000", "100000100111010101", "100001011011110000", "100010100010111010",
        "100011011110011111", "100100101100001011", "100101010000101110", "100110101001100100",
        "100111010101000001", "101000110001101001"
    ]
    if version >= 7:
        version_info = version_info_strings[version-7]
        bit_counter = len(version_info) - 1
        for j in range(6):
            for i in range(3):
                grid[size - 11 + i][j] = grid[j][size - 11 + i] = int(version_info[bit_counter])
                bit_counter -= 1

    return grid


# convert the message string into a list of 1s and 0s using the chosen encoding method
def _encode(message, ec, version):
    # this assumes BYTE encoding throughout
    sequence = [0, 1, 0, 0]  # 1st 4 bits are the encoding mode (4 for BYTE)
    # number of bits used to encode the length of the message depends on the version (and encoding)
    if version < 10:
        sequence.extend(_binary_sequence(len(message), 8))
    else:
        sequence.extend(_binary_sequence(len(message), 16))
    # now encode the data itself and append
    # BYTE mode uses ISO-8859-1 (Latin-1, which is basically ASCII)
    for char in message:
        sequence.extend(_binary_sequence(ord(char), 8))
    # add terminator bits to fill out the required codewords, or 4 bits, whichever is smaller
    required_bits = total_codewords[ec][version - 1] * 8  # bytes to bits
    sequence.extend([0] * min(required_bits, 4))
    # pad with 0s to take the number of bits to a multiple of 8
    sequence.extend([0] * (len(sequence) % 8))
    # pad with alternating 236 & 17 binary sequences to match the required total data codewords
    padding = [236, 17]
    for i in range((required_bits - len(sequence)) // 8):
        sequence.extend(_binary_sequence(padding[i % 2], 8))
    # split the sequence into 8-bit codewords
    codewords = [int(''.join(str(bit) for bit in sequence[i:i + 8]), 2) for i in range(0, len(sequence), 8)]
    return codewords


# returns a denary number in binary, as a list of 1s and 0s
def _binary_sequence(n, bits):
    return [int(digit) for digit in bin(n)[2:].zfill(bits)]


# structure the data into interleaved blocks and add the interleaved error codes after them
def _interleave_with_ec(codewords, ec_level, version):
    # split the codewords into blocks
    g1_blocks = group1_blocks[ec_level][version - 1]
    g2_blocks = group2_blocks[ec_level][version - 1]
    g1_words = data_codewords_in_group1[ec_level][version - 1]
    g2_words = data_codewords_in_group2[ec_level][version - 1]
    data_blocks = [codewords[i * g1_words:(i + 1) * g1_words] for i in range(g1_blocks)]
    data_blocks.extend([codewords[g1_words * g1_blocks + i * g2_words:(g1_words * g1_blocks) + (i + 1) * g2_words]
                        for i in range(g2_blocks)])

    # generate ec codewords for each block
    ec_blocks = []
    for block in data_blocks:
        ec_blocks.append(ec_codewords(block, ec_codewords_per_block[ec_level][version - 1]))

    # interleave everything
    interleaved = []
    word_count = 0
    i = 0
    # data from both groups
    while word_count < total_codewords[ec_level][version - 1]:
        for block_count in range(len(data_blocks)):
            if i < len(data_blocks[block_count]):
                interleaved.append(data_blocks[block_count][i])
                word_count += 1
        i += 1

    # ec codes
    for j in range(ec_codewords_per_block[ec_level][version - 1]):
        for block_count in range(len(ec_blocks)):
            interleaved.append(ec_blocks[block_count][j])

    return interleaved


# add the data bits in a specific zig-zag pattern
# see https://www.thonky.com/qr-code-tutorial/module-placement-matrix#step-6-place-the-data-bits
# whenever any non-empty squares are encountered, simply continue on to the next empty square along the path.
def _add_data_modules(grid, sequence):
    size = len(grid)  # assumes square
    row = col = size - 1  # start in the bottom right corner
    direction = -1  # -1 is up, +1 is down
    square_number = 0
    placement_path = [MODULE_EMPTY]*len(sequence)

    for i in range(len(sequence)):
        grid[row][col] = sequence[i]  # place the next bit in the binary sequence at this square
        placement_path[i] = row * size + col
        # move to the next unoccupied square on the grid (except if we are on the last module)
        while i < len(sequence) - 1 and grid[row][col] != MODULE_EMPTY:
            if square_number % 2 == 0:
                col -= 1
            else:
                col += 1
                row += direction
                if row < 0 or row >= size:  # reverse direction at the top and bottom edges
                    direction = -direction
                    row += direction  # reposition at the start of the next column
                    col -= 2
                    if col == 6:  # skip over the timing pattern on col 6
                        col -= 1
            square_number += 1
    return grid, placement_path

def _add_format(grid, ec_level, mask_number):
    # see https://www.thonky.com/qr-code-tutorial/format-version-information
    format_strings = {
        L: ["111011111000100", "111001011110011", "111110110101010", "111100010011101",
            "110011000101111", "110001100011000", "110110001000001", "110100101110110"],
        M: ["101010000010010", "101000100100101", "101111001111100", "101101101001011",
            "100010111111001", "100000011001110", "100111110010111", "100101010100000"],
        Q: ["011010101011111", "011000001101000", "011111100110001", "011101000000110",
            "010010010110100", "010000110000011", "010111011011010", "010101111101101"],
        H: ["001011010001001", "001001110111110", "001110011100111", "001100111010000",
            "000011101100010", "000001001010101", "000110100001100", "000100000111011"]
    }
    size = len(grid)
    # select the right pattern and convert to list
    format_bits = [int(f) for f in format_strings[ec_level][mask_number]]
    print(format_strings[ec_level][mask_number])
    for i in range(0, 6):  # bits 0-5 and 9-14 are placed in a nice regular way
        grid[8][i] = grid[size-i-1][8] = format_bits[i]  # bits 0-5
        grid[5 - i][8] = grid[8][size - 6 + i] = format_bits[i+9]  # bits 9-14

    # bits 6-8 must be placed separately because of the timing strips getting in the way
    grid[8][7] = grid[size-7][8] = format_bits[6]
    grid[8][8] = grid[8][size-8] = format_bits[7]
    grid[7][8] = grid[8][size-7] = format_bits[8]

    return grid


def _apply_mask(grid, placement_path, ec_level):
    # create an array of lambda functions, 1 for each mask rule
    masks = [lambda row, column: ((row + column) % 2) == 0,  # mask 0
             lambda row, column: (row % 2) == 0,  # mask  1
             lambda row, column: (column % 3) == 0,  # mask 2
             lambda row, column: ((row + column) % 3) == 0,  # mask 3
             lambda row, column: ((row / 2 + column / 3) % 2) == 0,  # mask 4
             lambda row, column: (((row * column) % 2) + ((row * column) % 3)) == 0,  # mask 5
             lambda row, column: (((row * column) % 2) + ((row * column) % 3)) % 2 == 0,  # mask 6
             lambda row, column: (((row + column) % 2) + ((row * column) % 3)) % 2 == 0,  # mask 7
             ]

    # try each one to find which has the lowest penalty
    lowest_penalty = 99999  # arbitrarily large initial value
    best_mask = 0
    for m in [0]:  # DEBUG force mask to always 0
    #for m in range(len(masks)):
        masked_grid = [row[:] for row in grid]  # clone the grid

        # apply the format modules now, so they can be included in the penalty score
        masked_grid = _add_format(masked_grid, ec_level, m)

    for square_number in placement_path:
        row = square_number // len(grid)
        col = square_number % len(grid)
        if masks[m](row, col):  # check the current mask rule against this square on the grid
            masked_grid[row][col] = (masked_grid[row][col] + 1) % 2  # invert 1 and 0, if the rule applies

    # check the penalty
    penalty = _mask_penalty(masked_grid)
    if penalty < lowest_penalty:
        lowest_penalty = penalty
        best_mask = m

    # DEBUG
    print(''.join([str(i) for i in masked_grid[0]]), end=' ')
    print("mask", m, "penalty=", penalty)

    # clone the final mask back to the master grid
    return masked_grid

# score the grid using the QR code penalty rules
# see https://www.thonky.com/qr-code-tutorial/data-masking#the-four-penalty-rules
def _mask_penalty(grid):
    total = 0
    penalty = 0
    # rows
    for i in range(len(grid)):
        current_colour = grid[i][0]
        streak = 1
        for j in range(1, len(grid)):
            if grid[i][j] == current_colour and j < len(grid)-1:  # automatically break the streak at the end of the row
                streak += 1
            else:
                penalty += streak-2 if streak >= 5 else 0  # only add a penalty for streaks of 5 or more
                current_colour = grid[i][j]
                streak = 1

    # columns
    for i in range(len(grid)):
        current_colour = grid[0][i]
        streak = 1
        for j in range(1, len(grid)):
            if grid[j][i] == current_colour and j < len(grid)-1:
                streak += 1
            else:
                penalty += streak-2 if streak >= 5 else 0  # only add a penalty for streaks of 5 or more
                current_colour = grid[j][i]
                streak = 1
    print("Penalty 1:", penalty)  # DEBUG
    total += penalty

    return total
