"""
Decodes a binary file into the original file using the LZ77 algorithm, Elias Omega Code, and Huffman Code
"""

__author__ = "Arthur Lee"

import sys


def read_input(filename):
    """
    Reads the contents of the compressed binary file

    :param filename: Name of file
    :return: File contents
    """
    file = open(filename, "rb")
    contents = file.read()
    file.close()
    return contents


def write_output(filename, contents):
    """
    Writes the uncompressed file data to the file

    :param filename: Name of original file
    :param contents: Original file data
    """
    file = open(filename, "w", encoding="utf-8")
    file.write(contents)
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


def elias_decode(container, encoded, current, start=0):
    """
    Decodes the most significant Elias encoded integer in encoded

    :param container: Current byte in iteration
    :param encoded: Encoded data
    :param current: Current byte index
    :param start: Start point of Elias Code (Default to 0)
    :return: Decoded Value as int
    """
    # Current Length
    k = 1

    # Loop until MSB == 1
    while container[0] != 1:
        container[0] = 1

        # Get Length
        d = 0       # Current Length
        p = k - 1   # Power
        while p > -1:
            d += container[0] << p
            p -= 1
            container.contract(1)
            container, encoded, current = update_container(container, encoded, current)

        k = d + 1

    # Get Number
    n = 0      # Current Length
    p = k - 1  # Power
    while p > -1:
        n += container[0] << p
        p -= 1
        container.contract(1)
        container, encoded, current = update_container(container, encoded, current)

    # Done
    return container, encoded, current, n + start - 1


class Node:
    """
    Simple Node Class for a node in CharTree
    """
    def __init__(self, char=None):
        """
        Constructor. Has link to the left child and right child. Stores char if leaf, else None.

        :param char: Char to store
        """
        self.left = None
        self.right = None
        self.char = char


class CharTree:
    """
    A BST used in Huffman Decoding
    """
    def __init__(self, code):
        """
        Constructor. Initialises the tree from the given encoding.
        """
        self.root = Node()
        for char, encoding in code:
            self.insert(char, encoding)

    def insert(self, char, code):
        """
        Insert an entry a Huffman Code into the tree

        :param char: Char to store
        :param code: Huffman code as bitarray
        """
        # Start from root and loop through code
        current = self.root
        for i in range(len(code)):

            # Go left if 0
            if code[i] == 0:

                # Add Node if it does not exist
                if current.left is None:
                    current.left = Node(char=char if i == len(code) - 1 else None)

                # Go left
                current = current.left

            # Go right if 1
            else:

                # Add Node if it does not exist
                if current.right is None:
                    current.right = Node(char=char if i == len(code) - 1 else None)

                # Go right
                current = current.right


def huffman_decode(container, encoded, current, tree):
    """
    Decodes the most significant huffman encoded char in encoded

    :param container: Current byte in iteration
    :param encoded: Encoded data
    :param current: Current byte index
    :param tree: Binary Tree of Huffman Key
    :return: Original Char
    """
    # Loop through tree
    current_node = tree.root
    while current_node.char is None:

        # Go left if 0 found
        if container[0] == 0:
            current_node = current_node.left

        # Go right if 1 found
        else:
            current_node = current_node.right

        # Update container and encoded
        container.contract(1)
        container, encoded, current = update_container(container, encoded, current)

    # Done
    return container, encoded, current, current_node.char


def lz77_decode(data, offset, length, char):
    """
    LZ77 Decoder that updates the data given an LZ77 triple

    :param data: Current data
    :param offset: Offset
    :param length: Length
    :param char: Next Char
    :return: Updated data
    """
    # Important Values
    current = len(data)
    count = 0

    # Loop append offset chars
    i = current - offset
    while count < length:
        data.append(data[i])
        count += 1
        i += 1
        if i >= current:
            i = current - offset

    # Append next char
    data.append(char)

    # Done
    return data


def update_container(container, encoded, current):
    """
    Update the container with the next byte when it reaches 0

    :param container: Current byte in iteration
    :param encoded: Encoded data
    :param current: Current byte index
    :return: Updated container, encoded, and current
    """
    if len(container) == 0:
        if current < len(encoded) - 1:
            current += 1
            container = BitArray(encoded[current], 8)
    return container, encoded, current


def main(encoded):
    """
    Main Method. Decodes a binary file using the LZ77 decoding algorithm, Elias Omega Code, and Huffman Code

    :param encoded: Encoded file data
    :return: Original File Name and File Data
    """
    # Important Variables
    current = 0
    container = BitArray(encoded[current], 8)

    # Get File Name Length (We always update container after decoding)
    container, encoded, current, name_length = elias_decode(container, encoded, current)

    # Uncompress File Name
    name = []
    for _ in range(name_length):
        # Get current char
        char_index = 0
        p = 7
        while p > -1:
            char_index += container[0] << p
            p -= 1
            container.contract(1)
            container, encoded, current = update_container(container, encoded, current)
        name.append(chr(char_index))
    # Join chars
    name = "".join(name)

    # Get File Data Length and Number of Distinct Chars
    container, encoded, current, data_length = elias_decode(container, encoded, current)
    container, encoded, current, distinct_chars = elias_decode(container, encoded, current)

    # Get Huffman Encoding Key
    huffman_key = []
    for _ in range(distinct_chars):
        # Get char
        char_index = 0
        p = 7
        while p > -1:
            char_index += container[0] << p
            p -= 1
            container.contract(1)
            container, encoded, current = update_container(container, encoded, current)

        # Get length of code
        container, encoded, current, code_length = elias_decode(container, encoded, current)

        # Get code
        code = BitArray(0, 0)
        for _ in range(code_length):
            code.append(BitArray(container[0], 1))
            container.contract(1)
            container, encoded, current = update_container(container, encoded, current)

        # Add data to key
        huffman_key.append((chr(char_index), code))

    # Compute the Binary Tree
    huffman_tree = CharTree(huffman_key)
    data = []

    # Uncompress File Data using LZ77
    i = 0
    while i < data_length:
        container, encoded, current, offset = elias_decode(container, encoded, current)
        container, encoded, current, length = elias_decode(container, encoded, current)
        container, encoded, current, char = huffman_decode(container, encoded, current, huffman_tree)
        data = lz77_decode(data, offset, length, char)
        i += length + 1

    # Done
    return name, "".join(data)


if __name__ == "__main__":
    # Read Inputs
    compressed_name = sys.argv[1]
    encoded_data = read_input(compressed_name)

    # Uncompress and Write
    file_name, file_data = main(encoded_data)
    write_output(file_name, file_data)
