"""
Given a text file and pattern file containing the text string and pattern string respectively, this program computes
all occurrences of pattern in text where the hamming distance is <= 1 by applying the Z-algorithm and writes it to an
output file.
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
        output_file.write(" ".join([str(matches[0][0] + 1), str(matches[0][1])]))
        for i in range(1, len(matches)):
            output_file.write("\n")
            output_file.write(" ".join([str(matches[i][0] + 1), str(matches[i][1])]))
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


def hd1_patmatch(txt, pat):
    """ 
    Uses prefix and suffix Z algorithms to compute all matches of pat in txt where the ham distance is <= 1
    
    :param txt: Text String
    :param pat: Pattern String
    :return: List in form of [(key, value), ...] where key = index of occurrence and value = ham
    """
    # Check if pat is empty
    if pat == "":
        return []

    # Important Variables
    matches = []
    query = "".join([pat, txt])  # The .join() method in Python has a complexity of O(N) where N = length of final str
    rev_query = "".join([txt, pat])

    # Initialise Z Array
    z_array = [None] * (len(query) + 1)
    right = len(rev_query)
    left = len(rev_query)

    # Compute Suffix Z Array for rev_query
    for i in range(len(rev_query) - 1, len(pat) - 1, -1):

        # Case 1
        if i < left:
            z_value = rev_compare_chars(rev_query, len(rev_query) - 1, i - 1)
            z_array[i] = z_value
            if z_value > 0:
                left = z_value + i - 1
                right = i

        # Case 2
        else:
            z_ref = z_array[len(rev_query) - 1 - i - right]
            remain = i + 1 - left

            # Case 2a
            if z_ref < remain:
                z_array[i] = z_ref

            # Case 2b
            elif z_ref > remain:
                z_array[i] = remain

            # Case 2c
            else:
                z_value = z_ref + rev_compare_chars(rev_query, z_ref, left - 1)
                z_array[i] = z_value
                left = z_value + i - 1
                right = i

    # Reset Pointers
    left = 0
    right = 0

    # Compute Prefix Z Array for query
    for i in range(1, len(query) - len(pat) + 1):

        # Case 1
        if i > right:
            z_value = compare_chars(query, 0, i)
            final = z_value
            if z_value > 0:
                right = z_value + i - 1
                left = i

        # Case 2
        else:
            z_ref = z_array[i - left]
            remain = right - i + 1

            # Case 2a
            if z_ref < remain:
                final = z_ref

            # Case 2b
            elif z_ref > remain:
                final = remain

            # Case 2c
            else:
                z_value = z_ref + compare_chars(query, z_ref, right + 1)
                final = z_value
                right = z_value + i - 1
                left = i

        # Check if there is a match
        if i >= len(pat):
            if z_array[i] + final == len(pat) - 1:
                matches.append((i - len(pat), 1))
            elif z_array[i] + final >= 2 * len(pat):
                matches.append((i - len(pat), 0))

        # Override existing value
        z_array[i] = final

    # Done
    return matches


if __name__ == "__main__":
    # Read Input Files
    text_file = sys.argv[1]
    pattern_file = sys.argv[2]
    text, pattern = read_file(text_file), read_file(pattern_file)

    # Actual Computation
    result = hd1_patmatch(text, pattern)

    # Write Output File
    write_output("output_hd1_patmatch.txt", result)
