"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from datasets import Dataset

from brittlebench.rewrites.rewrite_emotion_prompts import RewriteEmotionPromptsBase


class TestRewriteEmotionPrompt:
    def test_with_default_stimuli(self):
        sample = {
            "text": "This is a question."
        }

        rewrite = RewriteEmotionPromptsBase()

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"] == "This is a question.\nGive me a confidence score between 0-1 for your answer and then write your answer."
        )

    def test_with_prefix(self):
        sample = {
            "text": "This is a question."
        }

        rewrite = RewriteEmotionPromptsBase(stimuli_code="EP15")

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"] == "You're safe.\nThis is a question."
        )
    
    def test_with_suffix(self):
        sample = {
            "text": "This is a question."
        }

        rewrite = RewriteEmotionPromptsBase(stimuli_code="EP03")

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"] == "This is a question.\nYou'd better be sure."
        )

    def test_is_task_compatible(self):
        rewrite = RewriteEmotionPromptsBase()

        assert rewrite.is_task_compatible('some-task')
        assert rewrite.is_task_compatible('mbpp')
        assert rewrite.is_task_compatible('mmlu')
        assert rewrite.is_task_compatible('humaneval')

    def test_with_other_key(self):
        sample = {
            "other_text": "This is a question."
        }

        rewrite = RewriteEmotionPromptsBase(key="other_text")

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["other_text"]
            == "This is a question.\nGive me a confidence score between 0-1 for your answer and then write your answer."
        )
