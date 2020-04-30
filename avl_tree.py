# -*- coding: UTF-8 -*-

"""
Copyright:SCUT
Author:kjs
Date:2020/4/13
Description: Algorithm analysis and design course: AVL tree
"""

class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0


class AVLTree(object):
    def __init__(self):
        self.root = None

    def find(self, key):
        if self.root is None:
            return None
        else:
            return self._find(key, self.root)

    def _find(self, key, node):
        if node is None:
            return None
        elif key < node.key:
            return self._find(key, node.left)
        elif key > node.key:
            return self._find(key, node.right)
        else:
            return node

    def findMin(self):
        if self.root is None:
            return None
        else:
            return self._findMin(self.root)

    def _findMin(self, node):
        if node.left:
            return self._findMin(node.left)
        else:
            return node

    def findMax(self):
        if self.root is None:
            return None
        else:
            return self._findMax(self.root)

    def _findMax(self, node):
        if node.right:
            return self._findMax(node.right)
        else:
            return node

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def singleLeftRotate(self, node):
        k1 = node.left
        node.left = k1.right
        k1.right = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.left), node.height) + 1
        return k1

    def singleRightRotate(self, node):
        k1 = node.right
        node.right = k1.left
        k1.left = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.right), node.height) + 1
        return k1

    def doubleLeftRotate(self, node):
        node.left = self.singleRightRotate(node.left)
        return self.singleLeftRotate(node)

    def doubleRightRotate(self, node):
        node.right = self.singleLeftRotate(node.right)
        return self.singleRightRotate(node)

    def put(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self.root = self._put(key, self.root)

    def _put(self, key, node):
        if node is None:
            node = Node(key)
        elif key < node.key:
            node.left = self._put(key, node.left)
            if (self.height(node.left) - self.height(node.right)) == 2:
                if key < node.left.key:
                    node = self.singleLeftRotate(node)
                else:
                    node = self.doubleLeftRotate(node)

        elif key > node.key:
            node.right = self._put(key, node.right)
            if (self.height(node.right) - self.height(node.left)) == 2:
                if key < node.right.key:
                    node = self.doubleRightRotate(node)
                else:
                    node = self.singleRightRotate(node)

        node.height = max(self.height(node.right), self.height(node.left)) + 1
        return node

    def delete(self, key):
        self.root = self.remove(key, self.root)

    def remove(self, key, node):
        if node is None:
            print('Error,key not in tree')
        elif key < node.key:
            node.left = self.remove(key, node.left)
            if (self.height(node.right) - self.height(node.left)) == 2:
                if self.height(node.right.right) >= self.height(node.right.left):
                    node = self.singleRightRotate(node)
                else:
                    node = self.doubleRightRotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1

        elif key > node.key:
            node.right = self.remove(key, node.right)
            if (self.height(node.left) - self.height(node.right)) == 2:
                if self.height(node.left.left) >= self.height(node.left.right):
                    node = self.singleLeftRotate(node)
                else:
                    node = self.doubleLeftRotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1

        elif node.left and node.right:
            if node.left.height <= node.right.height:
                minNode = self._findMin(node.right)
                node.key = minNode.key
                node.right = self.remove(node.key, node.right)
            else:
                maxNode = self._findMax(node.left)
                node.key = maxNode.key
                node.left = self.remove(node.key, node.left)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
        else:
            if node.right:
                node = node.right
            else:
                node = node.left

        return node

    def display(self):
        lines, _, _, _ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is None and node.left is None:
            line = '%s' % node.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s' % node.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s' % node.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s' % node.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


if __name__ == "__main__":
    avl_tree = AVLTree()

    print("---------Initialize with 0-10-----------")
    for i in range(10):
        avl_tree.put(i)
    avl_tree.display()

    print("---------add a item: 10 RR -----------")
    avl_tree.put(10)
    avl_tree.display()

    print("---------add a item: -1 -----------")
    avl_tree.put(-1)
    avl_tree.display()

    print("---------add a item: -2 LL -----------")
    avl_tree.put(-2)
    avl_tree.display()

    print("---------delete a item: -2 -----------")
    avl_tree.delete(-2)
    avl_tree.display()

    print("---------delete a item: -1 -----------")
    avl_tree.delete(-1)
    avl_tree.display()