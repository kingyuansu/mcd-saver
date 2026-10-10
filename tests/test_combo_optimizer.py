
import unittest
from decimal import Decimal

from scripts.combo_optimizer import find_combinations


class TestComboOptimizer(unittest.TestCase):

    def setUp(self):
        self.items = [
            {"name": "巨无霸", "price": "25.5"},
            {"name": "麦辣鸡腿汉堡", "price": "20.0"},
            {"name": "薯条", "price": "12.0"},
            {"name": "可乐", "price": "9.0"},
        ]

    def test_all_combinations_within_budget(self):
        """所有结果都不能超过预算。"""
        budget = Decimal("40.0")
        results = find_combinations(self.items, budget)

        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertLessEqual(result["total"], budget)

    def test_total_and_remaining_are_correct(self):
        """核验组合总价和剩余预算。"""
        results = find_combinations(self.items, "40.0")

        for result in results:
            expected_total = sum(
                Decimal(item["price"])
                for item in self.items
                if item["name"] in result["items"]
            )
            self.assertEqual(result["total"], expected_total)
            self.assertEqual(
                result["remaining"],
                Decimal("40.0") - expected_total,
            )

    def test_results_sorted_by_total_descending(self):
        """组合应按总价从高到低排列。"""
        results = find_combinations(self.items, "40.0")
        totals = [result["total"] for result in results]

        self.assertEqual(totals, sorted(totals, reverse=True))

    def test_invalid_budget_is_rejected(self):
        """负数预算应被拒绝。"""
        with self.assertRaises(ValueError):
            find_combinations(self.items, "-1")

    def test_negative_item_price_is_rejected(self):
        """负数餐品价格应被拒绝。"""
        invalid_items = [
            {"name": "测试餐品", "price": "-5"}
        ]

        with self.assertRaises(ValueError):
            find_combinations(invalid_items, "20")

    def test_result_limit_is_respected(self):
        """返回结果数量不能超过 limit。"""
        results = find_combinations(
            self.items,
            "100",
            max_items=3,
            limit=2,
        )

        self.assertLessEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
