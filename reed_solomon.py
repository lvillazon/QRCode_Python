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
exp = (1, 3, 5, 15, 17, 51, 85, 255, 26, 46, 114, 150, 161, 248, 19, 53, 95, 225, 56, 72, 216, 115, 149, 164, 247, 2, 6, 10, 30, 34, 102, 170,
    229, 52, 92, 228, 55, 89, 235, 38, 106, 190, 217, 112, 144, 171, 230, 49, 83, 245, 4, 12, 20, 60, 68, 204, 79, 209, 104, 184, 211, 110, 178, 205,
    76, 212, 103, 169, 224, 59, 77, 215, 98, 166, 241, 8, 24, 40, 120, 136, 131, 158, 185, 208, 107, 189, 220, 127, 129, 152, 179, 206, 73, 219, 118, 154,
    181, 196, 87, 249, 16, 48, 80, 240, 11, 29, 39, 105, 187, 214, 97, 163, 254, 25, 43, 125, 135, 146, 173, 236, 47, 113, 147, 174, 233, 32, 96, 160,
    251, 22, 58, 78, 210, 109, 183, 194, 93, 231, 50, 86, 250, 21, 63, 65, 195, 94, 226, 61, 71, 201, 64, 192, 91, 237, 44, 116, 156, 191, 218, 117,
    159, 186, 213, 100, 172, 239, 42, 126, 130, 157, 188, 223, 122, 142, 137, 128, 155, 182, 193, 88, 232, 35, 101, 175, 234, 37, 111, 177, 200, 67, 197, 84,
    252, 31, 33, 99, 165, 244, 7, 9, 27, 45, 119, 153, 176, 203, 70, 202, 69, 207, 74, 222, 121, 139, 134, 145, 168, 227, 62, 66, 198, 81, 243, 14,
    18, 54, 90, 238, 41, 123, 141, 140, 143, 138, 133, 148, 167, 242, 13, 23, 57, 75, 221, 124, 132, 151, 162, 253, 28, 36, 108, 180, 199, 82, 246, 1)
log = ('**log 0 is invalid**', 0, 25, 1, 50, 2, 26, 198, 75, 199, 27, 104, 51, 238, 223, 3, 100, 4, 224, 14, 52, 141, 129, 239, 76, 113, 8, 200, 248, 105, 28, 193,
    125, 194, 29, 181, 249, 185, 39, 106, 77, 228, 166, 114, 154, 201, 9, 120, 101, 47, 138, 5, 33, 15, 225, 36, 18, 240, 130, 69, 53, 147, 218, 142,
    150, 143, 219, 189, 54, 208, 206, 148, 19, 92, 210, 241, 64, 70, 131, 56, 102, 221, 253, 48, 191, 6, 139, 98, 179, 37, 226, 152, 34, 136, 145, 16,
    126, 110, 72, 195, 163, 182, 30, 66, 58, 107, 40, 84, 250, 133, 61, 186, 43, 121, 10, 21, 155, 159, 94, 202, 78, 212, 172, 229, 243, 115, 167, 87,
    175, 88, 168, 80, 244, 234, 214, 116, 79, 174, 233, 213, 231, 230, 173, 232, 44, 215, 117, 122, 235, 22, 11, 245, 89, 203, 95, 176, 156, 169, 81, 160,
    127, 12, 246, 111, 23, 196, 73, 236, 216, 67, 31, 45, 164, 118, 123, 183, 204, 187, 62, 90, 251, 96, 177, 134, 59, 82, 161, 108, 170, 85, 41, 157,
    151, 178, 135, 144, 97, 190, 220, 252, 188, 149, 207, 205, 55, 63, 91, 209, 83, 57, 132, 60, 65, 162, 109, 71, 20, 42, 158, 93, 86, 242, 211, 171,
    68, 17, 146, 217, 35, 32, 46, 137, 180, 124, 184, 38, 119, 153, 227, 165, 103, 74, 237, 222, 197, 49, 254, 24, 13, 99, 140, 128, 192, 247, 112, 7)


#def ec_codewords(message: list[int], codewords: int) -> list[int]:
#    pass

# multiply the starting poly as many times as the number of codewords required
# the result is stored as a tuple of the powers (an int bit field)
# and a tuple of coefficients
#def build_generator_poly(codewords: int) -> tuple[int, tuple[int]]:
    # starting point: multiply (x-a^0) and (x-a^1)
    # equivalent to (a^0x^1 - a^0) * (a^0x^1 - a^1x^0)
    # represented as (3,(1, 1)) * (3, (1, 3))
    # the 3 is 11 in binary, so the first two terms of x (x^1 & x^0) are present
    # the other tuple gives the integer coefficients of each term 1=a^0, 3=a^1
    # the result of this multiplication is a^0x^2 + a^0x^1 + a^1x^0
    # represented as (7, (1, 1, 3))
    # note the number of elements in the 2nd tuple, must equal the number of
    # set bits in the initial integer (7 is 111, so 3 set bits, so 3 coefficients)

#    pass

# multiply 2 polynomials expressed as a list of coefficients, with SMALLEST powers of x 1st
def poly_multiply(poly1, poly2):
    # create an empty polynomial large enough to hold the result
    result = [0] * (len(poly1) + len(poly2)-1)
    # multiply every term by every other, combining terms with the same power
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            power = i+j
            term1 = str(poly1[i])+'x^'+str(i)
            term2 = str(poly2[j])+'x^'+str(j)
            product = gf256_multiply(poly1[i],poly2[j])
            product_str = str(gf256_multiply(poly1[i],poly2[j])) + 'x^' + str(i+j)
            print(term1, '*', term2, '=', product_str)
            result[i+j] = gf256_add(result[i+j], product)
    return result

def poly_print(poly) -> str:
    result = str(poly[0]) + 'x^0'
    for i in range(1, len(poly)):
        term = str(poly[i]) + 'x^' + str(i)
        result += ' + ' + term
    return result

def poly_print_alpha(poly) -> str:
    result = 'a'+str(log[poly[0]]) + 'x0'
    for i in range(1, len(poly)):
        term = 'a' + str(log[poly[i]]) + 'x' + str(i)
        result += ' + ' + term
    return result

def gf256_multiply(a: int, b: int) -> int:
    if a==0 or b==0:  # multiplying by 0 is a special case since log(0) is undefined
        return 0
    return exp[(log[a] + log[b])%256]

def gf256_add(a: int, b: int) -> int:
    return a ^ b

def test():
#    p1 = [1,2,3]
#    p2 = [3, 4]
    p1 = [1, 1]
    p2 = [2, 1]
    print("Multiplying", poly_print(p1), "and", poly_print(p2))
    result = poly_multiply(p1, p2)
    print("=", poly_print(result))
    print("=", poly_print_alpha(result))