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
def build_generator_poly(codewords: int):
    # starting point: multiply (x-a^0) and (x-a^1)
    # equivalent to (a^0x^1 - a^0) * (a^0x^1 - a^1x^0)
    # ignoring the signs, since +/- are equivalent in GF256
    # so (a0x1 + a0x0) (a0x1 + a1x0)
    # the result of this multiplication is a0x2 + a25x1 + a1x0

    # DEBUG - checking manually for 2 and 3 codewords
    # p1 = Polynomial()
    # p1.add_alpha_term(0, 1)
    # p1.add_alpha_term(0, 0)
    # p2 = Polynomial()
    # p2.add_alpha_term(0, 1)
    # p2.add_alpha_term(1, 0)
    # result = p1.multiply_poly(p2)
    # print(result.alpha_form())
    # # 3 codewords: multiply by (x-a2)
    # p3 = Polynomial()
    # p3.add_alpha_term(0, 1)
    # p3.add_alpha_term(2, 0)
    # result = result.multiply_poly(p3)
    # print(result.alpha_form())
    # print()

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
    generator.add_alpha_term(0, 1)
    generator.add_alpha_term(0, 0)
    for i in range(1, codewords):
        multiplier = Polynomial()
        multiplier.add_alpha_term(0, 1)
        multiplier.add_alpha_term(i, 0)
        generator = generator.multiply_poly(multiplier)
    if generator.alpha_form() == validator[codewords]:
        print("MATCH!")
    else:
        print("FAIL!")
        print("Should be:", validator[codewords])
        print("Actually :", generator.alpha_form())

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


class Polynomial:
    """ a sequence of terms of the form
    a^nx^m +...
    uses GF256 arthimetic for operations
    each term is stored in a dictionary
    with the key giving the power of x
    and the value the integer coefficient
    """

    def __init__(self):
        self.terms = {}

    # add a new term to this polynomial
    # or sum the term with whatever was already there
    # a is the actual GF256 integer coefficient
    # x is the power to which x is raised
    # so (1, 2) -> 1 x^2, which is x squared
    def add_int_term(self, a, x):
        check_valid_GF256(a)
        if x in self.terms:
            # use XOR for Galois Field addition
            coefficient = add_GF256(self.terms[x], a)
            if coefficient == 0:  # cancel out
                del self.terms[x]
            else:
                self.terms[x] = coefficient
        else:
            self.terms[x] = a

    # add a new term to this polynomial
    # or sum the term with whatever was already there
    # a is the power to which alpha is raised
    # x is the power to which x is raised
    # so (0, 2) -> a^0 x^2, which is x squared
    def add_alpha_term(self, a, x):
        self.add_int_term(exp[a], x)

    # return a copy of this polynomial
    def clone(self):
        result = Polynomial()
        for x, a in p.terms.items():
            result.terms[x] = a
        return result

    # add a whole polynomial to this one
    def add_poly(self, p):
        result = self.clone()
        for x, a in p.terms.items():
            result.add_int_term(a, x)
        return result

    # multiply this polynomial with another
    def multiply_poly(self, p2):
        result = Polynomial()
        for x1, a1 in self.terms.items():
            for x2, a2 in p2.terms.items():
                #                a = exp[(log[a1] + log[a2]) % 255]
                a = (log[a1] + log[a2]) % 255  # TODO Should this be 256?
                x = x1 + x2
                result.add_alpha_term(a, x)
        return result

    def alpha_form(self) -> str:
        alpha_terms = []
        for x, a in self.terms.items():
            if x==0:
                alpha_terms.append('α' + str(log[a]))
            elif x==1:
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
        return '+'.join(int_terms)


# TESTING
def test():
    # create generators for all possible numbers of codewords
    codewords = [7, 10, 13, 15, 16, 17, 18, 20, 22, 24, 26, 28, 30]
    for c in codewords:
        build_generator_poly(c)
