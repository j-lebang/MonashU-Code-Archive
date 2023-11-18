from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    MIN_CAPACITY = 1

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Complexity Analysis: N is the table size
        Best Case: O(N)
        Worst Case: O(N)
        """
        if sizes:
            self.TABLE_SIZES = sizes
        
        if internal_sizes:
            self.INTERNAL_TABLES_SIZES = internal_sizes
        else:
            self.INTERNAL_TABLES_SIZES = self.TABLE_SIZES

        self.size_index = 0
        self.top_table: ArrayR[(K1, LinearProbeTable) | None] = ArrayR(self.TABLE_SIZES[self.size_index]) # O(N)
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Complexity Analysis: N is the table size, M is the internal table size, K is hash2(key2)
        Best Case: O(len(key)) When the key you are finding is not in the table
        Worst Case: O(len(key) + N + (M + K * M)) When adding a new LinearProbeTable to the end of the outer table,
                     and adding the value to the end of the inner table.
        """

        top_index = self.hash1(key1) # O(len(key))

        for _ in range(self.table_size): # O(N)
            if self.top_table[top_index] is None:
                if is_insert:
                    table = LinearProbeTable(self.INTERNAL_TABLES_SIZES) # O(M)
                    self.top_table[top_index] = (key1, table)
                    table.hash = lambda k: self.hash2(k, table)
                    self.count +=1
                    sub_index = self.top_table[top_index][1]._linear_probe(key2, is_insert) # Best: O(K) Worst: O(K * M)
                    return top_index, sub_index
                else:
                    raise KeyError(key1)
                
            elif self.top_table[top_index][0] == key1:
                sub_index = self.top_table[top_index][1]._linear_probe(key2, is_insert) # Best: O(K) Worst: O(K * M)
                return top_index, sub_index
            else:
                top_index = (top_index + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1, key2)
        

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity Analysis: N is the table size. M is the inner table size
        Best Case: O(N) When key is None
        Worst Case: O(len(key) + N + M) When finding the keys of the inner table at the end of the outer table.
        """
        if key is None:
            for entry in self.top_table: # O(N)
                if entry is not None:
                    yield entry[0]
        else:
            top_index = self.hash1(key) # O(len(key))
            for _ in range(self.table_size): # O(N)
                if self.top_table[top_index][0] == key:
                    for sub_key in self.top_table[top_index][1].keys(): #O(M)
                        yield sub_key
                top_index = (top_index + 1) % self.table_size


    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity Analysis: N is the table size. M is the inner table size
        Best Case: O(N) When key is None.
        Worst Case: O(N + M) When iterating the whole table to find the position and returning the keys of the inner table. 
        """
        if key is None:
            res = []
            for table in self.top_table: # O(N)
                if table is not None:
                    res.append(table[0]) 
            return res
        

        top_index = self.hash1(key) # O(len(key))
        for _ in range(self.table_size):    # O(N)
            if self.top_table[top_index][0] == key:
                return self.top_table[top_index][1].keys() # O(M)
            top_index = (top_index + 1) % self.table_size
    
    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity Analysis: N is the table size. M is the inner table size
        Best Case: O(len(key) + M) getting the value of the inner table at the first position.
        Worst Case: O(N * M) getting values for a full table.
        """
        if key is None:
            for entry in self.top_table: # O(N)
                if entry is not None:
                    for value in entry[1].values(): # O(M)
                        yield value
        else:
            top_index = self.hash1(key) # O(len(key))
            for _ in range(self.table_size): # O(N)
                if self.top_table[top_index][0] == key:
                    for value in self.top_table[top_index][1].values(): #O(M)
                        yield value
                top_index = (top_index + 1) % self.table_size

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity Analysis: N is the table size. M is the inner table size
        Worst Case: O(len(key) + M) getting the value of the inner table at the first position of the outer table.
        Best Case: O(N * M) getting values for a full table.
        """
        if key is None:
            res = []
            for table in self.top_table: # O(N)
                if table is not None:
                    res += table[1].values() # O(M)
            return res
        

        top_index = self.hash1(key) # O(len(key))
        for _ in range(self.table_size): # O(N) 
            if self.top_table[top_index][0] == key: 
                return self.top_table[top_index][1].values() # O(M)
            top_index = (top_index + 1) % self.table_size
    

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity Analysis: N is the table size, M is the internal table size, K is hash2(key[1])
        Best Case: O(len(key)) When the K1 is not in the table. 
        Worst Case: O(len(key) + N + K * M) When getting the item we are looking for is at the end of each table.
        """
        top_index, sub_index = self._linear_probe(key[0], key[1], False) # B: O(len(key)) W: O(len(key) + N + K * M)
        return self.top_table[top_index][1][key[1]][1]  # B: O(K) W: O(K + M)

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Complexity Analysis: N is the table size, M is the internal table size, K is hash2(key[1]), T is the new table size(outer table).
        Best Case: O(len(key)) When the K1 is not in the table. 
        Worst Case: O(len(key) + N + K*M + M*K + M^2 + T + N + len(key)*N) -> O(N + K*M + M*K + M^2 + T + len(key)*N) When resizing is needed both in the inner and outer table
        """
        top_index, sub_index = self._linear_probe(key[0], key[1], True) # B: O(len(key)) W: O(len(key) + N + K * M)
        self.top_table[top_index][1].__setitem__(key[1], data) # B: O(K) W: O(M*K + M^2)
        
        if self.count > self.table_size / 2:
            self._rehash() # O(T + N + len(key)*N)

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity Analysis: N is the table size. M is the inner table size. K is hash2(key[1])
        Best Case: O(len(key)) When the K1 is not in the table. 
        Worst Case: O(K*M + N*K + M^2 + N*len(key)) When deleting and probing is needed in both inner and outer tables.
        """
        top_index, sub_index = self._linear_probe(key[0], key[1], False) # B: O(len(key)) W: O(len(key) + N + K * M)

        self.top_table[top_index][1].__delitem__(key[1]) # B: O(K) # W: O(M * K + M^2)

        if self.top_table[top_index][1].is_empty():
            self.top_table[top_index] = None
            self.count -=1
            top_index = (top_index + 1) % self.table_size
            while self.top_table[top_index] is not None: # worst O(N)
                temp_key, temp_table = self.top_table[top_index]
                self.top_table[top_index] = None
                #Reinsert
                newPos = self.hash1(temp_key) # O(len(key))
                self.top_table[newPos] = (temp_key, temp_table)
                top_index = (top_index + 1) % self.table_size
        

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity: Where T is the new table_size and N is the old table_size
        O(T + N + len(key) * N/2) -> O(T + N + len(key)*N) Since _rehash is only called when the old table is more than half full.
        """
        old_array = self.top_table
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # Cannot be resized further.
            return
        
        self.top_table: ArrayR[(K1, LinearProbeTable) | None] = ArrayR(self.TABLE_SIZES[self.size_index]) # O(T)
        
        for table in old_array: # O(N)
            if table is not None:
                new_pos = self.hash1(table[0]) # O(len(key))
                self.top_table[new_pos] = table 
                
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.top_table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        complexity: O(N) where N is the size of the outer table.
        """
        element_count = 0
        for table in self.top_table: # O(N)
            if table is not None:
                element_count += len(table[1])
        return element_count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """