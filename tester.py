#!/usr/bin/env python3

import unittest

import lazylist

class TestGetItem(unittest.TestCase):
    def setUp(self):
        pass
        #self.lazy = lazylist.List(range(20, 30))
    
    def test_incremental(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i]
            self.assertEqual(len(lazy._list), i + 1)
        self.assertEqual(len(lazy), range_size)
        for a, b in zip(lazy._list, range(range_size)):
            self.assertEqual(a, b)
            

    def test_all_at_once(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        lazy[range_size - 1]
        self.assertEqual(len(lazy._list), range_size)


if __name__ == '__main__':
    unittest.main()
