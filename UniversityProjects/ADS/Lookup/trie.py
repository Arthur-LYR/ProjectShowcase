""" 
This module contains a trie class with a special query function.
"""

__author__ = "Arthur Lee"


class Node:
    """
    Used in Trie. Node class representing a node in a Trie.
    """

    def __init__(self, value=0):
        """ Initialises Node with default Value of 0
        :param value: The number of strings in the Trie with the same prefix as the string represented by the node.
                      Terminal nodes will always have a value of 0.
        :time complexity: O(1)
        """
        self.link = [None] * 27     # We only need 26 lower case alphabets plus 1 terminal
        self.value = value


class Trie:
    """
    Implementation of Trie Data Structure.
    """

    def __init__(self):
        """ Initialises a Trie with a root node
        :time complexity: O(1)
        """
        self.root = Node()

    def insert(self, string):
        """ Inserts a string into the Trie
        :param string: String to be inserted
        :time complexity: O(M) where M is the number of characters in string
        """
        # Begin from Root
        current = self.root
        current.value += 1

        # Go through String
        for i in range(len(string)):
            # Calculate Index and Increment Value
            index = ord(string[i]) - 97 + 1

            # If path does not exist, create new node
            if current.link[index] is None:
                current.link[index] = Node()

            # Update Current
            current = current.link[index]
            current.value += 1

        # Repeat for Terminal and Set Value to 0
        terminal = 0
        if current.link[terminal] is None:
            current.link[terminal] = Node()

    def lex_greater(self, query):
        """ Computes the number of strings in the Trie that are lexicographically greater than query
        :param query: String to compute above
        :return: Number of strings in the Trie that are lexicographically greater than query
        :time complexity: O(M) where M is the number of characters in query
        """
        # Initialise Variables
        current = self.root
        count = 0

        # Go through Query
        for char in query:
            # Calculate Index
            index = ord(char) - 97 + 1

            # Check Links
            for i in range(index + 1, len(current.link)):
                if current.link[i] is not None:
                    count += current.link[i].value

            # Update Current
            current = current.link[index]

        # If query is a full string present in Trie, repeat for Terminal
        terminal = 0
        if current.link[terminal] is not None:
            # Check Links
            for i in range(terminal + 1, len(current.link)):
                if current.link[i] is not None:
                    count += current.link[i].value

            # Update Current
            current = current.link[terminal]

        # Update Count
        count += current.value

        # Return
        return count


def lex_pos(text: list, queries: list) -> list:
    """ For each query in queries, computes the number of strings in text that are lexicographically greater
        than query.
    :param text: List of strings
    :param queries: List of query strings where each query is a prefix of at least 1 string in text
    :return: List of results for each query in queries computed as described above
    :time complexity: O(T + Q) where T = sum of the number of characters in all strings in text and Q = total number of
                      characters in queries
    """
    # Initialise Trie and Output
    trie = Trie()
    result = []

    # Insert strings in text into Trie
    for string in text:
        trie.insert(string)

    # Obtain Individual Results for Each Query
    for query in queries:
        result.append(trie.lex_greater(query))

    # Return
    return result


if __name__ == "__main__":
    # Driver
    text = ["aaa", "bab", "aba", "baa", "baa", "aab", "bab"]
    queries = ["", "a", "b", "aab"]
    print(lex_pos(text, queries))
