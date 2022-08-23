""" This module contains an implementation of radix sort for integers >= 0 with different bases and radix sort for strings. """

__author__ = "Arthur Lee"

import math
import random
import time
import matplotlib.pyplot as plt


def num_rad_sort(nums: list, b: int) -> list:
    """ This function applies the radix sort algorithm to sort a list of non-negative integers in ascending
        numerical order using any given base.

    :param nums: List of non-negative integers to be sorted
    :param b: The base used to sort nums
    :return: The nums list sorted in ascending numerical order

    :best time complexity: O(n) if nums contains only 0s
    :worst time complexity: O((n + b) * log_b(M)) where n is length of nums, b is the base,
                           and M is the maximum element in nums

    :best total space complexity: O(n) if nums contains only 0s
    :worst total space complexity: O(n + b) otherwise
    :best auxiliary space complexity: O(1) if nums contains only 0s
    :worst auxiliary space complexity: O(n + b) otherwise
    """
    # Check if nums is empty
    if len(nums) == 0:
        return nums

    # Calculate Maximum Number in nums
    maximum = nums[0]
    for num in nums:
        if num > maximum:
            maximum = num

    # If maximum is 0, list is sorted
    if maximum == 0:
        return nums

    # Determine number of Columns in maximum
    columns = math.floor(math.log(maximum, b)) + 1

    # Apply Counting Sort for each Column
    for column in range(columns + 1):
        num_count_sort_routine(nums, b, column)

    # Return Sorted Array
    return nums


