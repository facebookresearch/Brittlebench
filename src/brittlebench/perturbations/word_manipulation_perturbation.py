"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from augly.text.functional import merge_words, split_words

from brittlebench.perturbations.perturbation import TextPerturbation


class WordManipulation(TextPerturbation):

    def __init__(self, manipulation_type: str):
        super().__init__()
        random.seed(42)

        if manipulation_type not in ["split", "merge"]:
            raise ValueError(
                f"Invalid manipulation_type: {manipulation_type}. Must be one of 'split' or 'merge'."
            )

        self.manipulation_type = manipulation_type

    def apply(self, text: str) -> str:
        if self.manipulation_type == "split":
            return "\n".join(split_words(line) for line in text.splitlines())
        elif self.manipulation_type == "merge":
            return "\n".join(merge_words(line) for line in text.splitlines())
        else:
            raise ValueError(f"Invalid manipulation_type: {self.manipulation_type}")
