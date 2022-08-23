"""
Uses a modified Kruskal's Algorithm to compute the smallest and second smallest MSTs of a graph provided in the
form of a txt file.
"""

__author__ = "Arthur Lee"

import sys


class DisjointSet:
    """
    Implementation of the Disjoint-Set Data Structure with union-by-height with path compression
    """

    def __init__(self, size):
        """
        Constructor. Initialises a fixed size Disjoint Set

        :param size: Number of items in Disjoint Set
        """
        self.parent = [-1] * size

    def __str__(self):
        """
        Returns the parent array and items a string. For visualization purposes.

        :return: Parent array as string
        """
        return str(self.parent)

    def find(self, a):
        """
        Find method with path compression.

        :param a: Index of Item in set
        :return: Index of Root of a
        """
        if self.parent[a] < 0:
            return a
        else:
            self.parent[a] = self.find(self.parent[a])
            return self.parent[a]

    def union(self, a, b):
        """
        Union by height with path compression

        :param a: Index of Item in set
        :param b: Index of Item in set
        :return: True if union possible, False otherwise
        """
        # Find Roots
        root_a = self.find(a)
        root_b = self.find(b)

        # Union if Roots not equal
        if root_a != root_b:

            # Compute Heights
            height_a = -self.parent[root_a]
            height_b = -self.parent[root_b]

            # Merge Shorter to Taller (b to a if equal)
            if height_a > height_b:
                self.parent[root_b] = root_a
            elif height_b > height_a:
                self.parent[root_a] = root_b
            else:
                self.parent[root_b] = root_a
                self.parent[root_a] = -(height_a + 1)

            # Union is possible
            return True
        else:
            # Union not possible
            return False


class Edge:
    """
    Simple Undirected Edge Class.
    """
    def __init__(self, source, sink, weight):
        """
        Constructor.

        :param source: Source Vertex
        :param sink: Sink Vertex
        :param weight: Weight
        """
        self.source = source
        self.sink = sink
        self.weight = weight

    def __str__(self):
        """
        Display Edge as string

        :return: Edge in string form
        """
        return "(" + str(self.source) + ", " + str(self.sink) + ", " + str(self.weight) + ")"

    def __eq__(self, other):
        """
        Two edges are equal if source, sink, and weight are equal

        :param other: Other edge
        :return: True if self == other, False otherwise
        """
        return self.source == other.source and self.sink == other.sink and self.weight == other.weight


def read_input(filename):
    """
    Function to read input and return its contents in the appropriate format

    :param filename: Name of file
    :return: Appropriate input for computation
    """
    # Open File and read lines
    file = open(filename, "r")
    lines = file.readlines()

    # Get vertex and edge count
    graph_info = lines[0].split()
    v = int(graph_info[0])
    e = int(graph_info[1])

    # Get list of edges
    edges = []
    for i in range(1, len(lines)):
        edge_info = lines[i].split()
        edges.append(Edge(int(edge_info[0]) - 1, int(edge_info[1]) - 1, int(edge_info[2])))

    # Done
    file.close()
    return v, e, edges


def write_output(filename, mst1, mst2):
    """
    Writes output to appropriately named output file

    :param filename: Name of output file
    :param mst1: Smallest MST from computation
    :param mst2: Second Smallest MST from computation
    """
    # Important Variables
    mst1_weight, mst1_edges = mst1[0], mst1[1]
    mst2_weight, mst2_edges = mst2[0], mst2[1]
    output_file = open(filename, "w")

    # Write Smallest MST
    output_file.write("Smallest Spanning Tree Weight = " + str(mst1_weight) + "\n")
    output_file.write("#List of edges in the smallest spanning tree:\n")
    output_file.write(" ".join([str(mst1_edges[0].source + 1), str(mst1_edges[0].sink + 1), str(mst1_edges[0].weight)]))
    for i in range(1, len(mst1_edges)):
        output_file.write("\n")
        output_file.write(" ".join([str(mst1_edges[i].source + 1), str(mst1_edges[i].sink + 1), str(mst1_edges[i].weight)]))

    # Write Second Smallest MST
    output_file.write("\nSecond-smallest Spanning Tree Weight = " + str(mst2_weight) + "\n")
    output_file.write("#List of edges in the second smallest spanning tree:\n")
    output_file.write(" ".join([str(mst2_edges[0].source + 1), str(mst2_edges[0].sink + 1), str(mst2_edges[0].weight)]))
    for i in range(1, len(mst2_edges)):
        output_file.write("\n")
        output_file.write(" ".join([str(mst2_edges[i].source + 1), str(mst2_edges[i].sink + 1), str(mst2_edges[i].weight)]))

    # Done
    output_file.close()


def main(graph):
    """
    Main Method. Implementation of Kruskal's Algorithm modified for finding smallest MST and second smallest MST.

    :param graph: Tuple in form of (v, e, edges) where v = No. of Vertices, e = No. of Edges, edge = List of Edges
    :return: Smallest and 2nd Smallest MST in form of (w, edges) tuple where w = Weight, edges = List of Edges
    """
    # Important Variables
    v, e, edges = graph
    disjoint_set = DisjointSet(v)
    edges.sort(key=lambda ed: ed.weight)
    mst1_weight = 0
    mst1_edges = []

    # Compute Smallest MST
    for edge in edges:

        # Add edge if it does not introduce cycle
        if disjoint_set.union(edge.source, edge.sink):
            mst1_edges.append(edge)
            mst1_weight += edge.weight

        # Done when E = V - 1
        if len(mst1_edges) == v - 1:
            break

    # Reset Variables
    disjoint_set = DisjointSet(v)
    mst2_weight = 0
    mst2_edges = []

    # Compute Initial 2nd Smallest MST
    for edge in edges:

        # Add edge if it does not introduce cycle
        if edge != mst1_edges[-1] and disjoint_set.union(edge.source, edge.sink):
            mst2_edges.append(edge)
            mst2_weight += edge.weight

        # Done when E = V - 1
        if len(mst2_edges) == v - 1:
            break

    # Loop through all edges in 1st MST and run Kruskal's discarding each edge
    for i in range(len(mst1_edges) - 2, -1, -1):

        # Temporary Variables
        disjoint_set = DisjointSet(v)
        mst2_weight_temp = 0
        mst2_edges_temp = []

        # Normal Kruskal's
        for edge in edges:

            # Add edge if it does not introduce cycle
            if edge != mst1_edges[i] and disjoint_set.union(edge.source, edge.sink):
                mst2_edges_temp.append(edge)
                mst2_weight_temp += edge.weight

            # Done when E = V - 1
            if len(mst2_edges_temp) == v - 1:
                break

        # Replace current 2nd MST if new one better
        if mst2_weight_temp < mst2_weight:
            mst2_weight = mst2_weight_temp
            mst2_edges = mst2_edges_temp

    # Sort Edges
    mst1_edges.sort(key=lambda ed: ed.sink)
    mst1_edges.sort(key=lambda ed: ed.source)
    mst2_edges.sort(key=lambda ed: ed.sink)
    mst2_edges.sort(key=lambda ed: ed.source)

    # Done
    return (mst1_weight, mst1_edges), (mst2_weight, mst2_edges)


if __name__ == "__main__":
    # Read Input File
    graph_file = sys.argv[1]
    graph_input = read_input(graph_file)

    # Actual Computation
    result1, result2 = main(graph_input)    # result1 = Smallest MST, result2 = 2nd Smallest MST

    # # Write Output File
    write_output("output_spanning.txt", result1, result2)
