from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Complexity Analysis: N is the table size
        Best Case: O(N)
        Worst Case: O(N)
        """
        self.table = ArrayR(self.TABLE_SIZE)
        self.count = 0

    def hash(self, key: K, level = 0) -> int:
        if level < len(key):
            return ord(key[level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity Analysis: N is length of the key
        Best Case: O(1) when the key is found at level 0
        Worst Case: O(N) when the key is located at level N - 1
        """
        def get(table, level):
            pos = self.hash(key, level)
            if isinstance(table[pos], ArrayR):
                return get(table[pos], level + 1)
            if table[pos] is None or not table[pos][0] == key:
                raise KeyError
            return table[pos][1]

        return get(self.table, 0)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity Analysis: N is length of the key
        Best Case: O(1) when the hash at level 0 is empty or when the key 
                   is found at level 0 so we can just reassign straight away
        Worst Case: O(N) when there is already a pair in the cell. We have to
                    create a new table and keep reassigning the values. It is
                    worst when we have to go to the deepest level of both the existing
                    key and the new key. e.g. inserting "lin", then "link"
                    before: lin
                    after : l - i - n - ''
                                      \ k
        """
        def update(table, k, v, level):
            pos = self.hash(k, level)
            if table[pos] is None:
                table[pos] = (k, v)
                return table
            
            if isinstance(table[pos], ArrayR):
                table[pos] = update(table[pos], k, v, level + 1)
                return table
            
            x, y = table[pos][0], table[pos][1]
            if x == k:
                table[pos] = (k, v)
                self.count -= 1
                return table
            table[pos] = ArrayR(self.TABLE_SIZE)
            table[pos] = update(table[pos], x, y, level + 1)
            table[pos] = update(table[pos], k, v, level + 1)
            return table

        self.count += 1
        self.table = update(self.table, key, value, 0)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        
        Complexity Analysis: N is length of the key, A is value of self.TABLE_SIZE
        Best Case: O(1) when the deleted item is found at level 0 and therefore need no merging
        Worst Case: O(N * A) when key is found at the deepest level, and after deleting
                    that key, only one key is left at that level. So we have to keep merging it to
                    the upper level e.g. only two keys: "lin" and "link", delete "lin", visualisation:
                    l - i - n - ''
                              \ k
                    l - i - nk
                    l - ink
                    link
        """
        deleted = False
        def delete(table, level):
            nonlocal deleted
            pos = self.hash(key, level)
            if isinstance(table[pos], ArrayR):
                table[pos] = delete(table[pos], level + 1)
            if (table[pos] is None or not table[pos][0] == key) and not deleted:
                raise KeyError
            if table[pos][0] == key:
                table[pos] = None
                deleted = True

            if level:
                filled = None
                filled_count = 0
                for i in range(len(table)):
                    if isinstance(table[i], ArrayR):
                        return table
                    if table[i] is None:
                        continue
                    filled = table[i]
                    filled_count += 1

                if filled_count == 1:
                    table = filled
            
            return table
        
        self.count -= 1
        self.table = delete(self.table, 0)

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Complexity Analysis: N is length of the key
        Best Case: O(1) when the key is found at level 0
        Worst Case: O(N) when the key is located at level N - 1
        """
        try:
            _ = self[key]
        except KeyError:
            raise KeyError

        result = []
        def traverse(table, level):
            pos = self.hash(key, level)
            result.append(pos)
            if not isinstance(table[pos], ArrayR):
                return
            traverse(table[pos], level + 1)
        
        traverse(self.table, 0)
        return result
        
    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.

        Complexity Analysis: N is the number of words inserted, A is value of self.TABLE_SIZE,
                             L is length of the longest word
        Best Case: O(A) when all the keys are located at level 0
        Worst Case: O(N * A * L) when all the keys are located at their deepest levels
        """
        result = []
        def traverse(curr, char):
            pos = self.hash(char)
            if curr[pos] is None:
                return
            if isinstance(curr[pos], ArrayR):
                traverse(curr[pos], "")
                for i in range(ord('a'), ord('z') + 1):
                    traverse(curr[pos], chr(i))
            else:
                result.append(curr[pos][0])

        traverse(self.table, "")
        for i in range(ord('a'), ord('z') + 1):
            traverse(self.table, chr(i))

        return result