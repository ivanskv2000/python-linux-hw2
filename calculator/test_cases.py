import pytest
import numpy as np 
from . import Calculator
from . import EmptyInputError, ParenthesesBalancingError, UnknownToken, IncompleteExpression


def calculate(input_string):
    return Calculator().calculate(input_string)


def eval_proof(input_string):
    via_calc = calculate(input_string)
    via_eval = eval(input_string.replace('^', '**'))
    return np.isclose(via_calc, via_eval)


def check_exception(input_string, err):
    with pytest.raises(err):
        _ = calculate(input_string)


class TestBasicFunctionality:
    def test_add(self):
        expr = '1 + 2'
        assert eval_proof(expr)

    def test_substract(self):
        expr = '38 - 16'
        assert eval_proof(expr)

    def test_divide(self):
        expr = '34 / 2 '
        assert eval_proof(expr)

    def test_exponent(self):
        expr = '2^10'
        assert eval_proof(expr)


class TestFloats:
    def test_two_floats(self):
        expr = '1.9 + 2.9'
        assert eval_proof(expr)
        assert isinstance(calculate(expr), float)

    def test_floats_and_ints(self):
        expr = '28 - 1.2'
        assert eval_proof(expr)
        assert isinstance(calculate(expr), float)


class TestUnaryMinus:
    def test_single_unary(self):
        expr = '-1'
        assert eval_proof(expr)

    def test_parentheses(self):
        expr = '12 + (-2 + 19) / 2'
        assert eval_proof(expr)

    def test_substract(self):
        expr = '-2 - 12 '
        assert eval_proof(expr)

    def test_floats(self):
        expr = '-2.0 + 12 '
        assert eval_proof(expr)

    def test_duplicate_signs(self):
        expr1 = '2 + -3'
        expr2 = '2 - -3'
        assert eval_proof(expr1)
        assert eval_proof(expr2)


class TestErrorHandling:
    def test_empty_input(self):
        check_exception('', EmptyInputError)

    def test_parentheses_balancing(self):
        check_exception('99 + (13', ParenthesesBalancingError)
        check_exception('99 - 13)', ParenthesesBalancingError)

    def test_unknown_tokens(self):
        check_exception('1 + 2 + 3 + &', UnknownToken)
        check_exception('458 / 474 + (1-2-3) ^ #', UnknownToken)

    def test_incomplete_expressions(self):
        check_exception('5 -', IncompleteExpression)
        check_exception('+2', IncompleteExpression)
