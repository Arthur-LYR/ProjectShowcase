"""
Given a text file and pattern file containing the text string and pattern string respectively, this program computes
all occurrences of pattern in text using the Boyer Moore algorithm implemented with modified shift rule and writes it
to an output file.
"""

__author__ = "Arthur Lee"

import sys


def read_file(filename):
    """ 
    Function to read a file and return its contents
    
    :param filename: Name of file
    :return: Contents as a str
    """
    file = open(filename, "r")
    data = file.read()
    file.close()
    return data


def write_output(filename, matches):
    """ 
    Writes output to appropriately named output file
    
    :param filename: Name of output file
    :param matches: Result of computation
    """
    output_file = open(filename, "w")
    if len(matches) > 0:
        output_file.write(str(matches[0] + 1))
        for i in range(1, len(matches)):
            output_file.write("\n")
            output_file.write(str(matches[i] + 1))
    output_file.close()


def compare_chars(string, i, j):
    """ 
    Compares two suffixes of the same string and computes the length of the longest common prefix among them
    
    :param string: String to check
    :param i: Starting index of first suffix
    :param j: Starting index of second suffix
    :return: Length of common prefix (0 if no common prefix)
    """
    count = 0
    while i < len(string) and j < len(string):
        if string[i] == string[j]:
            count += 1
            i += 1
            j += 1
        else:
            break
    return count


def z_algo(string):
    """ 
    Implementation of Gusfield's Z-algorithm
    
    :param string: String to compute Z values
    :return: Z-array of corresponding Z values
    :time complexity: O(n) where n = len(string)
    :aux space complexity: O(n)
    """
    # Return empty array for empty string
    if len(string) == 0:
        return []

    # Initialise Variables
    z_array = [len(string)]
    left = 0
    right = 0

    # Loop thorough string
    for i in range(1, (len(string))):

        # Case 1
        if i > right:
            z_value = compare_chars(string, 0, i)
            z_array.append(z_value)
            if z_value > 0:
                right = z_value + i - 1
                left = i

        # Case 2
        else:
            z_ref = z_array[i - left]
            remain = right - i + 1

            # Case 2a
            if z_ref < remain:
                z_array.append(z_ref)

            # Case 2b
            elif z_ref > remain:
                z_array.append(remain)

            # Case 2c
            else:
                z_value = z_ref + compare_chars(string, z_ref, right + 1)
                z_array.append(z_value)
                right = z_value + i - 1
                left = i

    # Return Z values
    return z_array


def rev_compare_chars(string, i, j):
    """ 
    Compares two prefixes of the same string and computes the length of the longest common suffix among them
    
    :param string: String to check
    :param i: Starting index of first prefix
    :param j: Starting index of second prefix
    :return: Length of common suffix (0 if no common suffix)
    """
    count = 0
    while i >= 0 and j >= 0:
        if string[i] == string[j]:
            count += 1
            i -= 1
            j -= 1
        else:
            break
    return count


def rev_z_algo(string):
    """ 
    Implementation of Gusfield's Z-algorithm for suffixes
    
    :param string: String to compute Z values
    :return: Suffix Z-array of corresponding Z values
    :time complexity: O(n) where n = len(string)
    :aux space complexity: O(n)
    """
    # Return empty array for empty string
    if len(string) == 0:
        return []

    # Initialise Variables
    z_array = [None] * len(string)
    z_array[-1] = len(string)
    right = len(string) - 1
    left = len(string) - 1

    # Loop thorough string
    for i in range(len(string) - 2, -1, -1):

        # Case 1
        if i < left:
            z_value = rev_compare_chars(string, len(string) - 1, i)
            z_array[i] = z_value
            if z_value > 0:
                left = z_value + i - 1
                right = i

        # Case 2
        else:
            z_ref = z_array[len(string) - 1 - i - right]
            remain = i + 1 - left

            # Case 2a
            if z_ref < remain:
                z_array[i] = z_ref

            # Case 2b
            elif z_ref > remain:
                z_array[i] = remain

            # Case 2c
            else:
                z_value = z_ref + rev_compare_chars(string, z_ref, left - 1)
                z_array[i] = z_value
                left = z_value + i - 1
                right = i

    # Return Z values
    return z_array


def index(char):
    """ 
    Given set of alphabets is printable ASCII chars of Dec 32 to 127. This function shifts the ord such that
    it falls within 0 to 95
    
    :param char: ASCII char
    :return: Shifted index
    """
    return ord(char) - 32


