import sys
import time
import store_credit as sc

def test_it():
    global ref_list
    for credit, L, ans in [
        (100, [5, 75, 25], [1, 2]),
        (200, [150, 24, 79, 50, 88, 345, 3], [0, 3]),
        (8, [2, 1, 9, 4, 4, 56, 90, 3], [3, 4]),
        (32, [1, 1, 1, 1, 32, 2, 2, 2], [4]),
        (42, [3, 8, 12, 80, 18, 12], [2, 4, 5]),
        (1001, [1, 100, 450, 50, 333, 67], [0, 1, 2, 3, 4, 5])]:
        sc.ref_list = L

        result = sc.store_credit(credit, L)
        assert result == ans, \
            "Expected %s, got %s, for list: %s" % (result, ans, L)
    print 'tests passed!'

test_it()
