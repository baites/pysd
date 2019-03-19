"""Implement a pure python binary search tree"""

from pyds.BinarySearchTree import BinarySearchTreeNode, BinarySearchTree


class SimpleBinarySearchTreeNode(BinarySearchTreeNode):
    """Implement a simple tree node."""
    def __init__(self, key):
        """Constructor."""
        super().__init__(key)

    def update(self):
        """No need for update in a simple node."""
        pass


class SimpleBinarySearchTree(BinarySearchTree):
    """Implement a simple BST."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    def insert(self, node):
        """Insert a node in the tree."""
        # Call BST insert first
        super().insert(node)
        # Implement insert operation
        if self._root is None:
            self._root = node
        else:
            self._root._insert(node)

    def delete(self, key):
        """Delete a node from the tree."""
        # Call BST delete first
        super().delete(key)
        # Implement delete operation
        node = self.find(key)
        deleted = None
        if not key == node.key:
            return deleted
        if node is self._root:
            pseudoroot = BinarySearchTreeNode(None)
            pseudoroot.left = self._root
            self._root.parent = pseudoroot
            deleted = self._root._delete()
            self._root = pseudoroot.left
            if self._root is not None:
                self._root.parent = None
        else:
            deleted = node._delete()
        deleted.parent = None
        return deleted

    @staticmethod
    def _merge_at_root(lnode, rnode, root):
        root.left = lnode
        root.right = rnode
        lnode.parent = root
        rnode.parent = root
        root.update()
        return root

    @classmethod
    def _fast_merge_trees(cls, ltree, rtree):
        """Merge fast for separated trees."""
        root = ltree._root.max()
        ltree.delete(root.key)
        ltree._root = cls._merge_at_root(
            ltree._root, rtree._root, root
        )
        rtree._root = None

    @classmethod
    def _slow_merge_trees(cls, ltree, rtree):
        """Merge slow for non separated trees."""
        node = rtree.min()
        while node is not None:
            key = node.key
            node = rtree.delete(key)
            ltree.insert(node)
            node = rtree.min()

    def merge(self, tree):
        """Merge tree to self."""
        if self._root is None or tree._root is None:
            return
        rootmax = self._root.max()
        treemin = tree.min()
        if rootmax.key < treemin.key:
            self._fast_merge_trees(self, tree)
        else:
            self._slow_merge_trees(self, tree)