import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puzzles.coin_change import coin_change_solve, COINS


class TestCoinChangeCount(unittest.TestCase):

    def test_basic_result(self):
        dp = coin_change_solve([1, 2, 3], 4)
        self.assertEqual(dp[3][4], 4)

    def test_sum_zero_always_one_way(self):
        dp = coin_change_solve([1, 2, 3], 5)
        for r in range(len([1, 2, 3]) + 1):
            self.assertEqual(dp[r][0], 1)

    def test_no_coins_zero_ways(self):
        dp = coin_change_solve([1, 2, 3], 5)
        for c in range(1, 6):
            self.assertEqual(dp[0][c], 0)

    def test_single_coin(self):
        # 1 coin -> one way
        dp = coin_change_solve([1], 5)
        for c in range(1, 6):
            self.assertEqual(dp[1][c], 1)

    def test_sum_10(self):
        # tests a target sum of 10
        dp = coin_change_solve([1, 2, 3], 10)
        self.assertEqual(dp[3][10], 14)

    def test_table_dimensions(self):
        coins  = [1, 2, 3]
        target = 7
        dp = coin_change_solve(coins, target)
        self.assertEqual(len(dp), len(coins) + 1)
        self.assertEqual(len(dp[0]), target + 1)

    def test_result_increases_with_sum(self):
        dp_small = coin_change_solve([1, 2, 3], 4)
        dp_large = coin_change_solve([1, 2, 3], 8)
        self.assertGreater(dp_large[3][8], dp_small[3][4])


if __name__ == "__main__":
    unittest.main(verbosity=2)