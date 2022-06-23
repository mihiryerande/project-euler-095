# Problem 95:
#     Amicable Chains
#
# Description:
#     The proper divisors of a number are all the divisors excluding the number itself.
#     For example, the proper divisors of 28 are 1, 2, 4, 7, and 14.
#     As the sum of these divisors is equal to 28, we call it a perfect number.
#
#     Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220,
#       forming a chain of two numbers.
#     For this reason, 220 and 284 are called an amicable pair.
#
#     Perhaps less well known are longer chains.
#     For example, starting with 12496, we form a chain of five numbers:
#         12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)
#
#     Since this chain returns to its starting point, it is called an amicable chain.
#
#     Find the smallest member of the longest amicable chain with no element exceeding one million.

def main(n):
    """
    Returns the longest amicable chain where no elements exceed `n`.
    The chain is returned such that the least element in the loop is the first array element.

    Args:
        n (int): Natural number

    Returns:
        (List[int]): Longest amicable chain where no elements exceed `n`. First element is least of the loop.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Generate a mapping of each number (< n) to the sum of its proper divisors
    # Also use this mapping later to keep track of remaining valid numbers
    amicable_next = dict.fromkeys(range(1, n+1), 0)

    # Use a 'reverse'-sieve method, by adding each possible factor to all of its proper multiples
    for f in range(1, n+1):
        for m in range(2*f, n+1, f):
            amicable_next[m] += f

    # Keep track of the largest loop chain seen so far
    loop_best = []

    # Keep traversing elements, and deleting them as they get used
    while len(amicable_next) > 0:
        # Start a new sequence using a not-yet-traversed element
        path_elt_to_index = {}
        path = []
        path_elt, path_next = amicable_next.popitem()  # Pop something random
        amicable_next[path_elt] = path_next  # Put it back for path-walking
        del path_next

        # Follow the amicable sequence
        while path_elt not in path_elt_to_index and path_elt in amicable_next:
            path_elt_to_index[path_elt] = len(path)
            path.append(path_elt)
            path_elt = amicable_next.pop(path_elt)

        if path_elt in path_elt_to_index:
            # Already saw this element in our path, so we found a loop
            # Consider only the looped portion of the path
            loop_start = path_elt_to_index[path_elt]
            if len(path) - loop_start > len(loop_best):
                # Cut down to only the loop portion
                loop_best = path[loop_start:]
            else:
                continue
        else:
            # -> path_elt not in amicable_next
            # `path_elt` either exceeds `n` or has been traversed already
            continue

    # Rotate to have the least element first
    loop_start = min(range(len(loop_best)), key=lambda i: loop_best[i])
    loop_best = loop_best[loop_start:] + loop_best[:loop_start]
    return loop_best


if __name__ == '__main__':
    amicable_limit = int(input('Enter a natural number: '))
    amicable_chain_longest = main(amicable_limit)
    print('Longest amicable chain with no element exceeding {}:'.format(amicable_limit))
    print('    Chain:')
    print('        {}'.format(' →\n        '.join(map(str, amicable_chain_longest))))
    print('    Length = {}'.format(len(amicable_chain_longest)))
    print('    Least  = {}'.format(amicable_chain_longest[0]))
