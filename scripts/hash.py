# PART D.
# Identify a self-adjusting data structure, such as a hash table,
# that can be used with the algorithm identified in part A to store the package data.
#
# 1. I use the key as the package ID and the value as the package object itself to easily
# identify which package is which in the search part of the hash table

# TIME COMPLEXITY: O(1)
# SPACE COMPLEXITY: O(n)
class HashTable:
    def __init__(self, init_capacity=10):
        self.table = []
        for i in range(init_capacity):
            self.table.append([])

    # PART E.
    # Develop a hash table, without using any additional libraries or classes,
    # that has an insertion function that takes the following components as input
    # and inserts the components into the hash table.

    # insert function for package object
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for obj in bucket_list:
            if obj[0] == key:
                obj[1] = item
                return True

        key_list = [key, item]
        bucket_list.append(key_list)

        return True

    # PART F.
    # Develop a look-up function that takes the following components as input
    # and returns the corresponding data elements:

    # search function for package object
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for key_list in bucket_list:
            if key_list[0] == key:
                return key_list[1]

        return None

    # remove function for package object
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for key_list in bucket_list:
            if key_list[0] == key:
                bucket_list.remove([key_list[0], key_list[1]])