"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from datasets import Dataset

from brittlebench.rewrites.rewrite_latexify_word_problems import RewriteLatexifyWordProblems


class TestRewriteLatexifyWordProblems:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_with_default_key(self):
        sample = {
            "text": "Gunter is trying to count the jelly beans in a jar. He asks his friends how many they think are in the jar. One says 80. Another says 20 more than half the first one. A third says 25% more than the first one. What is their average guess?"
        }

        rewrite = RewriteLatexifyWordProblems()

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["text"]
            == "Gunter is trying to count the jelly beans in a jar. He asks his friends how many they think are in the jar. One says $80$. Another says $20$ more than half the first one. A third says $25\\%$ more than the first one. What is their average guess?"
        )

    def test_with_other_key(self):
        sample = {
            "problem": "Terry eats 2 yogurts a day. They are currently on sale at 4 yogurts for $5.00. How much does he spend on yogurt over 30 days?",
        }

        rewrite = RewriteLatexifyWordProblems(key='problem')

        rewritten_sample = rewrite.apply(sample)

        assert (
            rewritten_sample["problem"]
            == "Terry eats $2$ yogurts a day. They are currently on sale at $4$ yogurts for $\\$5.00$. How much does he spend on yogurt over $30$ days?"
        )
