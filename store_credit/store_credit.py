"""Store Credit

Programming exercise based on
http://programmingpraxis.com/2011/02/15/google-code-jam-qualification-round-africa-2010/

You receive a credit C at a local store and would like to buy some items.
You first walk through the store and create a list L of all available
items (a list of ints). From this list you would like to buy items that
add up to the entire value of the credit. The solution you provide will
consist of the n integers indicating the positions of the items in your
list, L (smaller number first).

Examples:

With C=100 and L={5,75,25} the solution is 2,3.

With C=200 and L={150,24,79,50,88,345,3} the solution is 1,4.

With C=8 and L={2,1,9,4,4,56,90,3} the solution is 4,5.
"""

import sys
import time

ref_list = []

def store_credit(credit, L):

    if credit in L:
        return [ref_list.index(credit)]

    L2 = filter(lambda x: x < credit, L)
    while L2:
        # pop off the highest valued item and recursively find the combination
        # of remaining items that sum to that highest valued item
        mx = max(L2)
        L2.remove(mx)
        newsum = credit - mx
        combo = store_credit(newsum, L2)

        if combo:  # found a potential combination of items
            idx = ref_list.index(mx)
            while idx in combo:  # for duplicates
                idx = ref_list.index(mx, idx+1)
            return sorted(combo + [idx])

        # didnt find a potential combo, try the next expensive item
        L2 = filter(lambda x: x < mx, L2)


if __name__ == '__main__':

    try:
        L = [int(i) for i in sys.argv[2].split(',')]
        credit = int(sys.argv[1])
    except:
        print 'usage: %s credit \'num1,num2,...\'' % sys.argv[0]
        sys.exit(1)

    ref_list = L
    start_t = time.time()
    print store_credit(credit, L)
    print 'time: ', time.time() - start_t
