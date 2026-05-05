"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_word_manipulation import (
    RewriteWordMerge,
    RewriteWordSplit,
    RewriteWordManipulation,
)   

class TestRewriteWordManipulation:
    
    def test_word_split(self):
        sample = {
            "text": "Hello world! This is a test.",
        }
        rewrite = RewriteWordSplit()
        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"]
            == "Hel lo world! This is a t est."
        )

    def test_word_merge(self):
        sample = {
            "text": "Hello world! This is a test.",
        }
        rewrite = RewriteWordMerge()
        rewritten_sample = rewrite.apply(sample)

        assert rewritten_sample["text"] == "Helloworld! This is a test."

    def test_with_other_key(self):
        sample = {
            "question": "Hello world! This is a test.",
        }
        rewrite = RewriteWordSplit(key="question")
        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["question"]
            == "Hel lo world! This is a t est."
        )

    def test_invalid_manipulation_type(self):
        try:
            RewriteWordManipulation(name="invalid_rewrite", manipulation_type="invalid_type")
        except ValueError as e:
            assert str(e) == "Invalid manipulation_type: invalid_type. Must be one of 'split' or 'merge'."
        else:
            assert False, "ValueError was not raised for invalid manipulation_type"
