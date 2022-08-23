""" This module contains algorithms for various DP problems """

__author__ = "Arthur Lee"


def count_encounters(target_difficulty: int, monster_list: list) -> int:
    """ Uses DP to compute the number of possible monster combinations that have a total difficulty exactly equal to
        the target difficulty

    :param target_difficulty: Difficulty to find total number of monster combinations
    :param monster_list: A list of (monster, difficulty) tuples where monster is a string which is the name of the
                         monster while difficulty is a positive integer
    :return: The total number of combinations of monsters where their difficulty sums up to exactly target_difficulty

    :best time complexity: O(DM) where D = target_difficulty and M = len(monster_list)
    :worst time complexity: O(DM)

    :best space complexity: O(DM)
    :worst space complexity: O(DM)
    """
    # Initialise Memory and Base Case
    memory = [None] * (target_difficulty + 1)
    memory[0] = [1] * (len(monster_list) + 1)
    for i in range(1, len(memory)):
        memory[i] = [0] * (len(monster_list) + 1)

    # Solve Sub-problems
    for i in range(1, len(memory)):
        for j in range(1, len(memory[i])):
            index = i - monster_list[j - 1][1]
            if index >= 0:
                memory[i][j] = memory[i][j - 1] + memory[index][j]
            else:
                memory[i][j] = memory[i][j - 1]

    # Solution
    return memory[target_difficulty][len(monster_list)]


def best_lamp_allocation(num_p: int, num_l: int, probs: list) -> float:
    """ Uses DP to compute the highest probability of all plants ready from the optimal division of lamps to plants
    :param num_p: Number of plants we have
    :param num_l: Number of lamps we have
    :param probs: A list of lists where each row corresponds to a plant and each column is the number of lamps. Each
                  cell is the probability that that plant will be ready if it is allocated that specific amount of lamps
    :return: The highest probability of all plants ready from the optimal division of lamps to plants

    :best time complexity: O(PL^2) where P = num_p and L = num_l
    :worst time complexity: O(PL^2)

    :best space complexity: O(PL)
    :worst space complexity: O(PL)

    :note: This function can also compute the appropriate result if the dimensions of num_p, num_l and probs do not
           match. It does this by adding 0s to probs until it meets the value of num_p and num_l. Complexity of the
           algorithm still meets the requirements of O(PL^2)
    """
    # Initialise Memory and Base Case
    memory = [None] * (num_p + 1)
    for i in range(len(memory)):
        memory[i] = [1] * (num_l + 1)

    # Add 0s to probs if less data than num_p
    while len(probs) < num_p:
        probs.append([0] * (num_l + 1))

    # Add 0s to probs if less data than num_l
    for row in probs:
        while len(row) < num_l + 1:
            row.append(0)

    # Solve Sub-problems
    for i in range(1, len(memory)):
        for j in range(len(memory[i])):
            best = memory[i - 1][0] * probs[i - 1][j]
            for k in range(1, j + 1):
                current = memory[i - 1][k] * probs[i - 1][j - k]
                if current > best:
                    best = current
            memory[i][j] = best

    # Solution
    return memory[num_p][num_l]


if __name__ == "__main__":
    # Encounter Difficulty Problem
    target_difficulty = 15
    monster_list = [("bear", 5), ("imp", 2), ("kobold", 3), ("dragon", 10)]
    print(count_encounters(target_difficulty, monster_list))
    
    # Lamp Allocation Problem
    probs = [[0.92, 0.88, 0.07, 0.74, 0.83, 0.73, 0.85, 0.41, 0.94, 0.58, 0.17],
             [0.05, 0.42, 0.01, 0.53, 0.03, 0.13, 0.49, 0.64, 0.13, 0.78, 0.05],
             [0.68, 0.38, 0.86, 0.6, 0.53, 0.49, 0.89, 0.18, 0.69, 0.21, 0.3],
             [0.61, 0.85, 0.17, 0.78, 0.21, 0.05, 0.09, 0.7, 0.08, 0.86, 0.21],
             [0.72, 0.81, 0.12, 0.73, 0.45, 0.8, 0.3, 0.84, 0.89, 0.48, 0.33],
             [0.19, 0.33, 0.01, 0.54, 0.71, 0.56, 0.55, 0.28, 0.29, 0.43, 0.42],
             [0.36, 0.65, 0.38, 0.48, 0.05, 0.28, 0.45, 0.42, 0.49, 0.5, 0.97],
             [0.95, 0.05, 0.73, 0.91, 0.25, 0.16, 0.11, 0.67, 0.48, 0.48, 0.77],
             [0.96, 0.21, 0.19, 0.55, 0.04, 0.58, 0.91, 0.3, 0.92, 0.36, 0.48],
             [0.46, 0.6, 0.76, 0.91, 0.79, 0.92, 0.66, 0.28, 0.48, 0.32, 0.17]]
    print(best_lamp_allocation(10, 10, probs))