def num_count_sort_routine(nums: list, b: int, column: int) -> list:
    """ A stable version of counting sort modified for radix sort such that it takes into account
        the base and sorts according to the appropriate column

    :param nums: The Array to be sorted
    :param b: Base to be used
    :param column: The Column of the numbers to sort by
    :return: The sorted array

    :best time complexity: O(n + b) where n is length of array and b is the base
    :worst time complexity: O(n + b)

    :total space complexity: O(n + b)
    :auxiliary space complexity: O(n + b)

    :see: num_rad_sort
    """
    # Initialise Count Array
    count_array = [None] * b
    for i in range(len(count_array)):
        count_array[i] = []

    # Update Count Array
    for item in nums:
        count_array[(item // (b ** column)) % b].append(item)

    # Update Input Array
    index = 0
    for i in range(len(count_array)):
        item = count_array[i]
        for j in range(len(item)):
            nums[index] = item[j]
            index += 1

    # Return Sorted Array
    return nums


def base_timer(num_list: list, base_list: list) -> list:
    """ Records the time taken to sort num_list using num_rad_sort with provided bases in base_list.
    :param num_list: Array of non-negative integers to be sorted
    :param base_list: List of bases to use to sort num_list
    :return: List with times taken to sort num_list for each base in base_list
    :see: num_rad_sort
    """
    # Initialise times array and loop through each base
    times = []
    for base in base_list:
        # Record time taken to perform radix sort for provided base and append to times array
        start = time.time()
        num_rad_sort(num_list, base)
        times.append(time.time() - start)
    # Return the times
    return times


def interest_groups(data: list) -> list:
    """ Given data, a list of (name, interests) tuples, groups the names by similar interests
    :param data: A list containing (name, interests) tuples
    :return: A list of lists where each item contains names who share the exact same interests. Names within a group
             are sorted by lexicographical order

    :best time complexity: O(NM) where N is the number of items in data and M is the total number of characters in the
                           longest set of liked things
    :worst time complexity: O(NM)

    :total space complexity: O(N + M)
    :auxiliary space complexity: O(N + M)
    """
    # Check if data is empty
    if len(data) == 0:
        return data

    # Initialise groups
    groups = []

    # Sort Data by Names
    data = special_string_rad_sort(data, 0)

    # Sort and Concatenate Individual Interest Lists
    for i in range(len(data)):
        string_rad_sort(data[i][1])
        data[i] = (data[i][0], "-".join(data[i][1]))

    # Sort Data by Concatenated Interest Lists
    data = special_string_rad_sort(data, 1)

    # Group Names according to Interests
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(data) - 1:
        if data[pointer2][1] == data[pointer1 + 1][1]:
            pointer1 += 1
        else:
            group = []
            for i in range(pointer2, pointer1 + 1):
                group.append(data[i][0])
            groups.append(group)
            pointer2 = pointer1 + 1
            pointer1 += 1

    # Repeat for Last Index
    group = []
    for i in range(pointer2, pointer1 + 1):
        group.append(data[i][0])
    groups.append(group)

    # Return Groups
    return groups


def special_string_rad_sort(data: list, index: int) -> list:
    """ Similar to string_rad_sort but takes a list of (key, value) tuples where either the key
        or value is a string and sorts the tuples in lexicographical order based on either key or value

    :param data: A list of (key, value) tuples
    :param index: 0 to sort by key, 1 to sort by value
    :return: A list of strings sorted in lexicographical order

    :best time complexity: O(M) where M is the total number of characters in either all keys or values
    :worst time complexity: O(M)

    :total space complexity: O(N + K) where N is the number of items in data and K is the length of the
                             longest key or value
    :auxiliary space complexity: O(N + K)

    :see: interest_groups, string_rad_sort
    """
    # Check if strings is empty
    if len(data) == 0:
        return data

    # Find String with Maximum Length
    maximum = len(data[0][index])
    for item in data:
        if len(item[index]) > maximum:
            maximum = len(item[index])

    # Pre-Process by sorting strings by ascending order of length
    data = special_len_count_sort_routine(data, index, maximum)

    # Loop through each column
    for column in range(maximum - 1, -1, -1):

        # Identify strings where column exists
        start_index = len(data) - 1
        for i in range(len(data) - 2, -1, -1):
            if column <= len(data[i][index]) - 1:
                start_index -= 1
            else:
                break

        # Sort appropriate strings
        data = special_string_count_sort_routine(data, index, column, start_index)

    # Return Sorted List
    return data


def special_len_count_sort_routine(data: list, index: int, maximum: int) -> list:
    """ Similar to len_count_sort_routine but takes a list of (key, value) tuples instead.

    :param data: A list of (key, value) tuples
    :param index: 0 to sort by key, 1 to sort by value
    :param maximum: The length of the longest key or value in data
    :return: A list of (key, value) tuples sorted in ascending order by key length or value length

    :best time complexity: O(N + K) where N is the number of items in data and K is the value of maximum
    :worst time complexity: O(N + K)

    :total space complexity: O(N + K)
    :auxiliary space complexity: O(N + K)

    :see: interest_groups, special_string_rad_sort, len_count_sort_routine
    """
    # Initialise Count Array
    count_array = [None] * (maximum + 1)
    for i in range(len(count_array)):
        count_array[i] = []

    # Update Count Array
    for item in data:
        count_array[len(item[index])].append(item)

    # Update Input Array
    index = 0
    for i in range(len(count_array)):
        item = count_array[i]
        for j in range(len(item)):
            data[index] = item[j]
            index += 1

    # Return Sorted Array
    return data


def special_string_count_sort_routine(data: list, index: int, column: int, start_index: int) -> list:
    """ Similar to string_count_sort_routine but takes a list of (key, value) tuples instead.

    :pre: 0 <= start_index <= len(strings) - 1
    :param data: A list of (key, value) tuples
    :param index: 0 to sort by key, 1 to sort by value
    :param column: Column to sort data by
    :param start_index: Index of first item to include in the sort
    :return: A list of (key, value) tuples where data[start_index:len(strings)-1] is sorted based on column

    :best time complexity: O(n) where n = length of data - start_index
    :worst time complexity: O(n)

    :total space complexity: O(n)
    :auxiliary space complexity: O(n)

    :see: interest_groups, special_string_rad_sort, string_count_sort_routine
    """
    # Initialise Count Array
    count_array = [None] * 28
    for i in range(len(count_array)):
        count_array[i] = []

    # Update Count Array
    for i in range(start_index, len(data)):
        item = data[i]
        current_index = ord(item[index][column]) - 95
        if current_index >= 1:  # Item is alphabet
            count_array[current_index].append(item)
        elif current_index == -63:   # Item is space
            count_array[0].append(item)
        else:   # Item is -
            count_array[1].append(item)

    # Update Input Array
    current_index = start_index
    for i in range(len(count_array)):
        item = count_array[i]
        for j in range(len(item)):
            data[current_index] = item[j]
            current_index += 1

    # Return Sorted Array
    return data


def string_rad_sort(strings: list) -> list:
    """ A version of radix sort that sorts strings by lexicographical order.
    :param strings: A list of strings
    :return: A list of strings sorted in lexicographical order

    :best time complexity: O(M) where M is the total number of characters in all strings in strings
    :worst time complexity: O(M)

    :total space complexity: O(N + K) where N is the number of items in strings and K is the length of the
                             longest string
    :auxiliary space complexity: O(N + K)

    :see: interest_groups
    """
    # Check if strings is empty
    if len(strings) == 0:
        return strings

    # Find String with Maximum Length
    maximum = len(strings[0])
    for item in strings:
        if len(item) > maximum:
            maximum = len(item)

    # Pre-Process by sorting strings by ascending order of length
    strings = len_count_sort_routine(strings, maximum)

    # Loop through each column
    for column in range(maximum - 1, -1, -1):

        # Identify strings where column exists
        start_index = len(strings) - 1
        for i in range(len(strings) - 2, -1, -1):
            if column <= len(strings[i]) - 1:
                start_index -= 1
            else:
                break

        # Sort appropriate strings
        strings = string_count_sort_routine(strings, column, start_index)

    # Return Sorted List
    return strings


def len_count_sort_routine(strings: list, maximum: int) -> list:
    """ A modified version of counting sort that given a list of strings and the length of the
        longest string within it, sorts the strings in ascending order based on length.

    :param strings: A list of strings
    :param maximum: The length of the longest string in strings
    :return: A list of strings sorted in ascending order by length

    :best time complexity: O(N + K) where N is the number of items in strings and K is the value of maximum
    :worst time complexity: O(N + K)

    :total space complexity: O(N + K)
    :auxiliary space complexity: O(N + K)

    :see: interest_groups, string_rad_sort
    """
    # Initialise Count Array
    count_array = [None] * (maximum + 1)
    for i in range(len(count_array)):
        count_array[i] = []

    # Update Count Array
    for item in strings:
        count_array[len(item)].append(item)

    # Update Input Array
    index = 0
    for i in range(len(count_array)):
        item = count_array[i]
        for j in range(len(item)):
            strings[index] = item[j]
            index += 1

    # Return Sorted Array
    return strings


def string_count_sort_routine(strings: list, column: int, start_index: int) -> list:
    """ A modified version of counting sort that given a list of strings, column, and start_index,
        sorts the items in strings from start_index to the last item based on the ASCII character at the column (Note:
        for string "hello", column 0 = "h", column 1 = "e", column 2 = "l", etc. and ASCII characters may only include
        lowercase alphabets and the space)

    :pre: 0 <= start_index <= len(strings) - 1
    :param strings: A list of strings
    :param column: Column to sort strings by
    :param start_index: Index of first item to include in the sort
    :return: A list of strings where strings[start_index:len(strings)-1] is sorted based on column

    :best time complexity: O(n) where n = length of strings - start_index
    :worst time complexity: O(n)

    :total space complexity: O(n)
    :auxiliary space complexity: O(n)

    :see: interest_groups, string_rad_sort
    """
    # Initialise Count Array
    count_array = [None] * 27
    for i in range(len(count_array)):
        count_array[i] = []

    # Update Count Array
    for i in range(start_index, len(strings)):
        item = strings[i]
        index = ord(item[column]) - 96
        if index >= 1:  # Item is alphabet
            count_array[index].append(item)
        else:   # Item is space
            count_array[0].append(item)

    # Update Input Array
    index = start_index
    for i in range(len(count_array)):
        item = count_array[i]
        for j in range(len(item)):
            strings[index] = item[j]
            index += 1

    # Return Sorted Array
    return strings


if __name__ == "__main__":
    # Code to for timing radix sort for ints
    random.seed("SOMESEED")

    data1 = [random.randint(0, 2 ** 25) for _ in range(2 ** 15)]
    data2 = [random.randint(0, 2 ** 25) for _ in range(2 ** 16)]

    bases1 = [2 ** i for i in range(1, 23)]
    bases2 = [2 * 10 ** 6 + (5 * 10 ** 5) * i for i in range(1, 10)]

    y1 = base_timer(data1, bases1)
    y2 = base_timer(data2, bases1)
    y3 = base_timer(data1, bases2)
    y4 = base_timer(data2, bases2)

    # Plot First Graph
    plt.plot(bases1, y1, "b-", bases1, y2, "r-")

    plt.xscale("log")
    plt.yscale("linear")

    plt.xlabel("Base")
    plt.ylabel("Runtime (s)")

    plt.title("y1, y2 vs bases1")
    plt.legend(["y1", "y2"])
    plt.grid(True)

    plt.show()

    # Plot Second Graph
    plt.plot(bases2, y3, "g-", bases2, y4, "k-")

    plt.xscale("linear")
    plt.yscale("linear")

    plt.xlabel("Base")
    plt.ylabel("Runtime (s)")

    plt.title("y3, y4 vs bases2")
    plt.legend(["y3", "y4"])
    plt.grid(True)

    plt.show()
