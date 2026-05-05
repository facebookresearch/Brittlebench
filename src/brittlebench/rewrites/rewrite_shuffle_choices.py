"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.shuffle_choices_perturbation import (
    ShuffleChoicesPerturbation,
)
from brittlebench.rewrites.rewrite import Rewrite


class RewriteListWithShuffledChoices(Rewrite):
    """Shuffle the order of any list."""

    def __init__(self, 
                 apply_to="build_all_requests"):

        super().__init__(name="rewrite_shuffled_choices", 
                         apply_to=apply_to)
        self.exclusive_tasks = ["mmlu", "truthfulqa_mc1", "logiqa", "gpqa"]
        self.perturbation = ShuffleChoicesPerturbation()

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(text=sample[self.key])
        return sample
