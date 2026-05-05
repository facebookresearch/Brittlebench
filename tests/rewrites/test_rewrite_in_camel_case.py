"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.rewrites.rewrite_in_camel_case import (
    RewriteInCamelCase,
)
from tests.prompt_examples import (
    HUMAN_EVAL_PROMPT_1,
    HUMAN_EVAL_PROMPT_2,
    HUMAN_EVAL_PROMPT_3,
    HUMAN_EVAL_PROMPT_4,
)

_HUMAN_EVAL_PROMPT_1_REWRITTEN = """
def stringToMd5(text):
    \"""
    Given a string 'text', return its md5 hash equivalent string.
    If 'text' is an empty string, return None.

    >>> stringToMd5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    \"""
"""


_HUMAN_EVAL_PROMPT_2_REWRITTEN = """
def generateIntegers(a, b):
    \"""
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generateIntegers(2, 8) => [2, 4, 6, 8]
    generateIntegers(8, 2) => [2, 4, 6, 8]
    generateIntegers(10, 14) => []
    \"""
"""


_HUMAN_EVAL_PROMPT_4_REWRITTEN = """
def doAlgebra(operator, operand):
    \"""
    Given two lists operator, and operand. The first list has basic algebra operations, and
    the second list is a list of integers. Use the two given lists to build the algebric
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + )
    Subtraction ( - )
    Multiplication ( * )
    Floor division ( // )
    Exponentiation ( ** )

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    \"""
"""


class TestRewriteInCamelCase:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_with_prompt_1(self):
        sample = {"text": HUMAN_EVAL_PROMPT_1}

        rewrite = RewriteInCamelCase()

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == _HUMAN_EVAL_PROMPT_1_REWRITTEN

    def test_with_prompt_2(self):
        sample = {"text": HUMAN_EVAL_PROMPT_2}

        rewrite = RewriteInCamelCase()

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == _HUMAN_EVAL_PROMPT_2_REWRITTEN

    def test_with_prompt_3(self):
        sample = {"text": HUMAN_EVAL_PROMPT_3}

        rewrite = RewriteInCamelCase()

        rewritten_sample = rewrite.apply(sample)

        # Prompt 3, with function name "solve", should be unchanged
        assert rewritten_sample["text"] == HUMAN_EVAL_PROMPT_3

    def test_with_prompt_4(self):
        sample = {"text": HUMAN_EVAL_PROMPT_4}

        rewrite = RewriteInCamelCase()

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == _HUMAN_EVAL_PROMPT_4_REWRITTEN

    def test_with_other_key(self):
        sample = {"code": HUMAN_EVAL_PROMPT_1}

        rewrite = RewriteInCamelCase(key="code")

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["code"] == _HUMAN_EVAL_PROMPT_1_REWRITTEN
