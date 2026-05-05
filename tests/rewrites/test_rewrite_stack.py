"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pytest
import random 
from datasets import Dataset

from brittlebench.rewrites.rewrite_stack import RewriteStack, Stage


class DummyPerturbation:
    def apply(self, text):
        return text + "\nThis is a suffix."

class DummyRewrite:
    def __init__(self, name):
        self.name = name
        self.apply_to = "process_docs"
        self.perturbation = DummyPerturbation()

    def apply(self, sample):
        sample["text"] = self.perturbation.apply(sample["text"])
        return sample

class TestRewriteStack:

    def test_rewrite_stack_length(self):
        rewrite = DummyRewrite(name="dummy1")
        stack_len1 = RewriteStack(*[rewrite])

        random_len = random.randint(3, 10)
        random_rewrites = [DummyRewrite(name=f"dummy{i}") for i in range(random_len)]
        stack_random = RewriteStack(*random_rewrites)

        assert len(stack_len1.rewrites) == 1
        assert len(stack_random.rewrites) == random_len
        assert stack_len1.names == "dummy1"
        assert stack_random.names == "+".join(rw.name for rw in random_rewrites)

    def test_empty_stack(self):
        stack = RewriteStack(*[])

        assert len(stack.rewrites) == 0
        assert stack.names == "baseline"

    def test_add_rewrite(self):
        rewrite1 = DummyRewrite(name="dummy1")
        rewrite2 = DummyRewrite(name="dummy2")
        stack = RewriteStack(*[rewrite1])
        new_stack = stack.add(rewrite2)

        assert len(stack.rewrites) == 1
        assert len(new_stack.rewrites) == 2
        assert new_stack.rewrites[0].name == "dummy1"
        assert new_stack.rewrites[1].name == "dummy2"
        assert new_stack.names == "dummy1+dummy2"

    def test_with_hf_dataset(self):
        sample = {
            "text": "This is a question."
        }
        ds = Dataset.from_list([sample])
        rewrite1 = DummyRewrite(name="dummy1")

        stack = RewriteStack(*[rewrite1])
        process_docs = stack.to_process_docs(stage=Stage.PROCESS_DOCS)
        rewritten_dataset = process_docs(ds)

        assert (
            rewritten_dataset[0]["text"]
            == "This is a question.\nThis is a suffix."
        )

    def test_with_str(self):
        text = "This is a question."
        rewrite1 = DummyRewrite(name="dummy1")

        stack = RewriteStack(*[rewrite1])
        process_text = stack.apply(sample=text, stage=Stage.PROCESS_DOCS)

        assert (
            process_text == "This is a question.\nThis is a suffix."
        )
