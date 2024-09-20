import unittest
from repair_calculator import RepairCalculator

class TestRepairCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = RepairCalculator()

    def test_calculate_repair_cost(self):
        self.assertEqual(self.calculator.calculate_repair_cost(500, 300, 50), 850)

    def test_calculate_repair_time(self):
        self.assertEqual(self.calculator.calculate_repair_time(2, 30), (2, 30))

    def test_calculate_discounted_cost(self):
        self.assertEqual(self.calculator.calculate_discounted_cost(1000, 20), 800)

    def test_calculate_repair_cost_zero(self):
        self.assertEqual(self.calculator.calculate_repair_cost(0, 0, 0), 0)

    def test_calculate_repair_time_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_repair_time(-1, 30)

if __name__ == '__main__':
    unittest.main()
