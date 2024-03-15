# Generate Reed-Solomon error correction codes

# STEPS:
# 1. convert the message into a polynomial
#    where each byte is the coefficient of a different term
#    eg [84, 69, 83, 84] -> 84x^3 + 69x^2 + 83x + 84
#    The powers of x are represented as a bit field,
#    where a 1 means that this power is present, so 1111 in this case.
#    (1010101 would mean 84x^6 + 69x^4 + 83x^2 + 84)
#    So coefficients remain as a byte list and the powers as a bit string

# 2. Multiply message polynomial by x^number of EC codewords to make space
#    ie append as many zeros as you need need EC codewords

# 3. Divide the message using GF256 arithmetic

# 4. There should be exactly the right number of coefficients in the remainder
#    To supply the EC codewords, so simply return this list

# GLOBAL DATA TABLES
exp = (
1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38,
76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192,
157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35,
70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161,
95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240,
253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226,
217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206,
129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204,
133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84,
168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115,
230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255,
227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65,
130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166,
81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9,
18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22,
44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 0)

log = (
    "X", 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75,
    4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113,
    5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69,
    29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166,
    6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136,
    54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64,
    30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61,
    202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87,
    7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24,
    227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46,
    55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97,
    242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162,
    31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246,
    108, 161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90,
    203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215,
    79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175)

