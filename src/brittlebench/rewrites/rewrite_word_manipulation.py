"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.word_manipulation_perturbation import WordManipulation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteWordManipulation(Rewrite):
    """Apply word manipulation to a given sample key.

    By default, will apply a mix of splitting and merging words.

    manipulation_type='split' splits words in the text.
    manipulation_type='merge' merges words in the text.
    """

    def __init__(self, name: str,
                 manipulation_type: str,
                 key: str = "text"):
        super().__init__(name=name)
        self.key = key
        self.manipulation_type = manipulation_type
        self.apply_to = "process_docs"

        if manipulation_type not in ["split", "merge"]:
            raise ValueError(
                f"Invalid manipulation_type: {manipulation_type}. Must be one of 'split' or 'merge'."
            )
        self.perturbation = WordManipulation(manipulation_type=manipulation_type)

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample


class RewriteWordSplit(RewriteWordManipulation):
    """Split words in the given sample key."""

    def __init__(self, key: str = "text"):
        super().__init__(name="rewrite_word_split", key=key, manipulation_type="split")


class RewriteWordMerge(RewriteWordManipulation):
    """Merge words in the given sample key."""

    def __init__(self, key: str = "text"):
        super().__init__(name="rewrite_word_merge", key=key, manipulation_type="merge")