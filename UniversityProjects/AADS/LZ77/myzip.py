"""
Encodes a text file into a binary file using the LZ77 algorithm, storing integers using the Elias Omega code
and storing characters using Huffman Encoding.
"""

__author__ = "Arthur Lee"

import sys
import heapq


def read_input(filename):
    """
    Reads the contents of a file

    :param filename: Name of file
    :return: File contents
    """
    file = open(filename, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    return contents


def write_output(filename, compressed):
    """
    Writes the compressed bytearray into a binary file

    :param filename: Name of original file
    :param compressed: Compressed data as bytearray
    """
    file = open("".join([filename, ".bin"]), "wb")
    file.write(compressed)
    file.close()


class BitArray:
    """
    Wrapper Class to deal with binary operations
    """
    def __init__(self, bits, length=None):
        """
        We store bits as an integer but mark the area we are interested in with a length.

        :param bits: Bits stored as integer
        :param length: Length of bit array (from LSB)
        """
        self.length = length if length is not None else self.bit_length(bits)
        self.bits = bits & ((1 << self.length) - 1)

    @staticmethod
    def bit_length(n):
        """
        Compute the bit length of an int.

        :param n: Integer
        :return: Number of bits in minimal binary code of n
        """
        d = 0
        while n > 0:
            d += 1
            n >>= 1
        return d

    def __len__(self):
        """
        Get the length of the BitArray

        :return: Length of BitArray
        """
        return self.length

    def __int__(self):
        """
        Convert the BitArray to int by returning the bits

        :return: BitArray as int
        """
        return self.bits

    def __str__(self):
        """
        Get the BitArray as a binary string for display purposes

        :return: Bit string of BitArray
        """
        string = ""
        for i in range(len(self)):
            string += str(self[i])
        return string

    def ascii(self):
        """
        Get the ASCII representation of the BitArray if possible

        :return:
        """
        if self.length == 8:  # If the length is 8, we can obtain the ASCII char represented by the int
            return chr(int(self))
        else:
            raise ValueError("Bit length must be 8")

    def __getitem__(self, item):
        """
        Get a bit at a certain index by shifting and masking

        :param item: Index
        :return: Bit at index
        """
        return (self.bits >> (self.length - item - 1)) & 1

    def __setitem__(self, key, value):
        """
        Set a bit at a certain index by shifting and masking

        :param key: Index
        :param value: Bit to set
        """
        if value:   # Bit = 1
            value <<= (self.length - key - 1)
            self.bits |= value
        else:   # Bit = 0
            value = True
            value <<= (self.length - key - 1)
            self.bits &= ~value

    def get_slice(self, start, end):
        """
        Get a slice of the bit from start to end (inclusive) using shifting and masking

        :param start: Start of slice
        :param end: End of slice
        :return: Slice as a BitArray
        """
        new_bits = self.bits >> (self.length - end - 1)
        new_bits &= (1 << (end - start + 1)) - 1
        new_length = end - start + 1
        return BitArray(new_bits, new_length)

    def prepend(self, other):
        """
        Prepend another BitArray to the front

        :param other: Another BitArray
        """
        other.bits <<= self.length
        self.bits |= other.bits
        self.length += other.length

    def append(self, other):
        """
        Append another BitArray to the back

        :param other: Another BitArray
        """
        self.bits <<= other.length
        self.bits |= other.bits
        self.length += other.length

    def extend(self, n):
        """
        Pads n 0s to the back of BitArray

        :param n: Length of extension
        """
        self.bits <<= n
        self.length += n

    def contract(self, n):
        """
        Shortens the BitArray without changing anything

        :param n: Length of contraction
        """
        self.length -= n
        self.bits &= ((1 << self.length) - 1)

    def to_bytes(self):
        """
        Converts 1st 8 bits in BitArray to bytearray representation

        :return: BitArray as bytearray
        """
        byte_array = int(self.get_slice(0, 7))
        self.contract(8)
        return byte_array


def elias_encode(n, start=0):
    """
    Encodes an integer using the Elias Omega Code

    :param n: Integer >= start
    :param start: Start point of Elias Code (Default to 0)
    :return: Elias Omega Code of n as bitarray
    """
    # Shift n according to start point and initialise code
    n -= start - 1
    current = BitArray(n)
    code = BitArray(n)

    # Compute L_i - 1 until 1 reached
    while n > 1:
        n = len(current) - 1
        current = BitArray(n)
        current[0] = 0
        code.prepend(current)

    # Done
    return code


class CharInfo:
    """
    Wrapper class to allow for proper heap extract min when computing huffman code
    """
    def __init__(self, char, freq):
        """
        Constructor. Store the chars and their frequency.

        :param char: Chars concatenated in a single string
        :param freq: Number of occurrences in text
        """
        self.char = char
        self.freq = freq

    def __str__(self):
        """
        Display the object in a readable manner.

        :return: String representation
        """
        return "(\"" + self.char + "\", " + str(self.freq) + ")"

    def __lt__(self, other):
        """
        Override less than operator such that if frequencies are equal, smaller length is the tie breaker.

        :param other: Other object
        :return: True if self < other, False otherwise
        """
        if self.freq != other.freq:
            return self.freq < other.freq
        else:
            return len(self.char) < len(other.char)


def huffman_encode(text):
    """
    Generates a Huffman Code from a given text and encodes the text using the computed Huffman Code.

    :param text: String to encode
    :return: The encoded text and its encoding
    """
    # Important Variables
    code = [0] * 256
    chars = []

    # Compute Frequencies of every char in text
    for char in text:
        if code[ord(char)] == 0:
            chars.append(char)
        code[ord(char)] += 1

    # Collect chars who have occurred at least once
    for i in range(len(chars)):
        chars[i] = CharInfo(chars[i], code[ord(chars[i])])

    # Override code array with empty bitarrays
    for i in range(len(code)):
        code[i] = BitArray(0, 0)

    # If only one char in text, represent as single 0 bit
    if len(chars) == 1:
        code[ord(chars[0].char)] = BitArray(0, 1)

    # Heapify chars and keep computing until all chars fuse into a single CharInfo object
    heapq.heapify(chars)
    while len(chars) > 1:

        # Get least occurring chars (break tie by smallest length)
        cset1 = heapq.heappop(chars)
        for c in cset1.char:
            code[ord(c)].prepend(BitArray(0, 1))  # Prepend 0 to all chars in set

        # Get second least occurring chars (break tie by smallest length)
        cset2 = heapq.heappop(chars)
        for c in cset2.char:
            code[ord(c)].prepend(BitArray(1, 1))  # Prepend 1 to all chars in set

        # Combine both sets and push back to heap
        cset = CharInfo("".join([cset1.char, cset2.char]), cset1.freq + cset2.freq)
        heapq.heappush(chars, cset)

    # Done
    return code


def huffman_data(code):
    """
    Extracts the chars that exist in file data from huffman code

    :param code: Huffman code
    :return: Unique data
    """
    unique_code = []
    for i in range(len(code)):
        if len(code[i]) != 0:
            unique_code.append((i, code[i]))
    return unique_code


def string_index(start, current, end, i):
    """
    Converts regular i = 0, 1, 2, ... index to the appropriate index in string

    :param start: Left buffer of sliding window
    :param current: Current Index
    :param end: Right buffer of sliding window
    :param i: Index
    :return: Converted Index
    """
    lookahead = end - current + 1
    if i < lookahead:
        return i + current
    else:
        return i - lookahead + start


def compare_chars(string, start, current, end, i, j):
    """
    Compares two suffixes of the same string and computes the length of the longest common prefix among them

    :param string: String to check
    :param start: Left buffer of sliding window
    :param current: Current Index
    :param end: Right buffer of sliding window
    :param i: Starting index of first suffix
    :param j: Starting index of second suffix
    :return: Length of common prefix (0 if no common prefix)
    """
    # String Variables
    lookahead = end - current + 1
    slide_window = end - start + 1
    string_length = lookahead + slide_window

    # Compare
    count = 0
    while i < string_length and j < string_length:
        si = string_index(start, current, end, i)
        sj = string_index(start, current, end, j)
        if string[si] == string[sj]:
            count += 1
            i += 1
            j += 1
        else:
            break

    # Done
    return count


def z_algo(string, start, current, end):
    """
    Specialised Implementation of Gusfield's Z-algorithm for use in LZ77 encoding

    :param string: String to compute Z values
    :param start: Left buffer of sliding window
    :param current: Current Index
    :param end: Right buffer of sliding window
    :return: Z-array of corresponding Z values
    """
    # String Variables
    lookahead = end - current + 1
    slide_window = end - start + 1
    string_length = lookahead + slide_window

    # Z Algo Variables
    z = [0] * string_length
    left = 0
    right = 0

    # Output Variables
    index, length = 0, 0

    # Loop thorough string
    i = 1
    sp = string_index(start, current, end, i)
    while i < slide_window:

        # Case 1
        if i > right:
            z_value = compare_chars(string, start, current, end, 0, i)
            z[i] = z_value
            if z_value > 0:
                right = z_value + i - 1
                left = i

        # Case 2
        else:
            z_ref = z[i - left]
            remain = right - i + 1

            # Case 2a
            if z_ref < remain:
                z[i] = z_ref

            # Case 2b
            elif z_ref > remain:
                z[i] = remain

            # Case 2c
            else:
                z_value = z_ref + compare_chars(string, start, current, end, z_ref, right + 1)
                z[i] = z_value
                right = z_value + i - 1
                left = i

        # Update Output if better one found and if is within range
        if start <= sp <= current - 1 and length <= z[i]:
            index, length = string_index(start, current, end, i), z[i]

        # Update Pointers
        i += 1
        sp = string_index(start, current, end, i)

    # Make sure length is within sliding window
    length = min(lookahead, length)
    if current + length >= len(string):
        length -= 1

    # Done
    return current - index, length, string[current + length]


def lz77_encode(text, window, lookahead, huffman_key, container, encoded):
    """
    LZ77 Encoder

    :param text: String to encode
    :param window: Window size
    :param lookahead: Lookahead Buffer Size
    :param huffman_key: Huffman encoding generated from char frequencies
    :param container: BitArray container
    :param encoded: Encoded file data
    :return: Updated container and encoded with LZ77 encoded data
    """
    # Important Variables
    current = 0

    # Loop through text
    while current < len(text):
        # Get Appropriate Indices
        start = max(0, current - window)
        end = min(len(text) - 1, current + lookahead - 1)

        # Get triples values
        offset, length, char = z_algo(text, start, current, end)
        if length == 0:
            offset = 0

        # Update Current and Append
        current += length + 1

        # Compress Offset
        container.append(elias_encode(offset))
        container, encoded = update_container(container, encoded)

        # Compress Length
        container.append(elias_encode(length))
        container, encoded = update_container(container, encoded)

        # Compress Char
        container.append(huffman_key[ord(char)])
        container, encoded = update_container(container, encoded)

    # Done
    return container, encoded


def update_container(container, encoded):
    """
    Move bits from BitArray container to bytearray encoded until container is length < 8

    :param container: BitArray storage
    :param encoded: Bytearray encoding
    :return: Update container and encoded
    """
    while len(container) >= 8:
        encoded.append(container.to_bytes())
    return container, encoded


def main(name, data, window, lookahead):
    """
    Encodes a file using the LZ77 encoding algorithm with Elias Omega Encoding and Huffman Encoding
    for storing Integers and Characters.

    :param name: File Name
    :param data: File Contents
    :param window: Window (or Dictionary) Size
    :param lookahead: Lookahead Buffer Size
    :return: Compressed Data as bytearray
    """
    # Important Variables
    container = BitArray(0, 0)
    encoded = bytearray()

    # Compress Length of File Name
    container.append(elias_encode(len(name)))
    container, encoded = update_container(container, encoded)  # Always ensure container is of length 8 bits

    # Compress File Name Chars
    for char in name:
        container.append(BitArray(ord(char), 8))
        container, encoded = update_container(container, encoded)

    # Compress File Length
    container.append(elias_encode(len(data)))
    container, encoded = update_container(container, encoded)

    # Obtain Huffman Encoding
    huffman_key = huffman_encode(data)
    huffman_info = huffman_data(huffman_key)

    # Compress Number of Unique Chars
    container.append(elias_encode(len(huffman_info)))
    container, encoded = update_container(container, encoded)

    # Compress Huffman Encoding Data
    for char_index, encoding in huffman_info:
        # Char
        container.append(BitArray(char_index, 8))
        container, encoded = update_container(container, encoded)

        # Length of Encoding
        container.append(elias_encode(len(encoding)))
        container, encoded = update_container(container, encoded)

        # Actual Encoding
        container.append(encoding)
        container, encoded = update_container(container, encoded)

    # Compress File Data Using LZ77
    container, encoded = lz77_encode(data, window, lookahead, huffman_key, container, encoded)

    # Add remaining bits to encoded
    if len(container) != 0:
        container.extend(8 - (len(container) % 8))
        encoded.append(container.to_bytes())

    # Done
    return encoded


if __name__ == "__main__":
    # Read Inputs
    file_name, W, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    file_data = read_input(file_name)

    # Compress and Write
    encoded_data = main(file_name, file_data, W, L)
    write_output(file_name, encoded_data)