# old generators that used GF256 log tables with the wrong irreducible polynomial
# generators = {
#     7: {7: 1, 6: 127, 5: 123, 4: 226, 3: 201, 2: 13, 1: 80, 0: 115, },
#     10: {10: 1, 9: 180, 8: 169, 7: 230, 6: 110, 5: 173, 4: 77, 3: 76, 2: 118, 1: 229, 0: 171, },
#     13: {13: 1, 12: 241, 11: 91, 10: 155, 9: 16, 8: 220, 7: 16, 6: 39, 5: 11, 4: 58, 3: 62, 2: 70, 1: 250, 0: 120, },
#     15: {15: 1, 14: 26, 13: 175, 12: 110, 11: 206, 10: 119, 9: 89, 8: 12, 7: 104, 6: 104, 5: 242, 4: 250, 3: 233, 2: 51,
#          1: 249, 0: 29, },
#     16: {16: 1, 15: 47, 14: 11, 13: 105, 12: 214, 11: 80, 10: 186, 9: 24, 8: 15, 7: 206, 6: 84, 5: 61, 4: 157, 3: 101,
#          2: 33, 1: 54, 0: 47, },
#     17: {17: 1, 16: 112, 15: 86, 14: 70, 13: 120, 12: 112, 11: 23, 10: 174, 9: 70, 8: 134, 7: 61, 6: 247, 5: 249, 4: 64,
#          3: 38, 2: 124, 1: 100, 0: 93, },
#     18: {18: 1, 17: 145, 16: 133, 15: 218, 14: 118, 13: 234, 12: 196, 11: 173, 10: 188, 9: 136, 8: 177, 7: 91, 6: 71,
#          5: 199, 4: 88, 3: 51, 2: 87, 1: 181, 0: 237, },
#     20: {20: 1, 19: 225, 18: 211, 17: 136, 16: 4, 15: 110, 14: 100, 13: 6, 12: 177, 11: 119, 10: 232, 9: 81, 8: 54,
#          7: 208, 6: 23, 5: 156, 4: 172, 3: 121, 2: 121, 1: 200, 0: 197, },
#     22: {22: 1, 21: 74, 20: 223, 19: 253, 18: 221, 17: 219, 16: 141, 15: 19, 14: 214, 13: 81, 12: 60, 11: 27, 10: 241,
#          9: 26, 8: 122, 7: 87, 6: 131, 5: 66, 4: 183, 3: 159, 2: 29, 1: 239, 0: 140, },
#     24: {24: 1, 23: 123, 22: 113, 21: 194, 20: 83, 19: 222, 18: 146, 17: 180, 16: 96, 15: 117, 14: 232, 13: 157, 12: 91,
#          11: 252, 10: 90, 9: 41, 8: 62, 7: 163, 6: 1, 5: 146, 4: 143, 3: 127, 2: 181, 1: 238, 0: 115, },
#     26: {26: 1, 25: 142, 24: 32, 23: 218, 22: 5, 21: 240, 20: 101, 19: 173, 18: 225, 17: 94, 16: 45, 15: 163, 14: 30,
#          13: 239, 12: 60, 11: 186, 10: 115, 9: 151, 8: 63, 7: 248, 6: 80, 5: 83, 4: 238, 3: 237, 2: 94, 1: 62, 0: 77, },
#     28: {28: 1, 27: 130, 26: 14, 25: 27, 24: 11, 23: 18, 22: 133, 21: 187, 20: 232, 19: 97, 18: 197, 17: 99, 16: 61,
#          15: 203, 14: 10, 13: 143, 12: 45, 11: 115, 10: 112, 9: 151, 8: 127, 7: 217, 6: 99, 5: 121, 4: 236, 3: 221,
#          2: 89, 1: 46, 0: 174, },
#     30: {30: 1, 29: 190, 28: 142, 27: 94, 26: 91, 25: 168, 24: 170, 23: 88, 22: 101, 21: 4, 20: 83, 19: 97, 18: 220,
#          17: 23, 16: 181, 15: 243, 14: 32, 13: 217, 12: 142, 11: 90, 10: 31, 9: 18, 8: 58, 7: 156, 6: 89, 5: 180,
#          4: 168, 3: 13, 2: 106, 1: 252, 0: 232, },
# }
generators = {
7: {7: 1, 6: 127, 5: 122, 4: 154, 3: 164, 2: 11, 1: 68, 0: 117, },
10: {10: 1, 9: 216, 8: 194, 7: 159, 6: 111, 5: 199, 4: 94, 3: 95, 2: 113, 1: 157, 0: 193, },
13: {13: 1, 12: 137, 11: 73, 10: 227, 9: 17, 8: 177, 7: 17, 6: 52, 5: 13, 4: 46, 3: 43, 2: 83, 1: 132, 0: 120, },
15: {15: 1, 14: 29, 13: 196, 12: 111, 11: 163, 10: 112, 9: 74, 8: 10, 7: 105, 6: 105, 5: 139, 4: 132, 3: 151, 2: 32, 1: 134, 0: 26, },
16: {16: 1, 15: 59, 14: 13, 13: 104, 12: 189, 11: 68, 10: 209, 9: 30, 8: 8, 7: 163, 6: 65, 5: 41, 4: 229, 3: 98, 2: 50, 1: 36, 0: 59, },
17: {17: 1, 16: 119, 15: 66, 14: 83, 13: 120, 12: 119, 11: 22, 10: 197, 9: 83, 8: 249, 7: 41, 6: 143, 5: 134, 4: 85, 3: 53, 2: 125, 1: 99, 0: 79, },
18: {18: 1, 17: 239, 16: 251, 15: 183, 14: 113, 13: 149, 12: 175, 11: 199, 10: 215, 9: 240, 8: 220, 7: 73, 6: 82, 5: 173, 4: 75, 3: 32, 2: 67, 1: 217, 0: 146, },
20: {20: 1, 19: 152, 18: 185, 17: 240, 16: 5, 15: 111, 14: 99, 13: 6, 12: 220, 11: 112, 10: 150, 9: 69, 8: 36, 7: 187, 6: 22, 5: 228, 4: 198, 3: 121, 2: 121, 1: 165, 0: 174, },
22: {22: 1, 21: 89, 20: 179, 19: 131, 18: 176, 17: 182, 16: 244, 15: 19, 14: 189, 13: 69, 12: 40, 11: 28, 10: 137, 9: 29, 8: 123, 7: 67, 6: 253, 5: 86, 4: 218, 3: 230, 2: 26, 1: 145, 0: 245, },
24: {24: 1, 23: 122, 22: 118, 21: 169, 20: 70, 19: 178, 18: 237, 17: 216, 16: 102, 15: 115, 14: 150, 13: 229, 12: 73, 11: 130, 10: 72, 9: 61, 8: 43, 7: 206, 6: 1, 5: 237, 4: 247, 3: 127, 2: 217, 1: 144, 0: 117, },
26: {26: 1, 25: 246, 24: 51, 23: 183, 22: 4, 21: 136, 20: 98, 19: 199, 18: 152, 17: 77, 16: 56, 15: 206, 14: 24, 13: 145, 12: 40, 11: 209, 10: 117, 9: 233, 8: 42, 7: 135, 6: 68, 5: 70, 4: 144, 3: 146, 2: 77, 1: 43, 0: 94, },
28: {28: 1, 27: 252, 26: 9, 25: 28, 24: 13, 23: 18, 22: 251, 21: 208, 20: 150, 19: 103, 18: 174, 17: 100, 16: 41, 15: 167, 14: 12, 13: 247, 12: 56, 11: 117, 10: 119, 9: 233, 8: 127, 7: 181, 6: 100, 5: 121, 4: 147, 3: 176, 2: 74, 1: 58, 0: 197, },
30: {30: 1, 29: 212, 28: 246, 27: 77, 26: 73, 25: 195, 24: 192, 23: 75, 22: 98, 21: 5, 20: 70, 19: 103, 18: 177, 17: 22, 16: 217, 15: 138, 14: 51, 13: 181, 12: 246, 11: 72, 10: 25, 9: 18, 8: 46, 7: 228, 6: 74, 5: 216, 4: 195, 3: 11, 2: 106, 1: 130, 0: 150, },
}

