"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.bit_vector import BitVector
from structures.entry import Entry
from structures.util import object_to_byte_array
import math


class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then /you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    # NOt passing exhaustive tests
    # maybe due to when max key is lower value

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._data = BitVector()
        self.capacity = self.get_size(max_keys)
        self.hash_count = self.get_hash_count(self.capacity, max_keys)
        # print("Hash count: ", self.hash_count)
        # print("Capacity: ", self.capacity)
        # print("Ratio: ", self.capacity / max_keys)
        self._data.allocate(self.capacity)
        self.golden_ratio = (math.sqrt(5) - 1) / 2
        # More variables here if you need, of course

    def get_size(self, max_keys: int) -> int:
        m = -(max_keys * math.log(0.01)) / (math.log(2) ** 2)
        return self.get_prime(int(m))

    def get_prime(self, m: int) -> int:
        my_primes = [
            1009,
            2003,
            3001,
            4001,
            5003,
            6007,
            7001,
            8009,
            9001,
            10007,
            20011,
            30011,
            40009,
            50021,
            60013,
            70001,
            80021,
            90001,
            100003,
            200003,
            300007,
            400009,
            500009,
            600011,
            700001,
            800011,
            900001,
            1000003,
            1100009,
            1200011,
            1300021,
            1400003,
            1500011,
            1600013,
            1700021,
            1800017,
            1900009,
            2000003,
            2100013,
            2200007,
            2300017,
            2400011,
            2500009,
            2600017,
            2700013,
            2800001,
            2900021,
            3000017,
            3100003,
            3200009,
            3300017,
            3400013,
            3500009,
            3600017,
            3700007,
            3800023,
            3900017,
            4000003,
            4100017,
            4200013,
            4300009,
            4400021,
            4500013,
            4600009,
            4700023,
            4800019,
            4900013,
            5000011,
            5100007,
            5200019,
            5300011,
            5400007,
            5500009,
            5600017,
            5700013,
            5800021,
            5900011,
            6000001,
            6100001,
            6200017,
            6300013,
            6400011,
            6500021,
            6600007,
            6700013,
            6800011,
            6900019,
            7000003,
            7100019,
            7200023,
            7300013,
            7400021,
            7500007,
            7600007,
            7700021,
            7800019,
            7900017,
            8000009,
            8100023,
            8200011,
            8300003,
            8400017,
            8500013,
            8600023,
            8700019,
            8800013,
            8900009,
            9000011,
            9100013,
            9200021,
            9300017,
            9400003,
            9500009,
            9600007,
            9700013,
            9800011,
            9900019,
            10000019,
            10100001,
            10200007,
            10300013,
            10400001,
            10500001,
            10600007,
            10700009,
            10800007,
            10900013,
            11000003,
            11100001,
            11200013,
            11300001,
            11400019,
            11500001,
            11600009,
            11700007,
            11800001,
            11900003,
            12000001,
            12100007,
            12200009,
            12300001,
            12400003,
            12500001,
            12600001,
            12700009,
            12800003,
            12900001,
            13000001,
            13100001,
            13200001,
            13300001,
            13400001,
            13500001,
            13600001,
            13700001,
            13800001,
            13900001,
            14000001,
            14100001,
            14200001,
            14300001,
            14400001,
            14500001,
            14600001,
            14700001,
            14800001,
            14900001,
            15000001,
            15100001,
            15200001,
            15300001,
            15400001,
        ]
        for prime in my_primes:
            if prime > m:
                return prime

        return self.calc_prime(m)

    def calc_prime(self, m: int) -> int:
        while True:
            m += 1
            if self.is_prime(m):
                return m

    def is_prime(self, n: int) -> bool:
        if n <= 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def get_hash_count(self, capacity: int, max_keys: int) -> int:
        n = (capacity / max_keys) * math.log(2)
        return int(n)

    def my_hash(self, key: Any) -> int:
        a = 70125
        b = 853
        p = 14025089
        # c = 35062
        # d = 419
        # q = 28050163
        # mask = (1 << 32) - 1
        # h = 0
        # k = 1
        # key_bytes = key
        # for byte in key_bytes:
        #     h = ((h << 5) & mask) | (h >> 27)
        #     h += (byte)
        #     k = ((k << 5) & mask) | (k >> 27)
        #     k +=(byte)
        # return (a * h + b) % p, (c * k + d) % q
        key_value = int.from_bytes(key, byteorder="big")
        hash1 = (a * key_value + b) % p
        hash2 = ((a ^ key_value) >> 3 + b) % p  # Shift right by 3 bits and apply XOR
        hash3 = (hash1 ^ (key_value << 5)) % p
        return hash1, hash2, hash3

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        pass

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity for full marks: O(1)
        """
        key_bytes = object_to_byte_array(key)
        hash1, hash2, hash3 = self.my_hash(key_bytes)

        # for i in range(self.hash_count):
        #     index = (hash1 + i * hash2) % self.capacity
        #     self._data.set_at(index)
        for i in range(0, self.hash_count, 3):
            index1 = int(
                self.capacity
                * ((((i + hash1) * hash2) * self.golden_ratio) % 1)
            )
            self._data.set_at(index1)

            if i + 1 < self.hash_count:
                index2 = int(
                    self.capacity
                    * ((((i + 1) * hash2) * self.golden_ratio) % 1)
                )
                self._data.set_at(index2)

            if i + 2 < self.hash_count:
                index3 = int(
                    self.capacity
                    * ((((i + 2) * hash3) * self.golden_ratio) % 1)
                )
                self._data.set_at(index3)

            # index1 = ((i + hash1) * hash2) % self.capacity
            # index2 = (i * hash2) % self.capacity

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        key_bytes = object_to_byte_array(key)
        hash1, hash2, hash3 = self.my_hash(key_bytes)

        # for i in range(self.hash_count):
        #     index = (hash1 + i * hash2) % self.capacity
        #     if not self._data.get_at(index):
        #         return False
        # return True

        for i in range(0, self.hash_count, 3):
            index1 = int(
                self.capacity
                * ((((i + hash1) * hash2) * self.golden_ratio) % 1)
            )
            if not self._data.get_at(index1):
                return False

            if i + 1 < self.hash_count:
                index2 = int(
                    self.capacity
                    * ((((i + 1) * hash2) * self.golden_ratio) % 1)
                )
                if not self._data.get_at(index2):
                    return False

            if i + 2 < self.hash_count:
                index3 = int(
                    self.capacity
                    * ((((i + 2) * hash3) * self.golden_ratio) % 1)
                )
                if not self._data.get_at(index3):
                    return False

        return True

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return not self._data.to_byte_arr() == 0

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self.capacity
