
import pytest
from app.calculator import add, subtract, multiply, divide


# add()


class TestAdd:
    def test_add_two_positive_numbers(self):
        assert add(3, 5) == 8

    def test_add_positive_and_negative(self):
        assert add(10, -4) == 6

    def test_add_two_negatives(self):
        assert add(-2, -3) == -5

    def test_add_zeros(self):
        assert add(0, 0) == 0

    def test_add_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)


# subtract()


class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(10, 4) == 6

    def test_subtract_resulting_negative(self):
        assert subtract(3, 7) == -4

    def test_subtract_zero(self):
        assert subtract(5, 0) == 5

    def test_subtract_same_numbers(self):
        assert subtract(9, 9) == 0



# multiply()

class TestMultiply:
    def test_multiply_positive_numbers(self):
        assert multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0

    def test_multiply_negatives(self):
        assert multiply(-3, -4) == 12

    def test_multiply_positive_and_negative(self):
        assert multiply(6, -7) == -42

    def test_multiply_floats(self):
        assert multiply(2.5, 4) == pytest.approx(10.0)


# divide()

class TestDivide:
    def test_divide_basic(self):
        assert divide(10, 2) == 5.0

    def test_divide_resulting_float(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_negative_dividend(self):
        assert divide(-9, 3) == -3.0

    def test_divide_by_one(self):
        assert divide(42, 1) == 42.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)
