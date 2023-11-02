# Test Calculator
from django.test import SimpleTestCase
from . import calc

class CalulatorTest(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.add(5,6)
        self.assertEqual(res, 11)


    def test_subtract(self):
        res = calc.subtract(45,20)
        self.assertEqual(res, 25)