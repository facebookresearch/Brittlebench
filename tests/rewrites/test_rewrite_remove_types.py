"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_remove_types import RewriteRemoveTypes

class TestRewriteRemoveTypes:
    def test_apply_removes_types(self):
        rewrite = RewriteRemoveTypes()
        sample = {
            "text": "def add(a: int, b: int) -> int:\n    return a + b"
        }
        rewritten_sample = rewrite.apply(sample)
        expected_code = "def add(a, b):\n    return a + b"
        assert rewritten_sample["text"] == expected_code

    def test_exclusive_tasks(self):
        rewrite = RewriteRemoveTypes()
        assert "humaneval" in rewrite.exclusive_tasks 
    
    def test_with_different_key(self):
        rewrite = RewriteRemoveTypes()
        sample = {
            "different_key": "def multiply(x: float, y: float) -> float:\n    return x * y"
        }
        rewrite.key = "different_key"
        rewritten_sample = rewrite.apply(sample)
        expected_code = "def multiply(x, y):\n    return x * y"
        assert rewritten_sample["different_key"] == expected_code 
