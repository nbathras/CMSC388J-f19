import math

def hello_world():
    """ Returns 'Hello, World!'

    Arguments:
    None

    Usage:
    >>> hello_world()
    'Hello, World!'
    """

    return 'Hello, World!'


def sum_without_dups(l):
    """ Sums values in l, not counting duplicates.

    Arguments:
    l -- a list of integers

    Usage:
    >>> sum_unique([])
    0
    >>> sum_unique([4, 4, 5])
    9
    >>> sum_unique([4, 2, 5])
    11
    >>> sum_unique([2, 2, 2, 2, 1])
    3
    """

    sum = 0
    s = set(l)

    for entr in s:
        sum = sum + entr

    return sum

def palindrome(x):
    """ Determines if x, an integer or string, is a palindrome, i.e.
    has the same value reversed.

    Arguments:
    x -- an integer or string

    Usage:
    >>> palindrome(1331)
    True
    >>> palindrome('racecar')
    True
    >>> palindrome(1234)
    False
    >>> palindrome('python')
    False
    """

    convert = str(x)

    return convert == convert[::-1]

def sum_multiples(num):
    """ Sums up all multiples of 3 and 7 upto and not including num.

    Arguments:
    num -- a positive integer

    Usage:
    >>> sum_multiples(10) # Multiples: [3, 6, 7, 9]
    25
    >>> sum_multiples(3) # Multiples: []
    0
    >>> sum_multiples(7) # Multiples: [3, 6]
    9
    >>> sum_multiples(16) # Multiples: [3, 6, 7, 9, 12, 14, 15]
    66
    """
    sum = 0
    # for (i = 1; i < num; i++):
    for i in range(1, num):
        if (i % 3 == 0) or (i % 7 == 0):
            sum = sum + i
        i = i + 1

    return sum

def num_func_mapper(nums, funs):
    """ Applies each function in funs to the list of numbers, nums, and
    returns a list consisting of the results of those functions.

    Arguments:
    nums -- a list of numbers
    funs -- a list of functions
          - each function in funs acts on a list of numbers and returns a number

    Usage:
    >>> f_list = [sum_unique, sum]
    >>> num_list = [2, 2, 2, 4, 5]
    >>> all_the_sums(num_list, f_list)
    [11, 15]
    """
    l = list()

    for func in funs:
        l.append(func(nums))

    return l

def pythagorean_triples(limits):
    """ Finds all pythagorean triples where a, b, and c (sides of the triangle)
    are all less than n units long. This function should not return distinct tuples
    that still represent the same triangle. For example, (3, 4, 5) and (4, 3, 5)
    are both valid pythagorean triples, but only one should be in the final list.

    Arguments:
    n -- a positive integer

    Usage:
    >>> pythagorean_triples(10)
    [(3, 4, 5)]
    >>> pythagorean_triples(11)
    [(3, 4, 5), (6, 8, 10)]
    >>> pythagorean_triples(20)
    [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
    """

    l = list()

    for b in range(limits):
        for a in range(1, b):
            c = math.sqrt(a * a + b * b)
            
            if c >= limits:
                break

            if c % 1 == 0:
                c = int(c)
                l.append((a,b,c))

    return l