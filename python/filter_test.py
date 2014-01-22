#!/usr/bin/env python
"""
Script to measure the speed of filtering algorithms. Is there a more efficient
way to filter besides using python's stdlib?
"""

import random
import time

# For this exercise we generate integers as test data and filter by values
# greater than a certain limit.
INT_RANGE = 100       # generate random numbers from 0 up to this
INT_LIMIT = 25        # filter by values greater than this
DATA_SIZE = int(1e6)  # number of ints


class node(object):
    """Generic node class for constructing a linked list."""
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


# Generate a standard list and our custom linked list with test data
rlist = []
rllist = None
curnode = None
for i in xrange(DATA_SIZE):
    randnum = random.randint(0, INT_RANGE)
    rlist.append(randnum)
    if rllist is None:
        # Base case, generate the first node
        curnode = node(randnum)
        rllist = curnode
    else:
        curnode.next = node(randnum)
        curnode = curnode.next

def filterlist(inlist):
    return filter(lambda x: x > INT_LIMIT, inlist)

def filterllist(inlist):
    curnode = inlist
    prevnode = None
    while not curnode is None:
        nextnode = curnode.next
        if not curnode.value > INT_LIMIT:
            if prevnode is None:  # removing first node in list
                inlist = nextnode
            else:
                prevnode.next = nextnode
        else:
            prevnode = curnode
        curnode = nextnode
    return inlist

t1 = time.time()
filtlist = filterlist(rlist)
print "filter() time:", time.time() - t1, "size: "

t2 = time.time()
filtllist = filterllist(rllist)
print "linked list time:", time.time() - t2, "size: "

# Sanity check both lists are equal
i = 0
curnode = filtllist
while not curnode is None:
    assert curnode.value == filtlist[i], "Filtered linked list and list values don't equal"
    i += 1
    curnode = curnode.next
print "Filtered entries: %d" % i