# pre-generates all the possible different lengths of generator polynomials needed for QR codes
# these are now available as a lookup table, this is just the function that created the table originally
# multiply the starting poly as many times as the number of codewords required
def build_all_generators():
    all_codewords = [7, 10, 13, 15, 16, 17, 18, 20, 22, 24, 26, 28,
                     30]  # all valid generator lengths, in terms of number of EC codewords
    all_generators = {}
    for codewords in all_codewords:
        # starting point: multiply (x-a^0) and (x-a^1)
        # equivalent to (a^0x^1 - a^0) * (a^0x^1 - a^1x^0)
        # ignoring the signs, since +/- are equivalent in GF256
        # so (a0x1 + a0x0) (a0x1 + a1x0)
        # the result of this multiplication is a0x2 + a25x1 + a1x0

        # list of known correct generators from
        # https: // www.thonky.com / qr - code - tutorial / generator - polynomial - tool
        validator = {7: 'α0x7 + α87x6 + α229x5 + α146x4 + α149x3 + α238x2 + α102x + α21',
                     10: 'α0x10 + α251x9 + α67x8 + α46x7 + α61x6 + α118x5 + α70x4 + α64x3 + α94x2 + α32x + α45',
                     13: 'α0x13 + α74x12 + α152x11 + α176x10 + α100x9 + α86x8 + α100x7 + α106x6 + α104x5 + α130x4 + α218x3 + α206x2 + α140x + α78',
                     15: 'α0x15 + α8x14 + α183x13 + α61x12 + α91x11 + α202x10 + α37x9 + α51x8 + α58x7 + α58x6 + α237x5 + α140x4 + α124x3 + α5x2 + α99x + α105',
                     16: 'α0x16 + α120x15 + α104x14 + α107x13 + α109x12 + α102x11 + α161x10 + α76x9 + α3x8 + α91x7 + α191x6 + α147x5 + α169x4 + α182x3 + α194x2 + α225x + α120',
                     17: 'α0x17 + α43x16 + α139x15 + α206x14 + α78x13 + α43x12 + α239x11 + α123x10 + α206x9 + α214x8 + α147x7 + α24x6 + α99x5 + α150x4 + α39x3 + α243x2 + α163x + α136',
                     18: 'α0x18 + α215x17 + α234x16 + α158x15 + α94x14 + α184x13 + α97x12 + α118x11 + α170x10 + α79x9 + α187x8 + α152x7 + α148x6 + α252x5 + α179x4 + α5x3 + α98x2 + α96x + α153',
                     20: 'α0x20 + α17x19 + α60x18 + α79x17 + α50x16 + α61x15 + α163x14 + α26x13 + α187x12 + α202x11 + α180x10 + α221x9 + α225x8 + α83x7 + α239x6 + α156x5 + α164x4 + α212x3 + α212x2 + α188x + α190',
                     22: 'α0x22 + α210x21 + α171x20 + α247x19 + α242x18 + α93x17 + α230x16 + α14x15 + α109x14 + α221x13 + α53x12 + α200x11 + α74x10 + α8x9 + α172x8 + α98x7 + α80x6 + α219x5 + α134x4 + α160x3 + α105x2 + α165x + α231',
                     24: 'α0x24 + α229x23 + α121x22 + α135x21 + α48x20 + α211x19 + α117x18 + α251x17 + α126x16 + α159x15 + α180x14 + α169x13 + α152x12 + α192x11 + α226x10 + α228x9 + α218x8 + α111x7 + α0x6 + α117x5 + α232x4 + α87x3 + α96x2 + α227x + α21',
                     26: 'α0x26 + α173x25 + α125x24 + α158x23 + α2x22 + α103x21 + α182x20 + α118x19 + α17x18 + α145x17 + α201x16 + α111x15 + α28x14 + α165x13 + α53x12 + α161x11 + α21x10 + α245x9 + α142x8 + α13x7 + α102x6 + α48x5 + α227x4 + α153x3 + α145x2 + α218x + α70',
                     28: 'α0x28 + α168x27 + α223x26 + α200x25 + α104x24 + α224x23 + α234x22 + α108x21 + α180x20 + α110x19 + α190x18 + α195x17 + α147x16 + α205x15 + α27x14 + α232x13 + α201x12 + α21x11 + α43x10 + α245x9 + α87x8 + α42x7 + α195x6 + α212x5 + α119x4 + α242x3 + α37x2 + α9x + α123',
                     30: 'α0x30 + α41x29 + α173x28 + α145x27 + α152x26 + α216x25 + α31x24 + α179x23 + α182x22 + α50x21 + α48x20 + α110x19 + α86x18 + α239x17 + α96x16 + α222x15 + α125x14 + α42x13 + α173x12 + α226x11 + α193x10 + α224x9 + α130x8 + α156x7 + α37x6 + α251x5 + α216x4 + α238x3 + α40x2 + α192x + α180',
                     }

        print("Generator for", codewords, "codewords", end=' ')
        generator = Polynomial()
        generator = generator.add_alpha_term(0, 1)
        generator = generator.add_alpha_term(0, 0)
        for i in range(1, codewords):
            multiplier = Polynomial()
            multiplier = multiplier.add_alpha_term(0, 1)
            multiplier = multiplier.add_alpha_term(i, 0)
            generator = generator.multiply_poly(multiplier)
        if generator.alpha_form() == validator[codewords]:
            print("verified!")
            all_generators[codewords] = generator
        else:
            print("FAIL!")
            print("Should be:", validator[codewords])
            print("Actually :", generator.alpha_form())

    # print out the completed generator dictionary so we can hard code it for future reference
    print("Completed generator polynomial dictionary")
    print("generators = {")
    for codewords, generator in all_generators.items():
        print(str(codewords) + ': {', end='')
        for x, a in generator.terms.items():
            print(str(x) + ': ' + str(a), end=', ')
        print('},')
    print('}')


