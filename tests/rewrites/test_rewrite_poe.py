"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_poe import (
    CompositeRewritePoE,
    RewriteAddPoEInstructions,
    RewritePoEDropOptions,
    CompositeRewriteNoPoE,
)

from brittlebench.rewrites.rewrite import Rewrite


class TestRewritePoE:
    def test_rewrite_poe_drop_options(self):
        sample = {
            "choices": ["A", "B", "C", "D"],
            "answer": "A"
        }

        rewrite = RewritePoEDropOptions(choices="choices", answer="answer", target_option_count=2, is_poe=True)

        rewritten_sample = rewrite.apply(sample)

        assert len(rewritten_sample["choices"]) == 2
        assert rewritten_sample["answer"] != "A"

    def test_rewrite_add_poe_instructions(self):
        sample = {
            "text": "What is the capital of France?"
        }

        expected_instruction = "Your goal is to identify the incorrect answer to the multiple choice question.\nWhat is the capital of France?\nIncorrect Answer:"

        rewrite = RewriteAddPoEInstructions(is_poe=True, key="text")

        rewritten_sample = rewrite.apply(sample)

        assert expected_instruction == rewritten_sample["text"]

    def test_composite_rewrite_poe(self):
        sample = {
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "text": "What is the capital of France?"
        }

        expected_instruction = "Your goal is to identify the incorrect answer to the multiple choice question.\nWhat is the capital of France?\nIncorrect Answer:"

        composite_rewrite = CompositeRewritePoE(target_option_count=2, choices="options", answer="answer")

        for rewrite in composite_rewrite.rewrites:
            assert isinstance(rewrite, Rewrite)
            if rewrite.name == "rewrite_poe_drop_options":
                sample = rewrite.apply(sample)
                assert len(sample["options"]) == 2
                assert sample["answer"] != "A"

            elif rewrite.name == "rewrite_add_poe_instructions":
                sample = rewrite.apply(sample)
                assert sample["text"] == expected_instruction

    def test_composite_rewrite_no_poe(self):
        sample = {
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "text": "What is the capital of France?"
        }

        expected_instruction = "Your goal is to identify the correct answer to the multiple choice question.\nWhat is the capital of France?\nCorrect Answer:"

        composite_rewrite = CompositeRewriteNoPoE(target_option_count=2, choices="options", answer="answer")

        for rewrite in composite_rewrite.rewrites:
            assert isinstance(rewrite, Rewrite)
            if rewrite.name == "rewrite_poe_drop_options":
                sample = rewrite.apply(sample)
                assert len(sample["options"]) == 2
                assert sample["answer"] == "A"

            elif rewrite.name == "rewrite_add_poe_instructions":
                sample = rewrite.apply(sample)
                assert sample["text"] == expected_instruction
