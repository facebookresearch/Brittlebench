"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import CompositeRewrite, Rewrite
from brittlebench.perturbations.poe_perturbation import PoEInstructionsPerturbation
from brittlebench.perturbations.drop_options_perturbation import DropOptionsPerturbation


class RewritePoEDropOptions(Rewrite):
    def __init__(self, 
                 choices="choice",
                 answer="answer", 
                 target_option_count=2,
                 is_poe=True,
                 apply_to="process_docs"):
        super().__init__(name="rewrite_poe_drop_options", apply_to=apply_to)
        self.choices = choices
        self.answer = answer
        self.exclusive_tasks = ["mmlu", "truthfulqa_mc1", "logiqa", "gpqa"]
        self.target_option_count = target_option_count
        self.perturbation = DropOptionsPerturbation(target_option_count=target_option_count, is_poe=is_poe)

    def apply(self, sample: Dict) -> Dict:
        modified_list, new_answer = self.perturbation.apply(
            choices=sample[self.choices],
            answer=sample[self.answer],
            )
        sample[self.choices] = modified_list
        sample[self.answer] = new_answer
        return sample


class RewriteAddPoEInstructions(Rewrite):
    def __init__(self, 
                 is_poe: bool = True,
                 key: str = "text",
                 apply_to="build_all_requests"):
        super().__init__(name="rewrite_add_poe_instructions", apply_to=apply_to)
        self.key = key
        self.perturbation = PoEInstructionsPerturbation(is_poe=is_poe)

    def apply(self, sample: Dict) -> Dict:
        modified_text = self.perturbation.apply(sample[self.key])
        sample[self.key] = modified_text
        return sample


class CompositeRewritePoE(CompositeRewrite):
    def __init__(self, 
                 target_option_count: int = 2,
                 choices = "choices", 
                 answer = "answer",
        ):
        rewrites = [
            RewritePoEDropOptions(target_option_count=target_option_count, 
                                  choices=choices, 
                                  answer=answer, 
                                  is_poe=True),
            RewriteAddPoEInstructions(is_poe=True),
        ]
        super().__init__(name="rewrite_poe", rewrites=rewrites)


class CompositeRewriteNoPoE(CompositeRewrite):
    """Baseline of PoE where we drop options and we request the model give the correct answer. Used as a baseline for PoE."""
    def __init__(self, 
                 target_option_count: int = 2,
                 choices = "choices", 
                 answer = "answer",
        ):
        rewrites = [
            RewritePoEDropOptions(target_option_count=target_option_count, 
                                  choices=choices, 
                                  answer=answer, 
                                  is_poe=False),
            RewriteAddPoEInstructions(is_poe=False),
        ]
        super().__init__(name="rewrite_no_poe", rewrites=rewrites)
