import math
import os
import string

##########################
### Helper class for hex ops
##########################

class hexint(int):
    """ Python doesn't have support for a class that easily outputs
        information about ints as well as hex strings without the leading
        0x prefix, which means a lot of extra conversions must be done.
        This class is meant to simplify these operations; performance
        must be awful. """
    # ints are immutable, so we're using __new__
    def __new__(cls, *args, **kwargs):
        # if 'base' is not specified, cast our chr to an int
        if not kwargs and isinstance(args[0], str):
            args = (ord(args[0]),)
        return super(hexint, cls).__new__(cls, *args, **kwargs)
    @property
    def hstr(self):
        """ Returns: hex string, without the leading '0x'. """
        return format(self.real, '02x')

######################
### Crypto functions 
######################

# Set 1, Challenge 1
def hex_to_base64(hexval):
    """ Returns: base64 encoded value for a given
        hex value. """
    return hexval.decode('hex').encode('base64')

def test_hex_to_base64():
    results = hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
    assert results == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n"

# Set 1, Challenge 2
def xor(in1, in2):
    """ Returns: numeric hex XOR of input hex strings: in1 and in2. """
    if isinstance(in1, str):
        in1 = hexint(in1)
    if isinstance(in2, str):
        in2 = hexint(in2)
    return in1 ^ in2

def test_xor():
    result = xor(int('1c0111001f010100061a024b53535009181c', base=16), int('686974207468652062756c6c277320657965', base=16))
    assert result == 0x746865206b696420646f6e277420706c6179L

# Set 1, Challenge 3
def xor_cipher(hexin):
    """ Returns: highest scoring output from single char xor
        on an arbitrary hex string. """
    # 1. xor hexin with each char in string.lowercase
    # 2. score the hex string output according to frequency
    candidates = []
    for char in string.printable:
        results = ''
        for text in hexin.decode("hex"):
            result = xor(ord(text), ord(char))
            results += chr(result) 
        if all(char in string.printable for char in results):
            candidates.append((score_letter_frequency(results), results))
    if candidates:
        return max(candidates)[-1]

def score_letter_frequency(inputString):
    """ Returns: letter frequency score of an arbitrary string. """
    # From wikipedia
    letter_frequencies = {
        'a': 8.167,
        'b': 1.492,
        'c': 2.782,
        'd': 4.253,
        'e': 12.702,
        'f': 2.228,
        'g': 2.015,
        'h': 6.094,
        'i': 6.966,
        'j': 0.153,
        'k': 0.772,
        'l': 4.025,
        'm': 2.406,
        'n': 6.749,
        'o': 7.507,
        'p': 1.929,
        'q': 0.095,
        'r': 5.987,
        's': 6.327,
        't': 9.056,
        'u': 2.758,
        'v': 0.978,
        'w': 2.360,
        'x': 0.150,
        'y': 1.974,
        'z': 0.074,
    }

    inputString = inputString.lower()
    letterCount = {}
    count = 0
    letters = set(string.lowercase)

    # Add up letter counts
    for char in inputString:
        if char in letters:
            count += 1
        if char in letterCount:
            letterCount[char] += 1.
        else:
            letterCount[char] = 1.

    # Determine the total letter distribution
    for letter in letterCount:
        letterCount[letter] /= count

    # Score the results, Bhattacharyya coefficient algorithm gratuitously borrowed
    #  from https://github.com/tomdeakin/Matasano-Crypto-Challenges/blob/master/textutils.py
    totalscore = 0.0
    for letter in letter_frequencies:
        if letter not in letterCount:
            letterCount[letter] = 0.0
        totalscore += math.sqrt(letterCount[letter] * letter_frequencies[letter])
    return totalscore

def test_xor_cipher():
    result = xor_cipher("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    assert result == "Cooking MC's like a pound of bacon"

# Set 1, Challenge 4
def find_xord_string(strings):
    scores = {}
    for item in strings:
        max_item = xor_cipher(item)
        # string may not be readable, so dodge None returns
        if max_item:
            scores[score_letter_frequency(max_item)] = max_item
    return max(scores.items())

def test_find_xord_string():
    stringFile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'rsc', 'set4.txt')
    with open(stringFile, 'r') as infile:
        strings = [item.strip() for item in infile.readlines()]
    score, resultString = find_xord_string(strings)
    assert resultString == 'Now that the party is jumping\n'

# Set 1, Challenge 5
def repeating_xor(repeatingKey, value):
    newvalues = []
    keyRange = len(repeatingKey)
    for i, char in enumerate(value):
        key = repeatingKey[i % keyRange]
        newvalues.append(hexint(hexint(char) ^ hexint(key)).hstr)
    return ''.join(newvalues)

def test_repeating_xor():
    testvalue = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    testkey = "ICE"
    targetResult = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
    targetResult += "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    result = repeating_xor(testkey, testvalue)
    assert result == targetResult

# Set 1, Challenge 6
def bit_count(i):
    return bin(i).count("1")

def test_bit_count():
    assert bit_count(1) == 1
    assert bit_count(2) == 1
    assert bit_count(3) == 2
    assert bit_count(63) == 6

def hamming_distance(str1, str2):
    distance = 0
    for i, k in zip(str1, str2):
        distance += bit_count(ord(i) ^ ord(k))
    return distance

def test_hamming_distance():
    test_val = hamming_distance("this is a test", "wokka wokka!!!")
    assert test_val == 37

#######################
### Ad-hoc test runner
#######################

def runtests():
    import inspect
    thismodule = __import__(inspect.getmodulename(__file__))
    for name in dir(thismodule):
        obj = getattr(thismodule, name)
        if inspect.isfunction(obj) and name.startswith('test_'):
            obj()
            print name, "tests passed!"

if __name__ == "__main__":
    runtests()


#####################
###  References
#####################
# - http://en.wikipedia.org/wiki/XOR_cipher
