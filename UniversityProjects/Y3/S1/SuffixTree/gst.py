"""
Uses a Generalised Suffix Tree constructed with Ukkonen's Algorithm to perform case insensitive pattern matching
given a query txt file of texts and patterns.
"""

__author__ = "Arthur Lee"

import sys


class Node:
    """
    Node in Suffix Tree. Compressed representation: Store as [string_id, start, end] where string_id is index of string
    in strings array; start and end are indices in string.
    """
    def __init__(self, string_id=None, start=None, end=None, suffix_link=None, is_root=False, is_leaf=False):
        """
        Constructor

        :param string_id: Index of string in strings array
        :param start: Start Index
        :param end: End Index
        :param suffix_link: Link to next Suffix for Ukkonen
        :param is_root: True if root, False otherwise
        :param is_leaf: True if leaf, False otherwise
        """
        self.link = [None] * 128  # First 128 ASCII Chars
        self.string_id = string_id
        self.start = start
        self.end = end
        self.suffix_link = suffix_link
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.suffix_id = []  # We store Suffix IDs as array of (text_id, suffix_id) tuples


class GeneralisedSuffixTree:
    """
    Implementation of a Generalised Suffix Tree (GST) with a catch: the Suffix IDs of blank string suffixes (i.e. sole
    "$" strings are not stored in node.suffix_id)
    """
    def __init__(self, strings):
        """
        Constructor. Uses Ukkonen's Algorithm to store multiple strings (terminated with $) into a GST.

        :param strings: List of strings terminated with $
        """
        self.root = Node(is_root=True)
        for i in range(len(strings)):
            self.ukkonen(strings, i)

    @staticmethod
    def index(char):
        """
        Converts ASCII char to appropriate index in this special Suffix Tree

        :param char: ASCII character
        :return: Appropriate Index
        """
        # Shift chars before $ by 1
        if 0 <= ord(char) <= 35:
            return ord(char) + 1

        # Set $ to 0
        elif ord(char) == 36:
            return 0

        # Every other char is unchanged
        else:
            return ord(char)

    def ukkonen(self, strings, string_id):
        """
        Ukkonen's Algorithm modified to account for inserting into a GST

        :param strings: List of strings terminated with $
        :param string_id: Index of string in strings
        """
        # Counters
        i = 0
        j = 0

        # Active Point and Previous Node (for Suffix Link)
        previous_node = None
        active_node = self.root
        active_edge = 0     # Represented as an index for a char in string
        active_length = 0   # From Active Node

        # Phases
        while i < len(strings[string_id]):

            """
            We do not need a Global End as we immediately set node.end = len(string) - 1 if the node is a leaf. 
            Therefore, Rule 1 and Once a Leaf Always a Leaf has already been taken care of.
            """

            # Extensions
            while j < i + 1:
                # Traverse, Make Extension, Update Previous Node, Active Edge, and check if Showstopper
                previous_node, active_node, active_edge, active_length, show_stopper = \
                    self.traverse(previous_node, active_node, active_edge, active_length, strings, string_id, j, i)

                # Rule 3 Executed
                if show_stopper:
                    break   # Showstopper: Move to next phase, maintain current extension

                # Rule 2 Executed
                else:
                    j += 1  # Not Showstopper: Move to next extension

            # Move to next phase
            i += 1

    def traverse(self, previous_node, active_node, active_edge, active_length, strings, string_id, start, end):
        """
        Traversal Method for Ukkonen's algorithm. Traverses to active point and applies appropriate extension.

        :param previous_node: Previous Internal Node created (if any)
        :param active_node: Active Node
        :param active_edge: Active Edge
        :param active_length: Active Length
        :param strings: List of strings terminated with $
        :param string_id: Index of string in strings
        :param start: Current Extension (j-index)
        :param end: Current Phase (i-index)
        :return: Recently created internal node (if any), AN, AE, AL, Bool representing if Rule 3 executed
        """
        # Check if active node is root
        if active_node.is_root:
            # Rule 2a: Node completely traversed but no branch present, add branch and end
            if active_node.link[self.index(strings[string_id][start])] is None:

                # Create Leaf node
                active_node.link[self.index(strings[string_id][start])] = \
                    Node(string_id=string_id, start=start, end=len(strings[string_id]) - 1, is_leaf=True)

                # Only store Suffix ID if leaf is not blank string
                if self.index(strings[string_id][start]) != 0:
                    active_node.link[self.index(strings[string_id][start])].suffix_id.append((string_id, start))

                # No Internal Node Created, AN/AE maintained, AL is still 0, Not Showstopper
                return None, active_node, active_edge, 0, False

            # Branch Exists, set Active Edge to branch
            else:
                active_edge = start
        else:
            # Rule 2a: Node completely traversed but no branch present, add branch and end
            if active_node.link[self.index(strings[string_id][active_edge])] is None:

                # Create Leaf Node
                active_node.link[self.index(strings[string_id][active_edge])] = \
                    Node(string_id=string_id, start=active_edge, end=len(strings[string_id]) - 1, is_leaf=True)

                # Store Suffix ID
                active_node.link[self.index(strings[string_id][active_edge])].suffix_id.append((string_id, start))

                if active_node.suffix_link.is_root:
                    # No Internal Node Created, Traverse SL for AN, AE maintained, AL is i-j-1, Not Showstopper
                    return None, active_node.suffix_link, active_edge, end - start - 1, False
                else:
                    # No Internal Node Created, Traverse SL for AN, AE maintained, AL is 0, Not Showstopper
                    return None, active_node.suffix_link, active_edge, 0, False

        # Important Variables
        child = active_node.link[self.index(strings[string_id][active_edge])]
        string_index = end
        node_index = child.start + active_length
        node_length = child.end - child.start + 1

        # Skip-Count Traverse: If active length longer than node length, traverse to next node
        if active_length >= node_length:
            # Previous Node, Start, End maintained; Increase AE by Node Length; Current Node Length is shaved from AL
            return self.traverse(previous_node, child, active_edge + node_length, active_length - node_length,
                                 strings, string_id, start, end)

        # Rule 2b: Node not completely traversed and no branch present, branch out and end
        if strings[string_id][string_index] != strings[child.string_id][node_index]:

            # Replace child of current with first half of child
            active_node.link[self.index(strings[string_id][active_edge])] = \
                Node(string_id=child.string_id, start=child.start, end=node_index-1)

            # Update child start to new value and set new child as parent of old child
            child.start = node_index
            active_node.link[self.index(strings[string_id][active_edge])].link[
                self.index(strings[child.string_id][node_index])] = child

            # Create new node
            active_node.link[self.index(strings[string_id][active_edge])].link[
                self.index(strings[string_id][string_index])] = \
                Node(string_id=string_id, start=string_index, end=len(strings[string_id]) - 1, is_leaf=True)

            # Store Suffix ID
            active_node.link[self.index(strings[string_id][active_edge])].link[
                self.index(strings[string_id][string_index])].suffix_id.append((string_id, start))

            # Reset Child and Update Suffix Links
            child = active_node.link[self.index(strings[string_id][active_edge])]
            if previous_node is not None:
                previous_node.suffix_link = child
            child.suffix_link = self.root

            if active_node.is_root:
                # Internal Node Created, AN/AE maintained, AL is i-j-1, Not Showstopper
                return child, active_node, active_edge, end - start - 1, False
            else:
                if active_node.suffix_link.is_root:
                    # Internal Node Created, Traverse SL for AN, AE maintained, AL is i-j-1, Not Showstopper
                    return child, active_node.suffix_link, active_edge, end - start - 1, False
                else:
                    # Internal Node Created, Traverse SL for AN, AE/AL maintained, Not Showstopper
                    return child, active_node.suffix_link, active_edge, active_length, False

        # String completely traversed not ending at leaf
        else:
            # Special Rule: String completely traversed, next node is leaf
            if child.is_leaf and active_length == node_length - 1:

                # Store Suffix ID only if leaf is not blank string
                if self.index(strings[string_id][active_edge]) != 0 or not active_node.is_root:
                    child.suffix_id.append((string_id, start))

                if active_node.is_root:
                    # Internal Node Created, AN/AE maintained, AL is i-j-1, Not Showstopper
                    return child, active_node, active_edge, end - start - 1, False
                else:
                    if active_node.suffix_link.is_root:
                        # Internal Node Created, Traverse SL for AN, AE maintained, AL is i-j-1, Not Showstopper
                        return child, active_node.suffix_link, active_edge, end - start - 1, False
                    else:
                        # Internal Node Created, Traverse SL for AN, AE/AL maintained, Not Showstopper
                        return child, active_node.suffix_link, active_edge, active_length, False

            # Rule 3: String completely traversed not ending at leaf, next node is not leaf
            # No Internal Node Created, AN/AE maintained, Increment AL, Is Showstopper
            return None, active_node, active_edge, active_length + 1, True

    def pattern_match(self, texts, patterns):
        """
        Case Insensitive Pattern matching algorithm

        :param texts: List of strings in GST sorted in same order as insertion and terminated with $
        :param patterns: List of patterns to check for matches
        :return: List of (j, i, k) tuples where j = Index of pattern in patterns, i = Index of text in texts, k = Index
        where patterns[j] occurs in texts[i]
        """
        # Output
        matches = []

        # Loop through patterns
        for i in range(len(patterns)):

            # If pattern is empty, no matches
            if patterns[i] != "":

                # Traverse Pattern
                nodes = self.traverse_pattern(texts, patterns[i])

                # Inorder traverse from each node to get matches
                for node in nodes:
                    current_matches = self.suffix_array_aux(node, acc=[])

                    # Suffix IDs are in separate container arrays. We need to extract them.
                    for array in current_matches:
                        for text_id, index in array:
                            matches.append((i, text_id, index))

        # Done
        return matches

    def traverse_pattern(self, texts, pattern):
        """
        Traverse the pattern and check if it exists in GST.

        :param texts: List of strings in GST sorted in same order as insertion and terminated with $
        :param pattern: A Pattern to check for matches
        :return: End node of pattern, None if pattern does not exist
        """
        # Go two ways
        if pattern[0].isalpha():
            acc = self.traverse_pattern_aux(self.root, texts, pattern, 0, True, [])
            return self.traverse_pattern_aux(self.root, texts, pattern, 0, False, acc)

        # Go one way
        else:
            return self.traverse_pattern_aux(self.root, texts, pattern, 0, True, [])

    def traverse_pattern_aux(self, current, texts, pattern, start, upper, acc):
        """
        Auxiliary method for traverse_pattern

        :param current: Current node
        :param texts: List of strings in GST sorted in same order as insertion and terminated with $
        :param pattern: A Pattern to check for matches
        :param start: Starting index of pattern
        :param upper: True - Traverse uppercase link, False - Traverse lowercase link
        :param acc: Accumulator to store nodes
        :return: End node of pattern, None if pattern does not exist
        """
        # Check if child exists
        if pattern[start].isalpha():
            # Set child to uppercase link or lowercase link
            if upper:
                child = current.link[self.index(pattern[start].upper())]
            else:
                child = current.link[self.index(pattern[start].lower())]

        # Set to default if does not exist or performing case sensitive comparison
        else:
            child = current.link[self.index(pattern[start])]

        # No Link, go back up
        if child is None:
            return acc

        # Important Variables
        pattern_index = start
        text_id = child.string_id
        text_index = child.start

        # Compare chars in text node and pattern
        while pattern_index <= len(pattern) - 1 and text_index <= child.end:

            # Mismatched chars, no matches
            if pattern[pattern_index].upper() != texts[text_id][text_index].upper():
                return acc

            # Increment Counters
            pattern_index += 1
            text_index += 1

        # Pattern exists, return root node for traversal
        if pattern_index > len(pattern) - 1:
            acc.append(child)
            return acc

        # Node completely traversed, pattern has not. Jump to next node.
        elif text_index > child.end:
            # Go two ways
            if pattern[pattern_index].isalpha():
                acc = self.traverse_pattern_aux(child, texts, pattern, pattern_index, upper, acc)
                return self.traverse_pattern_aux(child, texts, pattern, pattern_index, not upper, acc)

            # Go one way
            else:
                return self.traverse_pattern_aux(child, texts, pattern, pattern_index, upper, acc)

    def suffix_array(self):
        """
        Computes the suffix array of the strings stored in GST.

        :return: Suffix array of strings in form of (i, j) where i is string_id and j is suffix_id of strings[i]
        """
        # Important Variables
        suffix_array = []
        arrays = self.suffix_array_aux(self.root, acc=[])

        # Suffix IDs are in separate container arrays. We need to extract them.
        for array in arrays:
            for suffix_id in array:
                suffix_array.append(suffix_id)

        # Done
        return suffix_array

    def suffix_array_aux(self, current, acc):
        """
        Auxiliary method for suffix_array.

        :param current: Current Node
        :param acc: Accumulator to store suffix ids
        :return: Suffix array of strings
        """
        # Base Case: Append Suffix ID and return
        if current.is_leaf:
            acc.append(current.suffix_id)
            return acc

        # Inductive Case: Traverse Links until Base Case reached
        else:
            for link in current.link:
                if link is not None:
                    acc = self.suffix_array_aux(link, acc)
            return acc

    def display(self, strings):
        """
        Display the Generalised Suffix Tree in console. For debugging purposes.

        :param strings: Strings stored in suffix tree
        """
        self.display_aux(strings, self.root, level=0)

    def display_aux(self, strings, current, level):
        """
        Auxiliary method for display.

        :param strings: Strings stored in generalised suffix tree
        :param current: Current Node
        :param level: Depth of Node (i.e. height from root)
        """
        # Base Case: Leaf reached, print out Suffix ID
        if current.is_leaf:
            # Indent based on level
            for _ in range(level):
                print(">", end="")

            # Print Node details
            print("\'" + strings[current.string_id][current.start:current.end+1] + "\':" + "[" +
                  str(current.string_id) + "," + str(current.start) + "," + str(current.end) + "] (" +
                  str(current.suffix_id) + ")")

        # Inductive Case: do not print out Suffix ID
        else:
            # Print Root
            if current == self.root:
                print("[ROOT]")

            # Loop through links
            for i in range(len(current.link)):

                # Print if Node exists
                if current.link[i] is not None:

                    # All information is in child node
                    child = current.link[i]

                    # Print if not leaf (leaf is for base case)
                    if not child.is_leaf:

                        # Indent based on level
                        for _ in range(level + 1):
                            print(">", end="")

                        # Print Node details
                        if child.suffix_link != self.root:
                            print("\'" + strings[child.string_id][child.start:child.end+1] + "\':[" +
                                  str(child.string_id) + "," + str(child.start) + "," + str(child.end) + "] ----> " +
                                  strings[child.string_id][child.suffix_link.start:child.suffix_link.end+1] +
                                  ":[" + str(child.suffix_link.string_id) + "," + str(child.suffix_link.start) + "," +
                                  str(child.suffix_link.end) + "]")
                        else:
                            print("\'" + strings[child.string_id][child.start:child.end+1] + "\':[" +
                                  str(child.string_id) + "," + str(child.start) + "," + str(child.end) +
                                  "] ----> [ROOT]")

                    # Traverse the Tree
                    self.display_aux(strings, child, level + 1)


def read_input(filename):
    """
    Function to read input and return its contents in the appropriate format

    :param filename: Name of file
    :return: Appropriate input for computation
    """
    # Important Variables
    counts = []
    strings = []
    txt_inputs = []
    pat_inputs = []

    # Open File
    file = open(filename, "r")

    # Read Lines
    lines = file.readlines()
    for line in lines:
        row = line.split()

        # This is a count of how many txt/pat files
        if len(row) == 1:
            counts.append(int(row[0]))

        # This is a file name
        else:
            str_file = open(row[1], "r")
            string = str_file.read()
            str_file.close()
            strings.append(string)

    # Collect txt inputs
    for i in range(counts[0]):
        txt_inputs.append(strings[i])

    # Collect pat inputs
    for i in range(counts[0], len(strings)):
        pat_inputs.append(strings[i])

    # Done
    file.close()
    return txt_inputs, pat_inputs


def write_output(filename, matches):
    """
    Writes output to appropriately named output file

    :param filename: Name of output file
    :param matches: Result of computation
    """
    # Open Output
    output_file = open(filename, "w")

    # Write if matches present
    if len(matches) > 0:
        output_file.write(" ".join([str(matches[0][0] + 1), str(matches[0][1] + 1), str(matches[0][2] + 1)]))
        for i in range(1, len(matches)):
            output_file.write("\n")
            output_file.write(" ".join([str(matches[i][0] + 1), str(matches[i][1] + 1), str(matches[i][2] + 1)]))

    # Done
    output_file.close()


def main(texts, patterns):
    """
    Main Method. Uses a GST to perform multiple text/pattern pattern matching.

    :param texts: List of texts
    :param patterns: List of patterns
    :return: List of (j, i, k) tuples where j = Index of pattern in patterns, i = Index of text in texts, k = Index
    where patterns[j] occurs in texts[i]
    """
    # Add terminal $ to end of all texts
    for i in range(len(texts)):
        texts[i] = "".join([texts[i], "$"])

    # Perform Pattern Matching and return
    return GeneralisedSuffixTree(texts).pattern_match(texts, patterns)


if __name__ == "__main__":
    # Read Input File
    query_file = sys.argv[1]
    text_inputs, pattern_inputs = read_input(query_file)

    # Actual Computation
    result = main(text_inputs, pattern_inputs)

    # Write Output File
    write_output("output_gst.txt", result)