def check_valid_GF256(n):
    if n < 0 or n > 255:
        raise ValueError(str(n) + " is invalid - must be 0-255")


# bitwise XOR for adding and subtracting
def add_GF256(a, b):
    # print(a,"XOR", b, "=", a^b)  # DEBUG
    return a ^ b


# use logs for multiplications
def multiply_GF256(a, b):
    # 0 is a special case, since log[0] isn't allowed
    if a == 0 or b == 0:
        return 0
    else:
        return exp[(log[a] + log[b]) % 256]

# takes a list of codewords as bytes, and returns a list of error correction codewords (also bytes)
def ec_codewords(message, ec_codewords: int):
    # initialise the result polynomial using the message codewords as coefficients
    result = Polynomial()
    for i in range(len(message)):
        result = result.add_int_term(message[i], len(message)-i-1)  # the first codeword is the highest power of x

    # get the correct generator for the number of codewords
    generator = Polynomial(generators[ec_codewords])
    # multiply this by the highest term in the message
    #generator = generator.multiply_by_x_to_the(result.highest_power_of_x())

    # multiply the message poly by x^codewords to ensure there is room for all the EC codewords
    result = result.multiply_by_x_to_the(ec_codewords)

    #print("Multiplied message  :", result.int_form())
    #print("Multiplied generator:", generator.alpha_form())

    # for as many times as the number of codewords in the message
    # OR
    # while the highest term of the result exceeds the highest term of the multiplied generator???
    for step in range(len(message)):
        #print("Step", step+1)
        # multiply the original generator in such a way as to guarantee that the lead term in the message
        # will be cancelled during the XOR step
        # to do this, we must use the coefficient of the lead term in the current remainder
        # and a power of x, such that the remainder and the step_multiplier have the same power of x in the lead term
        step_multiplier = generator.clone()
        lead_coefficient = result.highest_coefficient()
        adjusting_power = result.highest_power_of_x() - generator.highest_power_of_x()
        adjuster = Polynomial({adjusting_power: lead_coefficient})
        step_multiplier = step_multiplier.multiply_poly(adjuster)
        #print("multiply generator by", result.highest_term().alpha_form())
        #print(step_multiplier.int_form())

        # add the multiplied generator to the current result polynomial
        #print("XOR the result with the message polynomial")
        result = result.add_poly(step_multiplier)
        #print(result.int_form())

    # the integer coefficients of the result polynomial are the EC codewords
    return [a for a in result.terms.values()]


