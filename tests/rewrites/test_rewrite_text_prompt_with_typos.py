"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.rewrites.rewrite_text_prompt_with_typos import (
    RewriteTextPromptWithMisspellings,
    RewriteTextPromptWithTypos,
)

from brittlebench.perturbations.typo_perturbation import TypoCountPerturbation


class TestRewriteTextPromptWithTypos:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_with_default_key(self):
        sample = {
            "text": "Write a function to find the similar elements from the given two tuple lists.",
        }

        rewrite = RewriteTextPromptWithTypos()

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"]
            == "Wriet a function to fidn the similiar elem&ents frome the given two tupe liats."
        )

    def test_with_other_key(self):
        sample = {
            "question": "When was the first moon landing?",
        }

        rewrite = RewriteTextPromptWithTypos(key="question")

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["question"] == "Whn was the firts moon labding?"

    def test_with_misspelling_typos(self):
        sample = {
            "text": "Write a function to find the similar elements from the given two tuple lists.",
        }

        rewrite = RewriteTextPromptWithTypos(typo_type="misspelling")

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"]
            == "Wriet a function to fidn the similiar elements fomr the given two tuple lists."
        )

    def test_with_charmix_typos(self):
        sample = {
            "text": "When was the first moon landing?",
        }

        rewrite = RewriteTextPromptWithTypos(typo_type="charmix")

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == "Whne was the jfirst moon lmanding?"

    def test_with_keyboard_typos(self):
        sample = {
            "text": "When was the first moon landing?",
        }

        rewrite = RewriteTextPromptWithTypos(typo_type="keyboard")

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == "Whwn was the fi3st moon lahding?"

    def test_is_task_compatible(self):
        rewrite = RewriteTextPromptWithTypos()

        assert rewrite.is_task_compatible('some-task')
        assert not rewrite.is_task_compatible('mbpp')
        assert not rewrite.is_task_compatible('humaneval')

    def test_with_count_typos(self):
        rewrite = RewriteTextPromptWithTypos(typos_count=3)
        assert isinstance(rewrite.perturbation, TypoCountPerturbation)


class TestRewriteTextPromptWithMisspellings:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_with_default_key(self):
        sample = {
            "text": "Write a function to find the similar elements from the given two tuple lists.",
        }

        rewrite = RewriteTextPromptWithMisspellings()

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"]
            == "Wriet a function to fidn the similiar elements fomr the given two tuple lists."
        )

    def test_with_other_key(self):
        sample = {
            "question": "When was the first moon landing?",
        }

        rewrite = RewriteTextPromptWithMisspellings(key="question")

        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["question"] == "Whn was the firts moon landing?"

    def test_is_task_compatible(self):
        rewrite = RewriteTextPromptWithMisspellings()

        assert not rewrite.is_task_compatible('some-task')
        assert rewrite.is_task_compatible('mbpp')
