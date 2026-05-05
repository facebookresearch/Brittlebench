"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.shuffle_order_perturbation import (
    ShuffleOrderPerturbation,
)
from brittlebench.rewrites.rewrite import Rewrite


class RewriteListWithShuffledOrder(Rewrite):
    """Shuffle the order of any list."""

    def __init__(self, 
                 choices: str = "choices", 
                 answer: str = "answer", 
                 apply_to="process_docs"):

        super().__init__(name="rewrite_shuffled_order_options", apply_to=apply_to)
        self.choices = choices
        self.answer = answer
        self.exclusive_tasks = ["mmlu", "truthfulqa_mc1", "logiqa", "gpqa"]
        self.perturbation = ShuffleOrderPerturbation()

    def apply(self, sample: Dict) -> Dict:
        modified_list, new_answer = self.perturbation.apply(
            choices=sample[self.choices],
            answer=sample[self.answer],
            )
        sample[self.choices] = modified_list
        sample[self.answer] = new_answer
        return sample
