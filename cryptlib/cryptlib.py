import math
import string

##########################
### Informative decorator
##########################

def challenge():
    pass



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
        in1 = int(in1, base=16)
    if isinstance(in2, str):
        in2 = int(in2, base=16)
    return in1 ^ in2

def test_xor():
    result = xor('1c0111001f010100061a024b53535009181c','686974207468652062756c6c277320657965')
    assert result == 0x746865206b696420646f6e277420706c6179L

# Set 1, Challenge 3
def xor_cipher(hexin):
    """ Returns: highest scoring output from single char xor
        on an arbitrary hex string. """
    # 1. xor hexin with each char in string.lowercase
    # 2. score the hex string output according to frequency
    candidates = []
    hexbytes = bytearray(hexin, 'hex')
    for char in string.printable:
        newbytes = bytearray()
        for byte in hexbytes:
            result = xor(byte, ord(char))
            newbytes.append(result)
        modifiedText = newbytes.decode()
        if all(char in string.printable for char in modifiedText):
            candidates.append((score_letter_frequency(modifiedText), modifiedText))

    print max(candidates)

def score_letter_frequency(inputString):
    """ Returns: letter frequency score of an arbitrary string. """

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

    # Score the results, algorithm gratuitously borrowed
    #  from https://github.com/tomdeakin/Matasano-Crypto-Challenges/blob/master/textutils.py
    totalscore = 0.0
    for letter in letter_frequencies:
        if letter not in letterCount:
            letterCount[letter] = 0.0
        totalscore += math.sqrt(letterCount[letter] * letter_frequencies[letter])
    return totalscore


def test_xor_cipher():
    result = xor_cipher("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    assert result == None

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
###  Constants
#####################

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