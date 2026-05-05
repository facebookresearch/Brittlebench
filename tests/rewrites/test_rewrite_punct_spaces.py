"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_punct_spaces import RewritePunctSpaces


class TestRewritePunctSpaces:

    def test_default_apply(self):
        sample = {
            "text": "This is a question."
        }
        rewrite = RewritePunctSpaces()

        result = rewrite.apply(sample)
        assert result == {
            "text": "This is a question ."
        }

    def test_with_other_key(self):
        sample = {
            "other_text": "This is a question."
        }
        rewrite = RewritePunctSpaces(key="other_text")

        result = rewrite.apply(sample)
        assert result == {
            "other_text": "This is a question ."
        }

    def test_is_task_compatible(self):
        rewrite = RewritePunctSpaces()

        assert rewrite.is_task_compatible('some-task')
        assert rewrite.is_task_compatible('mbpp')
        assert rewrite.is_task_compatible('mmlu')
        assert rewrite.is_task_compatible('humaneval')
