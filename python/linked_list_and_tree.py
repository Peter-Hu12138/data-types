from __future__ import annotations
from typing import Any, Optional, Iterable

class _Node:
    item: Any
    next: Optional[_Node] = None

    def __init__(self, item, next=None):
        self.item = item
        self.next = next

    def add_next(self, next: _Node):
        self.next = next

#TODO: continue working on maintaning end.
class LinkedList():
    """
    An implementation of ADT linked list.

    This implementation has an _end attribute which is for optimizing append efficiency. 
    However, note that this is still not a double linked list due to _Node design.

    Efficiency (in terms of length of the list):
        - append - O(1)
        - pop(i) - O(i)
        - remove(value) - WC O(n)
    
    Representation invariant:
        - len(self) == len(self.to_list())
    """
    _front: Optional[_Node]
    _end: Optional[_Node]
    _len: int

    def __init__(self, items: Iterable = None):
        self._front = None
        self._end = None
        self._len = 0

        if items is not None:
            for item in items:
                self.append(item)

    def maximum(self) -> float:
        """ Return the maximum element in the list.
        Preconditions:
            - the list is not empty
            - every element in this list is a float
        """
        curr_node = self._front
        curr_num = curr_node.item

        while curr_node is not None:
            if curr_node.item > curr_num:
                curr_num = curr_node.item
            curr_node = curr_node.next  # increment at the end to make sure next round of block is executed after check

        return curr_num

    def check_len(self):
        assert len(self) == len(self.to_list())

    def insert(self, element: Any, index: int) -> None:
        """
        Insert an element at index of the list
        Precondition:
            - index >= 0
        """
        new_node = _Node(element)
        if index < 0:
            raise IndexError("index should be greater than or equal to 0")
        elif index >= self._len:
            self.append(element)
            return
        elif index == 0:
            new_node.next = self._front
            self._front = new_node
            self._len += 1
            return
        
        # case when we need to find where to insert
        curr = self._front
        curr_index = 0
        while curr is not None:
            if curr_index == index - 1:
                new_node.next, curr.next = curr.next, new_node
                self._len += 1
                return 
            curr_index += 1
            curr = curr.next
            """
            do not forget this with linked list
            acilliary line "curr_index += 1" is important to help us track the index
            but curr = curr.next is what really does the traversal
            """

    def pop(self, i: Optional[int] = None) -> Optional[Any]:
        """
        Pop and return the item if a valid index is given.
        Raise IndexError otherwise.
        """
        if i is None:
            i = self._len - 1

        if self._front is None:
            raise IndexError("pop from empty list")
        if i < 0:
            raise IndexError("index should be greater than or equal to 0")
        elif i >= self._len:
            raise IndexError("pop index out of range")
        elif i == 0:
            item = self._front.item
            if self._front is self._end:
                self._front = None
                self._end = None
            else:
                self._front = self._front.next
            self._len -= 1
            return item
        else:
            curr = self._front
            curr_index = 0
            while curr.next is not None:
                if curr_index == i - 1:
                    item = curr.next.item
                    curr.next = curr.next.next
                    if i == self._len - 1:
                        self._end = curr
                    self._len -= 1
                    return item
                curr = curr.next  # traverse along the list by going to the next node
                curr_index += 1  # keeps track the index

            raise IndexError("damn it, keep the fucking index below len(self)")

    def remove(self, value: Any) -> bool:
        """Value-based deletion.

        >>> a = LinkedList([1,2,3])
        >>> a.remove(1)
        True
        >>> a.to_list() == [2, 3]
        True
        >>> a = LinkedList()
        >>> a.remove(None)
        False
        """
        # Alternative:
        # prev, curr = None, self._first
        # while not (curr is None or curr.item == item):
        #     prev, curr = curr, curr.next
        # # Optional: Assert what we know after the loop ends
        # assert curr is None or curr.item == item
        # if curr is None:
        #     raise ValueError
        # else:  # curr.item == item (the item was found)
        #     if prev is None:  # curr is the first node in the list
        #         self._first = curr.next
        #     else:
        #     prev.next = curr.next
        if self._front is None:
            return False
        if self._front.item == value:  # only case where we need to change self._front
            if self._front is self._end:
                self._front = None
                self._end = None
            else:
                self._front = self._front.next
            self._len -= 1
            return True

        prev, curr = self._front, self._front.next
        i = 1
        while curr is not None:
            if curr.item == value:
                prev.next = curr.next
                if i == self._len - 1:
                    self._end = prev
                self._len -= 1
                return True
            prev, curr = curr, curr.next
            i += 1
        return False

    def append(self, element: Any) -> None:
        """
        Append an element at the end
        """
        new_node = _Node(element)
        if self._front is None:
            self._front = new_node
        else:
            self._end.add_next(new_node)
        self._end = new_node
        self._len += 1

    def __getitem__(self, index: int) -> _Node | None:
        """
            Return the element at index, index
            Raise IndexError when index is out of reach;

            Preconditions:
                index >= 0
        """
        if self._front is None:
            raise IndexError
        else:
            curr_node = self._front
        
        while curr_node is not None:
            if index == 0:
                return curr_node.item
            index -= 1
            curr_node = curr_node.next
        
        raise IndexError

        

    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this linked list.

        >>> linky = LinkedList()
        >>> linky.__contains__(10)
        False
        >>> node2 = Node(20)
        >>> node1 = Node(10, node2)
        >>> linky._first = node1
        >>> linky.__contains__(20)
        True
        """
        curr = self._front

        while curr is not None:
            if curr.item == item:
                # We've found the item and can return early.
                return True

            curr = curr.next

        # If we reach the end of the loop without finding the item,
        # it's not in the linked list.
        return False

    def to_list(self) -> list[Any]:
        """
        Returns a python list version of the linked list
        """
        lst = []
        curr = self._front
        while curr is not None:
            lst.append(curr.item)
            curr = curr.next
        return lst

    def __repr__(self) -> str:
        """
        Returns a string representation
        """
        return repr(self.to_list())
    def __len__(self):
        return self._len

class Tree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def add(self, subtree: Tree):
        self._subtrees.append(subtree)

    def _delete_root(self) -> None:
        """Remove the root item of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if self._subtrees == []:
            self._root = None
        else:
            # Get the last subtree in this tree.
            chosen_subtree = self._subtrees.pop()

            self._root = chosen_subtree._root
            self._subtrees.extend(chosen_subtree._subtrees)

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()  # delete the root
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                if deleted and subtree.is_empty():
                    # The item was deleted and the subtree is now empty.
                    # We should remove the subtree from the list of subtrees.
                    # Note that mutate a list while looping through it is
                    # EXTREMELY DANGEROUS!
                    # We are only doing it because we return immediately
                    # afterwards, and so no more loop iterations occur.
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    # The item was deleted, and the subtree is not empty.
                    return True

            # If the loop doesn't return early, the item was not deleted from
            # any of the subtrees. In this case, the item does not appear
            # in this tree.
            return False

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __contains__(self, item):
        if self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

if __name__ == "__main__":
    a = LinkedList([1,2,3])
    for i in a:
        print(i)
    a.append(50)
    assert len(a) == 4
    assert a._end.item == 50
    a.remove(1)
    assert len(a) == 3
    assert a._end.item == 50
    a.remove(50)
    assert len(a) == 2
    assert a._end.item == 3
    a.pop(1)
    assert len(a) == 1
    assert a._end.item == 2
    a.insert(1, 0)
    a.insert(100, 2)
    assert len(a) == 3
    assert a._end.item == 100
    a.pop(len(a) - 1)
    assert len(a) == 2
    assert a._end.item == 2
    a.pop()
    assert len(a) == 1
    assert a._end.item == 1