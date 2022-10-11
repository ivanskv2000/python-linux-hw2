import re
from collections import deque
from collections.abc import Iterable
from typing import Union


class CalculatorError(Exception):
    """Base class for Calculator exceptions"""
    pass


class EmptyInputError(CalculatorError):
    """Raised when an empty input is given"""
    def __init__(self):
        self.message = "Empty input provided."
        super().__init__(self.message)


class ParenthesesBalancingError(CalculatorError):
    """Raised when unbalanced parentheses are found in input"""
    def __init__(self, input_string):
        self.input_string = input_string
        self.message = f"Matching parenthesis not found in \'{self.input_string}\'."
        super().__init__(self.message)


class UnknownToken(CalculatorError):
    """Raised when an unknown token is present in math expression"""
    def __init__(self, token):
        self.unknown_token = token
        self.message = f"Couldn't understand token \'{self.unknown_token}\'."
        super().__init__(self.message)


class IncompleteExpression(CalculatorError):
    def __init__(self, operator):
        self.operator = operator
        self.message = f"No operand found for operator \'{self.operator}\'."
        super().__init__(self.message)


class Calculator:
    precedence_levels = {
        "^": 9,
        "*": 8,
        "/": 8,
        "%": 8,
        "+": 6,
        "-": 6,
        "(": -1,
        ")": None,
    }

    operators = list(
        filter(
            lambda x: x not in ["(", ")"],
            precedence_levels.keys()
            )
        )

    funcs = {
        "+": (lambda a, b: a + b),
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b),
        "/": (lambda a, b: a / b),
        "^": (lambda a, b: a ** b),
        "%": (lambda a, b: a % b),
    }

    def __init__(self) -> None:
        self.history = []

    def char_attribution(self, char) -> str:
        """
        Returns the type of a char (in calculator context):
        - `operand`, if char can be a part of variable (number)
        - `operator`, if char represents a binary operation
        - `parenthesis`
        - `other`
        """

        if char.isdigit() or char == ".":
            char_type = "operand"
        elif char in self.operators:
            char_type = "operator"
        elif char in ('(', ')'):
            char_type = "parenthesis"
        else:
            char_type = "other"

        return char_type

    def tokenize(self, string) -> Iterable[str]:
        """
        Yields tokens from a mathematical expression
        """

        token_attribution = self.char_attribution(string[0])
        token = ''
        for char in re.sub(r'\s+', "", string):
            new_type = self.char_attribution(char)

            # Case for unary minus
            if char == '-' and \
                    (token_attribution == 'operator' or token[-1] == '('):
                yield token
                token = ''
                token_attribution = 'operand'

            elif new_type != token_attribution:
                yield token
                token = ''
                token_attribution = new_type

            token += char

        if len(token) > 0:
            yield token

    def is_operand(self, element: str) -> bool:
        """
        Checks if token is an operand
        (i.e. it can be represented as int or float)
        """

        try:
            float(element)
            return True
        except ValueError:
            return False

    def int_or_float(self, number: str) -> Union[int, float]:
        """
        Returns a number in optimal format (int or float)
        """

        try:
            return int(number)
        except ValueError:
            return float(number)

    def convert_to_rpn(self, tokenized_expression: list) -> list:
        """
        Converts a tokenized infix expression to reverse Polish notation (RPN)
        Uses a variation of Dijkstra's "shunting yard" algorithm

        Source: https://web.archive.org/web/20090605032748/http://montcs.bloomu.edu/~bobmon/Information/RPN/infix2rpn.shtml
        """

        output = []
        operator_stack = deque()

        for token in tokenized_expression:
            if self.is_operand(token):
                output.append(token)

            elif token in self.operators:
                while True:
                    if len(operator_stack) == 0:
                        break
                    if self.precedence_levels[token] > self.precedence_levels[operator_stack[-1]]:
                        break

                    popped = operator_stack.pop()
                    output.append(popped)

                operator_stack.append(token)

            elif token == '(':
                operator_stack.append(token)

            elif token == ')':
                while True:
                    if len(operator_stack) == 0:
                        raise ParenthesesBalancingError(''.join(tokenized_expression))
                    if operator_stack[-1] == '(':
                        _ = operator_stack.pop()
                        break

                    popped = operator_stack.pop()
                    output.append(popped)

            else:
                raise UnknownToken(token)

        while len(operator_stack) > 0:
            stack_popped = operator_stack.pop()
            if stack_popped == '(':
                raise ParenthesesBalancingError(''.join(tokenized_expression))

            output.append(stack_popped)

        return output

    def eval_rpn(self, rpn_expression: list) -> float:
        """
        Evaluates an RPN expression via stack algorithm

        Source: https://ru.wikipedia.org/wiki/Обратная_польская_запись#Вычисления_на_стеке
        """

        parsing_stack = deque()

        for token in rpn_expression:
            if self.is_operand(token):
                parsing_stack.append(self.int_or_float(token))
            else:
                try:
                    arg2 = parsing_stack.pop()
                    arg1 = parsing_stack.pop()
                    result = self.funcs[token](arg1, arg2)
                    parsing_stack.append(result)
                except IndexError:
                    raise IncompleteExpression(token) from None

        eval_result = parsing_stack.pop()
        return eval_result

    def calculate(self, input_string: str) -> Union[int, float]:
        """
        Combines all methods necessary to go from input string to the answer
        """

        if input_string == '':
            raise EmptyInputError
        tokenized = [i for i in self.tokenize(input_string) if i != '']
        rpn = self.convert_to_rpn(tokenized)
        result = self.eval_rpn(rpn)

        return result
