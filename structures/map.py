"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self, my_cap=None) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self.size = 0
        if my_cap:
            self.capacity = my_cap
        else:
            self.capacity = 101
        self.map = [DoublyLinkedList() for _ in range(self.capacity)]
        self.primes = [
            211,
            419,
            853,
            1709,
            3433,
            6863,
            13729,
            27409,
            54833,
            109673,
            219143,
            438283,
            876563,
            1753127,
            3506257,
            7012519,
            14025089,
            28050163,
            56100313,
            112200689,
            224401369,
            448802727,
            897605461,
            1795210933,
        ]
        self.prime_index = -1

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        # ratio - loading factor
        if self.size / self.capacity >= 0.7:
            self._rehash()

        hashed_key = entry.get_hash()
        index = hashed_key % self.capacity

        # grouping / chaining
        chain = self.map[index]
        occurence = chain.find_and_return_key(entry)

        if occurence:
            old_value = occurence.get_value()
            occurence.update_value(entry.get_value())
            return old_value

        chain.insert_to_back(entry)
        self.size += 1
        return None

    def _rehash(self):
        old_map = self.map
        self.prime_index += 1
        self.capacity = self.primes[self.prime_index]
        self.map = [DoublyLinkedList() for _ in range(self.capacity)]
        self.size = 0

        for chain in old_map:
            for i in range(chain.get_size()):
                node = chain.remove_from_front()
                self.insert(node)

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        # hint: entry = Entry(key, value)
        entry = Entry(key, value)
        return self.insert(entry)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, value)
        self.insert(entry)

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, None)
        hashed_key = entry.get_hash()
        index = hashed_key % self.capacity

        chain = self.map[index]
        if chain.find_and_remove_element(entry):
            self.size -= 1

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, None)
        hashed_key = entry.get_hash()
        index = hashed_key % self.capacity

        chain = self.map[index]
        found = chain.find_and_return_element(entry)
        if found:
            return found.get_value()
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return True
        return False

    def __str__(self) -> str:
        """
        Time complexity for full marks: O(n)
        """
        string = ""
        for chain in self.map:
            chain_str = chain.map_str()
            if chain_str != "":
                string += chain_str + "\n"
        return string
