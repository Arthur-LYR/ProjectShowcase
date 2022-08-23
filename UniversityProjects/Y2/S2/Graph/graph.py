""" 
This module contains an implementation of a binomial min heap and a special graph.
"""

__author__ = "Arthur Lee"

from math import inf


class MinHeap:
    """
    Class that implements a MinHeap modified for use in Dijkstra Algorithm.
    """

    def __init__(self, max_capacity) -> None:
        """ Constructor. Initialises MinHeap with max_capacity items
        :param max_capacity: Maximum capacity of heap
        :time complexity: O(N) where N = max_capacity
        """
        self.length = 0
        self.array = [None] * (max_capacity + 1)

    def __len__(self):
        """ Returns number of items in MinHeap
        :return: Number of items in MinHeap
        :time complexity: O(1)
        """
        return self.length

    def is_full(self):
        """ Checks if heap is full
        :return: True if heap is full, False otherwise
        :time complexity: O(1)
        """
        return self.length + 1 == len(self.array)

    def rise(self, k):
        """ Rise Operation. Raises an item up the heap until parent is less than or equal to item
        :param k: Index of item to rise
        :time complexity: O(log N) where N = Number of items in heap
        """
        while k > 1 and self.array[k][1] < self.array[k // 2][1]:
            self.array[k], self.array[k//2] = self.array[k//2], self.array[k]
            self.array[k][0].index = k//2
            self.array[k//2][0].index = k
            k //= 2

    def sink(self, k):
        """ Sink Operation. Sinks an item down the heap until children are greater than or equal to item
        :param k: Index of item to sink
        :time complexity: O(log N) where N = Number of items in heap
        """
        while 2 * k <= self.length:
            child = self.smallest_child(k)
            if self.array[k][1] <= self.array[child][1]:
                break
            self.array[child], self.array[k] = self.array[k], self.array[child]
            self.array[child][0].index = k
            self.array[k][0].index = child
            k = child

    def smallest_child(self, k):
        """ Given a parent node, find the smallest child
        :param k: Index of parent node
        :return: Index of smallest child
        :time complexity: O(1)
        """
        if 2 * k == self.length or self.array[2 * k][1] < self.array[2 * k + 1][1]:
            return 2 * k
        else:
            return 2 * k + 1

    def append(self, vertex, distance):
        """ Add a vertex and distance (priority) to the heap
        :param vertex: Vertex Object
        :param distance: Distance while computing Dijkstra
        :return: True if not empty, False otherwise
        :time complexity: O(log N) where N = Number of items in heap
        """
        has_space_left = not self.is_full()

        if has_space_left:
            self.length += 1
            self.array[self.length] = (vertex, distance)
            self.rise(self.length)
            vertex.index = self.length

        return has_space_left

    def serve(self):
        """ Remove and return the Vertex at the top of the heap
        :return: Vertex with minimum distance
        :time complexity: O(log N) where N = Number of items in heap
        """
        if self.length == 0:
            raise IndexError("Heap is empty")

        min_elt = self.array[1]
        self.length -= 1
        if self.length > 0:
            self.array[1] = self.array[self.length + 1]
            self.sink(1)

        return min_elt[0]

    def update_distance(self, vertex, distance):
        """ Updates the distance of a vertex within the heap
        :param vertex: Vertex Object
        :param distance: New Distance
        :time complexity: O(log N) where N = Number of items in heap
        """
        self.array[vertex.index] = (vertex, distance)
        self.rise(vertex.index)
        self.sink(vertex.index)


class Edge:
    """
    Class that represents a Weighted Directed Edge between two Vertices in the WordGraph.
    """

    def __init__(self, u, v, ham, alphabets):
        """ Constructor.
        :param u: Source Vertex
        :param v: Destination Vertex
        :param ham: Hamming Distance of u and v
        :param alphabets: Alphabetical Distance of u and v
        :time complexity: O(1)
        """
        self.u = u
        self.v = v
        self.ham = ham
        self.alphabets = alphabets

    def __str__(self):
        """ For visualization purposes
        :return: String form of Edge
        :time complexity: O(1)
        """
        return "(" + str(self.v.word) + "[" + str(self.v.id) + "], AD[" + str(self.alphabets) + "])"


class WordVertex:
    """
    Class that represents a WordVertex in the WordGraph.
    """

    def __init__(self, id, word):
        """ Constructor.
        :param id: Name of WordVertex. Must be unique.
        :param word: Raw word to be stored in Vertex
        :time complexity: O(1)
        """
        # Basic Info
        self.id = id
        self.word = word
        self.edges = []

        # For Traversal
        self.discovered = False
        self.visited = False
        self.source_distance = inf
        self.destination_distance = inf
        self.total_distance = inf
        self.source_previous = None
        self.destination_previous = None
        self.index = None

    def create_edge(self, v, ham, alphabets):
        """ Create an Edge with self as Source WordVertex
        :param v: Destination WordVertex
        :param ham: Hamming Distance
        :param alphabets: Alphabetical Distance
        :time complexity: O(1)
        """
        self.edges.append(Edge(self, v, ham, alphabets))

    def reset(self, from_source):
        """ Set Traversal Attributes to Default
        :param from_source: True if reset for source_dijkstra, False if reset for destination_dijkstra
        :time complexity: O(1)
        """
        self.discovered = False
        self.visited = False
        self.destination_distance = inf
        self.total_distance = inf
        self.destination_previous = None
        self.index = None
        if from_source:
            self.source_distance = inf
            self.source_previous = None

    def __str__(self):
        """ For visualization purposes
        :return: String form of WordVertex
        :time complexity: O(D) where D = Number of Edges Vertex has
        """
        edges = []
        for edge in self.edges:
            edges.append(str(edge))
        return str(self.word) + "[" + str(self.id) + "] -> [" + ", ".join(edges) + "]"


class WordGraph:
    """
    Class that implements the Graph ADT.
    """

    def __init__(self, words):
        """ Constructor. Initialise WordGraph with words provided and sets edges between words with hamming distances
            of 1 with the appropriate hams and alphabets.
        :param words: List of words for use in word ladder
        :time complexity: O(MW^2) where M = Length of words in words and W = Number of words in words
        """
        # Add Vertices
        self.words = []
        for id in range(len(words)):
            self.words.append(WordVertex(id, words[id]))

        # Add Edges
        for i in range(len(words)):
            for j in range(i, len(words)):
                hamming_distance = self.hamming_distance(words[i], words[j])
                if hamming_distance == 1:
                    alphabet_distance = self.alphabet_distance(words[i], words[j])
                    self.set_edge(i, j, hamming_distance, alphabet_distance)

    def hamming_distance(self, word1, word2):
        """ Computes the hamming distance of two words of the same length
        :param word1: First Word
        :param word2: Second Word
        :return: Hamming Distance (Number of letters that are different)
        :time complexity: O(M) where M = Number of characters in each word
        """
        hamming_distance = 0
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                hamming_distance += 1
        return hamming_distance

    def alphabet_distance(self, word1, word2):
        """ Computes the alphabetical distance between two words with hamming distance of 1
        :param word1: First Word
        :param word2: Second Word
        :return: Alphabetical Distance (Absolute difference of ASCII value of characters that are different)
        :time complexity: O(M) where M = Number of characters in each word
        """
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                alphabet_distance = abs(ord(word1[i]) - ord(word2[i]))
                break
        return alphabet_distance

    def reset(self, from_source):
        """ Reset all WordVertices
        :param from_source: True if reset for source_dijkstra, False if reset for destination_dijkstra
        :time complexity: O(W) where W = Number of Words in Graph
        """
        for word in self.words:
            word.reset(from_source)

    def get_word_vertex(self, id):
        """ Get a WordVertex given its ID
        :param id: Name of WordVertex to find
        :return: WordVertex with corresponding ID
        :time complexity: O(1)
        """
        return self.words[id]

    def set_edge(self, u, v, ham, alphabets, directed=False):
        """ Set an Edge between two WordVertices in Graph
        :param u: Source WordVertex ID
        :param v: Destination WordVertex ID
        :param ham: Hamming Distance
        :param alphabets: Alphabetical Distance
        :param directed: True if edge is directed, False otherwise
        :time complexity: O(1)
        """
        u = self.get_word_vertex(u)
        v = self.get_word_vertex(v)
        u.create_edge(v, ham, alphabets)
        if not directed:
            v.create_edge(u, ham, alphabets)

    def source_dijkstra(self, source):
        """ Modified version of Dijkstra Algorithm for finding minimum alphabetical distances to all words from source
        :param source: Source WordVertex ID
        :time complexity: O(D log W + W log W) where W = Number of Words in Graph and D = Number of Edges in Graph
        """
        # Reset Vertices and Initialise Heap
        self.reset(from_source=True)
        source = self.get_word_vertex(source)
        source.source_distance = 0
        discovered = MinHeap(len(self.words))
        discovered.append(source, source.source_distance)

        # Perform Dijkstra
        while len(discovered) > 0:
            # Serve from Queue
            u = discovered.serve()
            u.discovered = True
            u.visited = True

            # Check Edges
            for edge in u.edges:
                v = edge.v

                # Update Distance of newly discovered vertices
                if not v.discovered:
                    v.discovered = True
                    v.source_distance = u.source_distance + edge.alphabets
                    v.source_previous = u
                    discovered.append(v, v.source_distance)

                # Perform Edge Relaxation
                elif not v.visited:
                    if v.source_distance > u.source_distance + edge.alphabets:
                        v.source_distance = u.source_distance + edge.alphabets
                        v.source_previous = u
                        discovered.update_distance(v, v.source_distance)

    def destination_dijkstra(self, destination):
        """ Modified version of Dijkstra Algorithm for finding minimum alphabetical distances to all words from
            destination
        :param destination: Destination WordVertex ID
        :time complexity: O(D log W + W log W) where W = Number of Words in Graph and D = Number of Edges in Graph
        """
        # Reset Vertices and Initialise Heap
        self.reset(from_source=False)
        source = self.get_word_vertex(destination)
        source.destination_distance = 0
        source.total_distance = source.source_distance + source.destination_distance
        discovered = MinHeap(len(self.words))
        discovered.append(source, source.destination_distance)

        # Perform Dijkstra
        while len(discovered) > 0:
            # Serve from Queue
            u = discovered.serve()
            u.discovered = True
            u.visited = True

            # Check Edges
            for edge in u.edges:
                v = edge.v

                # Update Distance of newly discovered vertices
                if not v.discovered:
                    v.discovered = True
                    v.destination_distance = u.destination_distance + edge.alphabets
                    v.total_distance = v.source_distance + v.destination_distance
                    v.destination_previous = u
                    discovered.append(v, v.destination_distance)

                # Perform Edge Relaxation
                elif not v.visited:
                    if v.destination_distance > u.destination_distance + edge.alphabets:
                        v.destination_distance = u.destination_distance + edge.alphabets
                        v.total_distance = v.source_distance + v.destination_distance
                        v.destination_previous = u
                        discovered.update_distance(v, v.destination_distance)

    def floyd_warshall(self):
        """ Implements Floyd-Warshall Algorithm for finding minimum hamming distances for all-word pairs
        :return: Matrix where matrix[i][j] is minimum hamming distance from Word i to Word j
        :time complexity: O(W^3) where W = Number of Words in Graph
        """
        # Initialise Adjacency Matrix
        matrix = [[]] * len(self.words)
        for i in range(len(matrix)):
            matrix[i] = [inf] * len(self.words)

        # Set Self Edges to 0
        for k in range(len(matrix)):
            matrix[k][k] = 0

        # Transfer existing edges
        for vertex in self.words:
            for edge in vertex.edges:
                source = edge.u.id
                destination = edge.v.id
                weight = edge.ham
                matrix[source][destination] = weight

        # Implement Algorithm
        for k in range(len(self.words)):
            for i in range(len(self.words)):
                for j in range(len(self.words)):
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

        # Return Distances
        return matrix

    def best_start_word(self, target_words):
        """ Computes the best start word to all target words such that the maximum of all optimal distances
            from source to destination is minimised.
        :param target_words: List of Destination Word IDs
        :return: The ID of the best start word
        :time complexity: O(W^3) where W = Number of Words in Graph
        """
        # Initialise Variables
        best_source = -1
        max_distances = []
        mapping = self.floyd_warshall()

        # If no target words, no best start word
        if len(target_words) == 0:
            return best_source

        # Compute the maximum optimal from all sources
        for row in mapping:
            max_distance = row[target_words[0]]
            for i in range(1, len(target_words)):
                if row[target_words[i]] > max_distance:
                    max_distance = row[target_words[i]]
            max_distances.append(max_distance)

        # Find the source with the minimum maximum optimal
        min_distance = inf
        for i in range(len(max_distances)):
            if max_distances[i] < min_distance:
                min_distance = max_distances[i]
                best_source = i

        # Best source is finalised
        return best_source

    def constrained_ladder(self, start, target, constraint_words):
        """ Computes a word ladder that includes at least one of the constraint words while minimising alphabetical
            distance
        :param start: Word ID of source
        :param target: Word Id of destination
        :param constraint_words: List of Word IDs of possible detours
        :return: The ideal path that satisfies the description above
        :time complexity: O(D log W + W log W) where W = Number of Words in Graph and D = Number of Edges in Graph
        """
        # Perform Dijkstra from start and target to constraint_words
        self.source_dijkstra(start)
        self.destination_dijkstra(target)

        # Find the best detour
        best_detour = self.get_word_vertex(constraint_words[0])
        for i in range(1, len(constraint_words)):
            word = self.get_word_vertex(constraint_words[i])
            if word.total_distance < best_detour.total_distance:
                best_detour = word

        # Initialise Best Path
        distance = best_detour.total_distance
        path = []

        # There is a valid path
        if distance != inf:
            # Backtrack to get path from source to detour
            current = best_detour
            while current.id != start:
                path.append(current.id)
                current = current.source_previous
            path.append(current.id)
            path.reverse()

            # Backtrack to get path from detour to destination
            current = best_detour.destination_previous
            if current is not None:
                while current.id != target:
                    path.append(current.id)
                    current = current.destination_previous
                path.append(current.id)

            # Best Path is finalised
            return path

        # There is no valid path
        else:
            return None

    def __str__(self):
        """ Display the Adjacency List of the Graph in String Form
        :return: String form of Graph
        :time complexity: O(WD) where W = Number of Words in Graph and D = Number of Edges in Graph
        """
        string = ""
        for vertex in self.words:
            string += str(vertex) + "\n"
        return string


if __name__ == "__main__":
    # Best Start Word
    g = WordGraph(["aaa", "bbb", "bab", "aaf", "aaz", "baz", "caa", "cac", "dac", "dad", "ead", "eae", "bae", "abf", "bbf"])
    print(g.best_start_word([2, 7, 5]))
    
    # Constrained Ladder
    start = 0
    end = 1
    detour = [12]
    g = WordGraph(["aaa", "bbb", "bab", "aaf", "aaz", "baz", "caa", "cac", "dac", "dad", "ead", "eae", "bae", "abf", "bbf"])
    print(g.constrained_ladder(start, end, detour))
