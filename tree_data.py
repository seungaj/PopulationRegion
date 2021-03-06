"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""

from __future__ import annotations
import os
from random import randint
import math

from typing import Tuple, List, Optional


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    data_size: the total size of all leaves of this tree.
    colour: The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    _root: the root value of this tree, or None if this tree is empty.
    _subtrees: the subtrees of this tree.
    _parent_tree: the parent tree of this tree; i.e., the tree that contains
        this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    data_size: int
    colour: (int, int, int)
    _root: Optional[object]
    _subtrees: List[AbstractTree]
    _parent_tree: Optional[AbstractTree]

    def __init__(self: AbstractTree, root: Optional[object],
                 subtrees: List[AbstractTree], data_size: int = 0) -> None:
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None

        # 1. Initialize self.colour and self.data_size,
        # according to the docstring.
        # 2. Properly set all _parent_tree attributes in self._subtrees

        red = randint(0, 255)
        blue = randint(0, 255)
        green = randint(0, 255)
        self.colour = (red, green, blue)
        if not self._subtrees:
            self.data_size = data_size
        else:
            self.data_size = 0
            for subtree in self._subtrees:
                self.data_size += subtree.data_size
                subtree._parent_tree = self

    def is_empty(self: AbstractTree) -> bool:
        """Return True if this tree is empty."""
        return self._root is None

    def generate_treemap(self: AbstractTree, rect: Tuple[int, int, int, int]) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]

        """
        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.

        x, y, width, height = rect
        treemap = []
        if self.is_empty() or self.data_size == 0:
            return []
        if self._subtrees == [] and self.data_size > 0:
            return [(rect, self.colour)]
        else:
            for subtree in self._subtrees:
                percent = subtree.data_size / self.data_size
                if width > height:
                    new_width = math.floor(percent * width)
                    treemap.extend(subtree.generate_treemap(
                        (x, y, new_width, height)))
                    x += new_width
                else:
                    new_height = math.floor(percent * height)
                    treemap.extend(subtree.generate_treemap(
                        (x, y, width, new_height)))
                    y += new_height
            return treemap

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        raise NotImplementedError

    def leaf_list(self: AbstractTree) -> List[AbstractTree]:
        """
        Returns the list of leafs
        """
        ans = []
        if self.is_empty():
            return []
        else:
            if self._subtrees:
                for subtree in self._subtrees:
                    ans += subtree.leaf_list()
            else:
                ans.append(self)
        return ans

    def delete_leaf(self: AbstractTree, leaf: AbstractTree) -> None:
        """
        Removes the leaf and update data_size
        """
        leaf._parent_tree._subtrees.remove(leaf)
        a = leaf.data_size
        while leaf._parent_tree is not None:
            if leaf.data_size is not None:
                leaf = leaf._parent_tree
                leaf.data_size -= a
        leaf._parent_tree = None


def l_up(self, leaf: AbstractTree) -> None:
    """Increase the size
    """
    leaf.data_size += math.ceil(leaf.data_size / 100)


def l_down(self, leaf: AbstractTree) -> None:
    """Decrease the size
    """
    if leaf.data_size - math.ceil(leaf.data_size / 100) >= 1:
        leaf.data_size -= math.ceil(leaf.data_size / 100)

    def get_rect(x: int, y: int, rect: List[tuple], subtree: List[tuple])\
            -> AbstractTree:
        """Returns the rect of position x, y
        @rtype: AbstractTree
        """

        for subi in rect:
            sub = subi[0]
            min_x = sub[0]
            max_x = sub[2] + sub[0]
            min_y = sub[1]
            max_y = sub[3] + sub[1]
            if max_x > x > min_x:
                if max_y > y > min_y:
                    return subtree[rect.index(subi)]
        return None

    def l_text(self: FileSystemTree, leaf: FileSystemTree) -> str:
        """ Returns the path from root to the node
        """
        result_str = ""
        data = leaf.data_size
        while leaf._parent_tree is not None:
            result_str = self.get_separator() + str(leaf._root) + result_str
            leaf = leaf._parent_tree
        return str(leaf._root) + result_str + "  (" + str(data) + ")"


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self: FileSystemTree, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!

        self._subtrees = []
        self.path = path
        self.data_size = 0
        if os.path.isfile(path):
            root = os.path.basename(path)
            self.data_size = os.path.getsize(path)
            AbstractTree.__init__(self, root, self._subtrees, self.data_size)
        else:
            root = os.path.basename(path)
            for file in os.listdir(path):
                item = os.path.join(path, file)
                self._subtrees.append(FileSystemTree(item))
            AbstractTree.__init__(self, root, self._subtrees, self.data_size)

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        return "/"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['os', 'random', 'math'],
            'generated-members': 'pygame.*'})
