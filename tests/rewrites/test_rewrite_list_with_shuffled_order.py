"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from datasets import Dataset

from brittlebench.rewrites.rewrite_list_with_shuffled_order import (
    RewriteListWithShuffledOrder,
)


class TestRewriteListWithShuffledOrder:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_with_string(self):
        sample = {
            "choices": [
                "Oak",
                "Maple",
                "Pine",
                "Birch",
            ],
            "answer": "Oak",
        }

        rewrite = RewriteListWithShuffledOrder(choices="choices", answer="answer")
        rewritten_sample = rewrite.apply(sample)
        assert rewritten_sample["choices"] == ["Birch", "Maple", "Oak", "Pine"]
        assert rewritten_sample["answer"] == "Oak"

    def test_with_index(self):
        sample = {
            "choices": [
                "Oak",
                "Maple",
                "Pine",
                "Birch",
            ],
            "answer": 0,
        }

        rewrite = RewriteListWithShuffledOrder(choices="choices", answer="answer")
        rewritten_sample = rewrite.apply(sample)
        assert rewritten_sample["choices"] == ["Birch", "Maple", "Oak", "Pine"]
        assert rewritten_sample["answer"] == 2

    def test_with_letter(self):
        sample = {
            "choices": [
                "Oak",
                "Maple",
                "Pine",
                "Birch",
            ],
            "answer": "A",
        }

        rewrite = RewriteListWithShuffledOrder(choices="choices", answer="answer")
        rewritten_sample = rewrite.apply(sample)
        assert rewritten_sample["choices"] == ["Birch", "Maple", "Oak", "Pine"]
        assert rewritten_sample["answer"] == "C"


    def test_with_non_default_key(self):
        sample = {
            "options": [
                "Oak",
                "Maple",
                "Pine",
                "Birch",
            ],
            "answer": "Oak",
        }

        rewrite = RewriteListWithShuffledOrder(choices="options", answer="answer")
        rewritten_sample = rewrite.apply(sample)
        assert rewritten_sample["options"] == ["Birch", "Maple", "Oak", "Pine"]
        assert rewritten_sample["answer"] == "Oak"
