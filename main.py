import random
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


class RBNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.color = "black"
        self.parent = None


class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        y = None
        z = self.root
        while z is not None:
            y = z
            if key < z.key:
                z = z.left
            else:
                z = z.right
        node = Node(key)
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node


class RBST:
    def __init__(self):
        self.NIL = RBNode(None)
        self.root = self.NIL

    def insert(self, key):
        y = self.NIL
        x = self.root
        while x is not self.NIL:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right
        node = RBNode(key)
        node.parent = y
        if y is self.NIL:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        node.left = self.NIL
        node.right = self.NIL
        node.color = "red"
        self.fixup(node)

    def fixup(self, node):
        while node.parent.color == "red":
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == "red":
                    node.parent.color = "black"
                    y.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.leftrotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.rightrotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == "red":
                    node.parent.color = "black"
                    y.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rightrotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.leftrotate(node.parent.parent)
        self.root.color = "black"

    def leftrotate(self, node):
        y = node.right
        node.right = y.left
        if y.left is not self.NIL:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is self.NIL:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def rightrotate(self, node):
        y = node.left
        node.left = y.right
        if y.right is not self.NIL:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is self.NIL:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def depth(self, node):
        if node is self.NIL or node is None:
            return 0
        lefth = depth(self, node.left)
        righth = depth(self, node.right)
        return max(lefth, righth) + 1

    def fillTree(self, n, rand):
        values = []
        for x in range(0, n):
            values.append(x)
        if rand:
            random.shuffle(values)
        for x in values:
            self.insert(x)
        return self.depth(self.root)


class AVL:
    def __init__(self):
        self.root = None

    def insert(self, node, key):
        if not node:
            node = AVLNode(key)
            self.root = node
            return node
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)
        node.height = 1 + max(self.getHeight(node.left),
                              self.getHeight(node.right))
        balance = self.getBalance(node)
        # double Left
        if balance > 1 and key < node.left.key:
            return self.rightRotate(node)
        # double Right
        if balance < -1 and key > node.right.key:
            return self.leftRotate(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)
        return node

    def leftRotate(self, z):
        y = z.right
        node = y.left
        y.left = z
        z.right = node
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        node = y.right
        y.right = z
        z.left = node
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)


# generating either a BST or a RBST tree
def fillTree(tree, n, rand):
    values = []
    for x in range(0, n):
        values.append(x)
    if rand:
        random.shuffle(values)
    for x in values:
        tree.insert(x)
    return depth(tree, tree.root)


# generating an AVL tree
def fillAVLtree(tree, numElem, rand):
    values = []
    for x in range(0, numElem):
        values.append(x)
    if rand:
        random.shuffle(values)
    root = None
    for x in values:
        root = tree.insert(root, x)
    return root.height


# height method for BST and RBST
def depth(tree, node):
    if node is None:
        return 0
    lefth = depth(tree, node.left)
    righth = depth(tree, node.right)
    return max(lefth, righth) + 1

def main():
    height = []
    x = []
    time = []
    create = input("what type of tree do you want to see? BST, RBST, AVL")
    rand = input("random or sequential?")
    if rand == "random":
        rand = True
    else:
        rand = False
    for i in range(1, 11):
        if create == "BST":
            tree = BST()
            height.append(fillTree(tree, i, rand))
        elif create == "RBST":
            tree = RBST()
            height.append(fillTree(tree, i, rand)-1)
        else:
            tree = AVL()
            height.append(fillAVLtree(tree, i, rand))
        x.append(i)
    plt.plot(x, height)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Tree height')
    plt.show()

def main2():
    heightb = []
    heightr = []
    heighta = []
    x = []
    rand = input("random or sequential?")
    if rand == "random":
        rand = True
    else:
        rand = False
    for i in range(1, 30):
        #bst = BST()
        #heightb.append(fillTree(bst, i, rand))
        rbst = RBST()
        heightr.append(fillTree(rbst, i, rand)-1)
        avl = AVL()
        heighta.append(fillAVLtree(avl, i, rand))
        x.append(i)
    #plt.plot(x, heightb)
    plt.plot(x, heightr)
    plt.plot(x, heighta)
    plt.legend(["RBST", "AVL"], title="Tipologia alberi")#manca nella legenda il BST
    plt.xlabel('Number of Nodes')
    plt.ylabel('Tree height')
    plt.show()

if __name__ == "__main__":
    main2()

