#!/usr/bin/env python

## Simple binary tree class and tree traversals

class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.val)

def printit(x):
    print x,

class BinTree(object):
    def __init__(self, root):
        self.root = root

    def _inorder(self, node, func):
        if node is None:
            return
        self._inorder(node.left, func)
        func(node)
        self._inorder(node.right, func)

    def printInorder(self):
        self._inorder(self.root, printit)

    def _preorder(self, node, func):
        if node is None:
            return
        func(node)
        self._preorder(node.left, func)
        self._preorder(node.right, func)

    def printPreorder(self):
        self._preorder(self.root, printit)

    def _postorder(self, node, func):
        if node is None:
            return
        self._postorder(node.left, func)
        self._postorder(node.right, func)
        func(node)

    def printPostorder(self):
        self._postorder(self.root, printit)

    def _levelorder(self, node, func):
        q = [node]
        while q:
            n = q.pop(0)
            if n is None:
                continue
            func(n)
            q.append(n.left)
            q.append(n.right)

    def printLevelorder(self):
        self._levelorder(self.root, printit)


# Builds a tree like this:
#       F
#     /    \
#    B      G
#   / \      \
#  A   D      I
#     / \    /
#    C   E  H
tree = BinTree(Node("F",
    Node("B", Node("A"), Node("D", Node("C"), Node("E"))),
    Node("G", None, Node("I", Node("H")))))

print "\nprintInorder:"
tree.printInorder()
print "\nprintPreorder:"
tree.printPreorder()
print "\nprintPostorder:"
tree.printPostorder()
print "\nprintLevelorder:"
tree.printLevelorder()
