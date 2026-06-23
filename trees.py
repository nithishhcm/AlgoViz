"""
algorithms/trees.py — Tree algorithm implementations.
Inorder, Preorder, Postorder traversals.
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert_bst(root, val):
    """Insert value into BST."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root


def inorder(root, result=None):
    """
    Inorder Traversal (Left → Root → Right) — O(n) time, O(h) space.
    Visits nodes in sorted order for a BST.
    """
    if result is None:
        result = []
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result


def preorder(root, result=None):
    """
    Preorder Traversal (Root → Left → Right) — O(n) time, O(h) space.
    Useful for copying/serialising a tree.
    """
    if result is None:
        result = []
    if root:
        result.append(root.val)
        preorder(root.left, result)
        preorder(root.right, result)
    return result


def postorder(root, result=None):
    """
    Postorder Traversal (Left → Right → Root) — O(n) time, O(h) space.
    Useful for deleting a tree or evaluating expressions.
    """
    if result is None:
        result = []
    if root:
        postorder(root.left, result)
        postorder(root.right, result)
        result.append(root.val)
    return result


if __name__ == "__main__":
    values = [50, 30, 70, 20, 40, 60, 80]
    root = None
    for v in values:
        root = insert_bst(root, v)

    print("Inorder (sorted):", inorder(root))
    print("Preorder:         ", preorder(root))
    print("Postorder:        ", postorder(root))
