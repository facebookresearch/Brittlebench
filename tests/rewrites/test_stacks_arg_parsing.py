"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import unittest
from unittest.mock import patch
import fire
import sys

from brittlebench.rewrites.rewrite_stack import parse_stacks_arg

class TestParseRewriteUserArg:

    def test_simple_str(self):
        input_str = "baseline"
        expected = [["baseline"]]
        result = parse_stacks_arg(input_str)
        assert isinstance(result, list)
        assert result == expected

    def test_tuple(self):
        input_str = ("type", "persona_knowledge")
        expected = [["type", "persona_knowledge"]]
        result = parse_stacks_arg(input_str)
        assert isinstance(result, list)
        assert result == expected

    def test_semicolon(self):
        input_str = "type;persona_knowledge"
        expected = [["type"], ["persona_knowledge"]]
        result = parse_stacks_arg(input_str)
        assert isinstance(result, list)
        assert result == expected

    def test_nested(self):
        input_str = "type,persona_math;persona_knowledge"
        expected = [["type", "persona_math"], ["persona_knowledge"]]
        result = parse_stacks_arg(input_str)
        assert isinstance(result, list)
        assert result == expected

    def test_empty(self):
        input_str = ""
        expected = [["all"]]
        result = parse_stacks_arg(input_str)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result == expected
