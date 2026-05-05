"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_add_space_seq import RewriteAddSpaceSeq

class TestRewriteAddSpaceSeq:
    
    def test_default_apply(self):
        sample = {
            "text": "This is a test."
        }
        rewrite = RewriteAddSpaceSeq(prob=1.0, min_spaces=1, max_spaces=1)  # Set prob to 1.0 to ensure spaces are added

        result = rewrite.apply(sample)
        # Since spaces are added after every character, we expect a space after each character
        expected_text = "T h i s   i s   a   t e s t . "
        assert result == {
            "text": expected_text
        }

    def test_with_other_key(self):
        sample = {
            "other_text": "Hello!"
        }
        rewrite = RewriteAddSpaceSeq(key="other_text", prob=1.0, min_spaces=2, max_spaces=2)  # 2 spaces after each char

        result = rewrite.apply(sample)
        expected_text = "H  e  l  l  o  !  "
        assert result == {
            "other_text": expected_text
        }

    def test_is_task_compatible(self):
        rewrite = RewriteAddSpaceSeq()

        assert rewrite.is_task_compatible('some-task')
        assert rewrite.is_task_compatible('mbpp')
        assert rewrite.is_task_compatible('mmlu')
        assert rewrite.is_task_compatible('humaneval')