class Polynomial:
    """ a sequence of terms of the form
    a^nx^m +...
    uses GF256 arthimetic for operations
    each term is stored in a dictionary
    with the key giving the power of x
    and the value the integer coefficient
    """

    # construct from a pre-existing dictionary of terms or just initialise as an empty polynomial
    def __init__(self, dictionary={}):
        # shallow copy the dict
        self.terms = dictionary.copy()

    # add a new term to this polynomial
    # or sum the term with whatever was already there
    # a is the actual GF256 integer coefficient
    # x is the power to which x is raised
    # so (1, 2) -> 1 x^2, which is x squared
    def add_int_term(self, a, x):
        check_valid_GF256(a)
        result = self.clone()
        if x in result.terms:
            # use XOR for Galois Field addition
            coefficient = add_GF256(result.terms[x], a)
            if coefficient == 0:  # cancel out
                del result.terms[x]
            else:
                result.terms[x] = coefficient
        else:
            result.terms[x] = a
        return result

    # add a new term to this polynomial
    # or sum the term with whatever was already there
    # a is the power to which alpha is raised
    # x is the power to which x is raised
    # so (0, 2) -> a^0 x^2, which is x squared
    def add_alpha_term(self, a, x):
        return self.add_int_term(exp[a], x)

    # return a copy of this polynomial
    def clone(self):
        return Polynomial(self.terms)

    # add a whole polynomial to this one
    def add_poly(self, p):
        result = self.clone()
        for x, a in p.terms.items():
            result = result.add_int_term(a, x)
        return result

    # multiply this polynomial by an integer coefficient
    def multiply_by_int(self, n):
        # each coefficient is multiplied using logarithm lookups
        result = Polynomial()
        for x, a in self.terms.items():
            new_a = (log[a] + log[n]) % 255  # TODO Should this be 256?
            result = result.add_alpha_term(new_a, x)
        return result

    # multiply this polynomial with another
    def multiply_poly(self, p2):
        result = Polynomial()
        for x1, a1 in self.terms.items():
            for x2, a2 in p2.terms.items():
                #                a = exp[(log[a1] + log[a2]) % 255]
                a = (log[a1] + log[a2]) % 255  # TODO Should this be 256?
                x = x1 + x2
                result = result.add_alpha_term(a, x)
        return result

    # shift all terms up by some power of x
    def multiply_by_x_to_the(self, power):
        # this is just a question of adding power to every key in the polynomial dictionary
        result = Polynomial({x + power: a for x, a in self.terms.items()})
        return result

    # return the highest power in the polynomial
    def highest_power_of_x(self) -> int:
        # this is just the largest key
        highest = 0
        for x in self.terms.keys():
            if x > highest:
                highest = x
        return highest

    # return the entire term with the highest power
    # it is returned as a polynomial with just 1 term
    def highest_term(self):
        highest = 0
        for x in self.terms.keys():
            if x > highest:
                highest = x
        return Polynomial({highest: self.terms[highest]})

    # return the integer coefficient of the term with the highest power
    def highest_coefficient(self):
        highest = 0
        for x in self.terms.keys():
            if x > highest:
                highest = x
        return self.terms[highest]

    def alpha_form(self) -> str:
        alpha_terms = []
        for x, a in self.terms.items():
            if x == 0:
                alpha_terms.append('α' + str(log[a]))
            elif x == 1:
                alpha_terms.append('α' + str(log[a]) + 'x')
            else:
                alpha_terms.append('α' + str(log[a]) + 'x' + str(x))
        return ' + '.join(alpha_terms)

    def int_form(self) -> str:
        int_terms = []
        for x, a in self.terms.items():
            coefficient = a
            t = ''
            if coefficient > 1 or x == 0:
                t = str(coefficient)
            if x > 0:
                t = t + 'x'
                if x > 1:
                    t = t + str(x)
            if t:
                int_terms.append(t)
        return ' + '.join(int_terms)


# TESTING
def test():
    # check using the HELLO WORLD example from https://www.thonky.com/qr-code-tutorial/error-correction-coding
    #test_message = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    #print("Test codewords:", ec_codewords(test_message, 10))  # 10 EC codewords required

    # input message codewords from the java app and try generating the correct codewords for them
    while True:
        message_string = input("\nEnter message codewords: ")
        message = [int(m) for m in message_string.split(",")]
        print("\nYour EC codewords:")
        print(", ".join([str(cw) for cw in ec_codewords(message, 28)]))  # 28 EC codewords required