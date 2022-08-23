"""
Driver for sorting.py
"""

__author__ = "Arthur Lee"

from sorting import num_rad_sort, interest_groups


if __name__ == "__main__":
    # Radix Sort with ints
    nums = [43, 101, 22, 27, 5, 50, 15]
    base = 10
    print(num_rad_sort(nums, base))
    
    # Radix Sort with strs
    data = [("nuka", ["birds", "napping"]),
            ("hadley", ["napping birds", "nash equilibria"]),
            ("yaffe", ["rainy evenings", "the colour red", "birds"]),
            ("laurie", ["napping", "birds"]),
            ("kamalani", ["birds", "rainy evenings", "the colour red"])]
    print(interest_groups(data))
