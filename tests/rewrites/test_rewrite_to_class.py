"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_to_class import RewriteToClass

class TestRewriteToClass:
    def test_apply(self):
        rewrite = RewriteToClass()
        input_code = (
            "def my_function(x):\n"
            "    return x * 2\n"
        )
        expected_output = (
            "class MyClass:\n"
            "    def my_function(x):\n"
            "        return x * 2\n"
        )
        result = rewrite.perturbation.apply(input_code)
        assert result == expected_output

    def test_apply_empty_function(self):
        rewrite = RewriteToClass()
        input_code = ""
        expected_output = (
            "class MyClass:\n"
            "    pass\n"
        )
        result = rewrite.perturbation.apply(input_code)
        assert result == expected_output

    def test_with_other_key(self):
        rewrite = RewriteToClass(key="code_snippet")
        sample = {
            "code_snippet": (
                "def add(a, b):\n"
                "    return a + b\n"
            )
        }
        expected_output = (
            "class MyClass:\n"
            "    def add(a, b):\n"
            "        return a + b\n"
        )
        result_sample = rewrite.apply(sample)
        assert result_sample["code_snippet"] == expected_output
