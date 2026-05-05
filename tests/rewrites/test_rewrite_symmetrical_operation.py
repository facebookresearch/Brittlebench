"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_symmetrical_operation import RewriteSymmetricalOperationBase, RewriteSymmetricalAddition, RewriteSymmetricalMultiplication


class TestRewriteSymmetricalOperation:
    def test_addition(self):
        sample = {
            "text": "Calculate 2 + 2 and (3 * 4)."
        }
        rewrite = RewriteSymmetricalAddition()

        result = rewrite.apply(sample)
        assert result["text"] == "Calculate (1-1)+2 + 2 and (1-1)+(3 * 4)."

    def test_multiplication(self):
        sample = {
            "text": "Calculate 5 * 6 and (7 + 8)."
        }
        rewrite = RewriteSymmetricalMultiplication()

        result = rewrite.apply(sample)
        assert result["text"] == "Calculate 1*5 * 6 and 1*(7 + 8)."

    def test_with_invalid_operation_type(self):
        try:
            RewriteSymmetricalOperationBase(operation_type="invalid_type")
        except ValueError as e:
            assert str(e) == "Unsupported operation type: invalid_type"
        else:
            assert False, "ValueError was not raised for invalid operation_type"

    def test_with_supported_benchmarks(self):
        benchmarks = [
            "mathqa",
            "gsm8k",
            "gpqa",
            "aime25"
        ]
        rewrite_addition = RewriteSymmetricalAddition()
        rewrite_multiplication = RewriteSymmetricalMultiplication()

        for benchmark in benchmarks:
            assert benchmark in rewrite_addition.exclusive_tasks
            assert benchmark in rewrite_multiplication.exclusive_tasks
