"""
Given a number N where N > 7 and N is odd, compute three odd prime numbers that sum up to N sorted in
ascending order.
"""

__author__ = "Arthur Lee Yen Rong (31435939)"

import sys
import math
import random


def mod(a, b, n):
    """
    Performs modular exponentiation using the square and multiply method for use in Miller Rabin

    :param a: Integer >= 1
    :param b: Integer >= 1
    :param n: Integer >= 1
    :return: a^b mod n
    """
    # Important Variables
    x = a % n
    result = 1

    # Loop through bits in b
    while b > 0:

        # Update Result if current bit == 1
        if b & 1 == 1:
            result = (result * x) % n

        # Shift b right by 1 and update x
        b >>= 1
        x = (x * x) % n

    # Done
    return result


def is_odd_prime(n):
    """
    Checks if n is odd and prime using Miller Rabin primality testing

    :param n: Integer
    :return: True - If n is odd and probably prime, False - Otherwise
    """
    # Edge Cases
    if n == 3:
        return True
    elif n < 3 or n & 1 == 0:
        return False

    # Number of trials, k = ln(n) due to prime distribution, but we set 10 as threshold to be safe
    k = max(10, math.floor(math.log(n)) + 1)

    # Compute s,t such that n-1 = 2^s * t where t is odd
    s = 0
    t = n - 1
    while t & 1 == 0:
        s += 1
        t >>= 1

    # Perform k Miller Rabin trials
    for _ in range(k):
        a = random.randint(2, n - 2)

        # Miller Rabin (Obtained and Modified From: https://gist.github.com/Ayrx/5884790 Lines 22-30)
        x = mod(a, t, n)
        if x != 1 and x != n - 1:
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
                elif x == 1:
                    return False
            else:
                return False

    # If all tests passed, n is probably prime
    return True


def main(n):
    """
    Main Method. Given a number N where N > 7 and N is odd, compute three odd prime numbers that sum up to N
    sorted in ascending order.

    :param n: Odd Integer > 7
    :return: Three odd primes that sum up to n
    """
    # Check if N is valid
    if n <= 7 or n & 1 == 0:
        return []
    
    # n = a + b + c where a, b, c are odd primes and a <= b <= c
    a, b, c = 3, 3, n - 6

    # At the start of a phase, a and b are odd primes, check if c is odd prime
    while not is_odd_prime(c):

        # If this happens, no possible sum as invariant is broken
        if c < b:
            return []

        # a needs to catch up to b, slice c by 2 and give to a until a is odd prime
        if a < b:
            c -= 2
            a += 2
            while not is_odd_prime(a):
                c -= 2
                a += 2

        # Invariant is a <= b, to maintain this, slice c by 2 and give to b until b is odd prime
        else:
            c -= 2
            b += 2
            while not is_odd_prime(b):
                c -= 2
                b += 2

    # Done
    return [a, b, c]


if __name__ == "__main__":
    # Compute Result
    number = int(sys.argv[1])
    primes = main(number)

    # Write Outputs if exist, Else don't do anything
    output_file = open("output_threeprimes.txt", "w")
    if len(primes) != 0:
        p1, p2, p3 = primes
        output_file.write(" ".join([str(p1), str(p2), str(p3)]))
    output_file.close()