def char(index):
    """ 
    Given an index specially shifted using index method, compute the corresponding ASCII char
    
    :param index: Shifted index
    :return: Corresponding ASCII char
    """
    return chr(index + 32)


def shift_preprocess(pat, rev_z_array):
    """ 
    Computes the shift_table for a given pat used to implement the special rule
    
    :param pat: Pattern string
    :param rev_z_array: Suffix Z Array of pat
    :return: shift_table for pat
    :time complexity: O(m) where m = len(pat)
    :space complexity: O(m)
    """
    # Initialise Important Variables
    alphabet_size = 96
    shift_table = [None] * alphabet_size

    # Fill in rows where char exists
    count = 0
    for character in pat:
        # Char exists in pat
        if shift_table[index(character)] is None:
            shift_table[index(character)] = [-1] * (len(pat) + 1)

            # Row computed in similar fashion to conventional gs_array
            for i in range(len(pat) - 1):
                j = len(pat) - rev_z_array[i]

                # Only update value if char at end of suffix is equal to the current char
                if pat[i - rev_z_array[i]] == character:
                    shift_table[index(character)][j] = i

            # A new character has been computed
            count += 1

        # When all characters in the alphabet have been computed, break from loop
        if count >= alphabet_size:
            break

    # Done
    return shift_table  # Technically an array of arrays but I'll call it a table for simplicity


def mp_preprocess(pat, z_array):
    """ 
    Computes the mp_array for a given pat
    
    :param pat: Pattern string
    :param z_array: Z Array for pat
    :return: mp_array for pat
    :time complexity: O(m) where m = len(pat)
    :space complexity: O(m)
    """
    # Initialise Important Variables
    mp_array = [0] * (len(pat) + 1)
    mp_array[-2] = z_array[-1]

    # Compute mp_array
    for i in range(len(mp_array) - 3, -1, -1):
        if z_array[i] + i == len(pat):
            mp_array[i] = z_array[i]
        else:
            mp_array[i] = mp_array[i + 1]

    # Done
    return mp_array


def modified_BoyerMoore(txt, pat):
    """ 
    Implementation of Boyer Moore Algorithm modified with the new shift rule.
    The new shift rule may be treated as a modification of the conventional Good Suffix Rule which replaces the
    conventional Bad Character and Good Suffix Rules.
    
    :param txt: Text String
    :param pat: Pattern String
    :return: Array containing start indices of pat occurrences in txt
    :time complexity: O(n + m) where n = len(txt) and m = len(pat); O(n/m) average case
    :space complexity: O(n + m)
    """
    # Check if pat is empty string
    if pat == "":
        return []

    # Initialise Important Variables
    matches = []
    shift = 0
    stop = -1
    resume = -1

    # Compute Z Arrays
    z_array = z_algo(pat)
    rev_z_array = rev_z_algo(pat)

    # Preprocess pat
    shift_table = shift_preprocess(pat, rev_z_array)
    mp_array = mp_preprocess(pat, z_array)

    # Keep shifting pat until it exceeds txt
    while len(pat) - 1 + shift <= len(txt) - 1:

        # Compare txt and pat
        k = len(pat) - 1
        while k >= 0:
            pat_char = pat[k]
            txt_char = txt[k + shift]

            # Match
            if pat_char == txt_char:
                # Galil's Optimisation
                if k == stop:
                    k = resume
                else:
                    k -= 1

            # Mismatch
            else:
                # Modified Shift Rule
                if shift_table[index(txt_char)] is not None and shift_table[index(txt_char)][k + 1] > -1:
                    # Try to find special case 
                    shift += len(pat) - 1 - shift_table[index(txt_char)][k + 1]
                    stop = shift_table[index(txt_char)][k + 1] + 1
                    resume = shift_table[index(txt_char)][k + 1] - len(pat) + k
                else:
                    # If cannot find, use MP
                    shift += len(pat) - mp_array[k + 1]
                    stop = mp_array[k + 1]
                    resume = -1

                break

        # Check if match present
        if k < 0:
            matches.append(shift)
            shift += len(pat) - mp_array[1]
            stop = -1
            resume = -1

    # Done
    return matches


if __name__ == "__main__":
    # Read Input Files
    text_file = sys.argv[1]
    pattern_file = sys.argv[2]
    text, pattern = read_file(text_file), read_file(pattern_file)

    # Actual Computation
    result = modified_BoyerMoore(text, pattern)

    # Write Output File
    write_output("output_modified_BoyerMoore.txt", result)
